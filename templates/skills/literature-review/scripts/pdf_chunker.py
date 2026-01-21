#!/usr/bin/env python3
"""
PDF Chunker - Preprocesses PDFs into text chunks for incremental reading.

Usage:
    python pdf_chunker.py <pdf_path> [--pages-per-chunk N] [--output-dir DIR]

Output:
    Creates chunk files: <output_dir>/<pdf_name>_chunk_001.txt, etc.
    Also creates a manifest: <output_dir>/<pdf_name>_manifest.txt
"""

import argparse
import os
from pathlib import Path

import pdfplumber


def extract_text_by_pages(pdf_path: str) -> list[tuple[int, str]]:
    """Extract text from PDF, returning list of (page_num, text) tuples."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append((i + 1, text))
    return pages


def chunk_pages(pages: list[tuple[int, str]], pages_per_chunk: int) -> list[dict]:
    """Group pages into chunks."""
    chunks = []
    for i in range(0, len(pages), pages_per_chunk):
        chunk_pages_subset = pages[i:i + pages_per_chunk]
        page_nums = [p[0] for p in chunk_pages_subset]
        text = "\n\n".join([f"--- Page {p[0]} ---\n{p[1]}" for p in chunk_pages_subset])
        chunks.append({
            "chunk_num": len(chunks) + 1,
            "pages": page_nums,
            "text": text,
            "char_count": len(text)
        })
    return chunks


def save_chunks(chunks: list[dict], pdf_path: str, output_dir: str) -> str:
    """Save chunks to files and create manifest."""
    pdf_name = Path(pdf_path).stem
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    manifest_lines = [
        f"PDF: {pdf_path}",
        f"Total chunks: {len(chunks)}",
        f"Total pages: {sum(len(c['pages']) for c in chunks)}",
        "",
        "Chunks:",
    ]

    for chunk in chunks:
        chunk_filename = f"{pdf_name}_chunk_{chunk['chunk_num']:03d}.txt"
        chunk_path = output_path / chunk_filename

        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk["text"])

        manifest_lines.append(
            f"  {chunk_filename}: pages {chunk['pages'][0]}-{chunk['pages'][-1]}, "
            f"{chunk['char_count']} chars"
        )

    manifest_path = output_path / f"{pdf_name}_manifest.txt"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines))

    return str(manifest_path)


def chunk_pdf(pdf_path: str, pages_per_chunk: int = 5, output_dir: str = None) -> str:
    """Main function to chunk a PDF."""
    if output_dir is None:
        output_dir = str(Path(pdf_path).parent / "chunks")

    print(f"Extracting text from: {pdf_path}")
    pages = extract_text_by_pages(pdf_path)
    print(f"Extracted {len(pages)} pages")

    chunks = chunk_pages(pages, pages_per_chunk)
    print(f"Created {len(chunks)} chunks ({pages_per_chunk} pages each)")

    manifest_path = save_chunks(chunks, pdf_path, output_dir)
    print(f"Saved to: {output_dir}")
    print(f"Manifest: {manifest_path}")

    return manifest_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chunk PDF into text files")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--pages-per-chunk", type=int, default=5,
                        help="Number of pages per chunk (default: 5)")
    parser.add_argument("--output-dir", help="Output directory (default: <pdf_dir>/chunks)")

    args = parser.parse_args()
    chunk_pdf(args.pdf_path, args.pages_per_chunk, args.output_dir)
