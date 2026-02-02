#!/usr/bin/env python3
"""
BibTeX Citation Validator

Validates .bib files for common issues including missing fields,
duplicate entries, and formatting problems.

Usage:
    python validate_citations.py references.bib
    python validate_citations.py references.bib --fix --output fixed.bib
"""

import argparse
import re
import sys
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


# Required fields by entry type
REQUIRED_FIELDS = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "incollection": ["author", "title", "booktitle", "year"],
    "book": ["author", "title", "publisher", "year"],
    "misc": ["author", "title", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "techreport": ["author", "title", "institution", "year"],
}

# Recommended fields
RECOMMENDED_FIELDS = {
    "article": ["volume", "pages", "doi"],
    "inproceedings": ["pages"],
    "book": ["address"],
}


def parse_bibtex(content: str) -> List[Tuple[str, str, Dict[str, str], int]]:
    """
    Parse BibTeX content into entries.
    Returns list of (entry_type, key, fields_dict, line_number).
    """
    entries = []

    # Pattern to match BibTeX entries
    entry_pattern = re.compile(
        r'@(\w+)\s*\{\s*([^,\s]+)\s*,',
        re.IGNORECASE
    )

    # Track position in content
    lines = content.split('\n')
    line_positions = {}
    pos = 0
    for i, line in enumerate(lines, 1):
        line_positions[pos] = i
        pos += len(line) + 1  # +1 for newline

    def get_line_number(char_pos):
        for pos, line in sorted(line_positions.items(), reverse=True):
            if char_pos >= pos:
                return line
        return 1

    # Find all entries
    for match in entry_pattern.finditer(content):
        entry_type = match.group(1).lower()
        key = match.group(2)
        start_pos = match.end()
        line_num = get_line_number(match.start())

        # Find matching closing brace
        brace_count = 1
        pos = start_pos
        while pos < len(content) and brace_count > 0:
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
            pos += 1

        if brace_count != 0:
            print(f"Warning: Unmatched braces for entry {key}", file=sys.stderr)
            continue

        entry_content = content[start_pos:pos-1]

        # Parse fields
        fields = {}
        field_pattern = re.compile(
            r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|(\d+))',
            re.IGNORECASE
        )

        for field_match in field_pattern.finditer(entry_content):
            field_name = field_match.group(1).lower()
            # Value can be in braces, quotes, or numeric
            field_value = field_match.group(2) or field_match.group(3) or field_match.group(4) or ""
            fields[field_name] = field_value.strip()

        entries.append((entry_type, key, fields, line_num))

    return entries


def validate_entry(entry_type: str, key: str, fields: Dict[str, str], line_num: int) -> List[str]:
    """Validate a single entry and return list of issues."""
    issues = []

    # Check required fields
    required = REQUIRED_FIELDS.get(entry_type, ["author", "title", "year"])
    for field in required:
        if field not in fields or not fields[field].strip():
            issues.append(f"Line {line_num}: {key} - Missing required field: {field}")

    # Check recommended fields
    recommended = RECOMMENDED_FIELDS.get(entry_type, [])
    for field in recommended:
        if field not in fields:
            issues.append(f"Line {line_num}: {key} - Missing recommended field: {field}")

    # Validate year format
    if "year" in fields:
        year = fields["year"]
        if not re.match(r'^\d{4}$', year):
            issues.append(f"Line {line_num}: {key} - Invalid year format: {year}")

    # Validate DOI format
    if "doi" in fields:
        doi = fields["doi"]
        if doi and not re.match(r'^10\.\d{4,}/', doi):
            issues.append(f"Line {line_num}: {key} - Invalid DOI format: {doi}")

    # Check for empty title
    if "title" in fields and not fields["title"].strip():
        issues.append(f"Line {line_num}: {key} - Empty title")

    # Check for empty author
    if "author" in fields and not fields["author"].strip():
        issues.append(f"Line {line_num}: {key} - Empty author")

    return issues


def check_duplicates(entries: List[Tuple[str, str, Dict[str, str], int]]) -> List[str]:
    """Check for duplicate keys and similar entries."""
    issues = []
    keys = defaultdict(list)

    for entry_type, key, fields, line_num in entries:
        keys[key.lower()].append((key, line_num))

    for key_lower, occurrences in keys.items():
        if len(occurrences) > 1:
            lines = [str(line) for _, line in occurrences]
            issues.append(f"Duplicate key '{occurrences[0][0]}' on lines: {', '.join(lines)}")

    return issues


def format_entry(entry_type: str, key: str, fields: Dict[str, str]) -> str:
    """Format a single entry with consistent style."""
    lines = [f"@{entry_type}{{{key},"]

    # Order fields sensibly
    field_order = ["author", "title", "booktitle", "journal", "year", "volume",
                   "number", "pages", "publisher", "address", "doi", "url", "note"]

    # Add fields in order
    added = set()
    for field in field_order:
        if field in fields and fields[field]:
            value = fields[field]
            lines.append(f"  {field:10} = {{{value}}},")
            added.add(field)

    # Add remaining fields
    for field, value in sorted(fields.items()):
        if field not in added and value:
            lines.append(f"  {field:10} = {{{value}}},")

    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate BibTeX citations")
    parser.add_argument("bibfile", help="BibTeX file to validate")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues")
    parser.add_argument("--output", "-o", help="Output file for fixed entries")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show errors")
    args = parser.parse_args()

    try:
        with open(args.bibfile, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {args.bibfile}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        # Try latin-1
        with open(args.bibfile, 'r', encoding='latin-1') as f:
            content = f.read()

    entries = parse_bibtex(content)

    if not args.quiet:
        print(f"Found {len(entries)} entries in {args.bibfile}")
        print()

    all_issues = []

    # Validate each entry
    for entry_type, key, fields, line_num in entries:
        issues = validate_entry(entry_type, key, fields, line_num)
        all_issues.extend(issues)

    # Check for duplicates
    dup_issues = check_duplicates(entries)
    all_issues.extend(dup_issues)

    # Report issues
    errors = [i for i in all_issues if "Missing required" in i or "Duplicate" in i or "Invalid" in i or "Empty" in i]
    warnings = [i for i in all_issues if i not in errors]

    if errors:
        print("ERRORS:")
        for issue in errors:
            print(f"  {issue}")
        print()

    if warnings and not args.quiet:
        print("WARNINGS:")
        for issue in warnings:
            print(f"  {issue}")
        print()

    # Summary
    if not args.quiet:
        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings")

    # Fix and output if requested
    if args.fix and args.output:
        formatted = []
        for entry_type, key, fields, _ in entries:
            formatted.append(format_entry(entry_type, key, fields))

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(formatted))
        print(f"\nFormatted entries written to {args.output}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
