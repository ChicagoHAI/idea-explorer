"""
Fetch research ideas from IdeaHub and convert to Idea Explorer YAML format.

Usage:
    python fetch_from_ideahub.py <ideahub_url>
    python fetch_from_ideahub.py https://hypogenic.ai/ideahub/idea/HGVv4Z0ALWVHZ9YsstWT
"""

import sys
import os
import re
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import yaml
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env.local or .env
env_local = Path(__file__).parent.parent.parent / ".env.local"
env_file = Path(__file__).parent.parent.parent / ".env"

if env_local.exists():
    load_dotenv(env_local)
elif env_file.exists():
    load_dotenv(env_file)


def fetch_ideahub_content(url: str) -> dict:
    """
    Fetch content from IdeaHub URL.

    Args:
        url: IdeaHub idea URL (e.g., https://hypogenic.ai/ideahub/idea/...)

    Returns:
        Dictionary with extracted content
    """
    print(f"📥 Fetching idea from IdeaHub...")
    print(f"   URL: {url}")

    try:
        # Fetch page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract content (this may need adjustment based on actual HTML structure)
        # Try to find title
        title = None
        title_elem = soup.find('h1') or soup.find('h2')
        if title_elem:
            title = title_elem.get_text(strip=True)

        # Try to find description/content
        description = None
        # Look for main content areas
        content_selectors = [
            'div.description',
            'div.content',
            'div.idea-content',
            'article',
            'main'
        ]

        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                description = content_elem.get_text(separator='\n', strip=True)
                break

        # If still no description, try to get all paragraphs
        if not description:
            paragraphs = soup.find_all('p')
            if paragraphs:
                description = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # Extract tags
        tags = []
        tag_elems = soup.find_all(class_=re.compile(r'tag|label|badge', re.I))
        for tag_elem in tag_elems:
            tag_text = tag_elem.get_text(strip=True)
            if tag_text and len(tag_text) < 50:  # Reasonable tag length
                tags.append(tag_text)

        # Extract author
        author = None
        author_elem = soup.find(class_=re.compile(r'author|posted-by', re.I))
        if author_elem:
            author = author_elem.get_text(strip=True)

        # Get all text as fallback
        all_text = soup.get_text(separator='\n', strip=True)

        return {
            'url': url,
            'title': title,
            'description': description or all_text,
            'tags': tags,
            'author': author,
            'raw_html': response.text
        }

    except requests.RequestException as e:
        print(f"❌ Error fetching URL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error parsing content: {e}")
        sys.exit(1)


def convert_to_yaml(ideahub_content: dict) -> dict:
    """
    Use GPT to convert IdeaHub content to Idea Explorer YAML format.

    Args:
        ideahub_content: Dictionary with IdeaHub content

    Returns:
        Dictionary in Idea Explorer format
    """
    print("\n🤖 Converting to Idea Explorer format using GPT...")

    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env.local or .env")
        print("   Please add your OpenAI API key to use this feature.")
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("❌ Error: openai package not installed")
        print("   Install with: uv add openai")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Read schema for reference
    schema_path = Path(__file__).parent.parent.parent / "ideas" / "schema.yaml"
    with open(schema_path, 'r') as f:
        schema_content = f.read()

    # Read example for reference
    example_path = Path(__file__).parent.parent.parent / "ideas" / "examples" / "ai_chain_of_thought_evaluation.yaml"
    with open(example_path, 'r') as f:
        example_content = f.read()

    # Create prompt for GPT
    prompt = f"""You are an expert research assistant helping convert research ideas from IdeaHub to the Idea Explorer YAML format.

# IdeaHub Content

Title: {ideahub_content.get('title', 'No title')}
Tags: {', '.join(ideahub_content.get('tags', []))}
Author: {ideahub_content.get('author', 'Unknown')}

Description/Content:
{ideahub_content.get('description', 'No description')}

# Task

Convert this IdeaHub idea into a complete YAML file following the Idea Explorer schema.

# Schema Reference

{schema_content}

# Example YAML

Here's an example of a well-formatted idea:

{example_content}

# Instructions

1. **Domain**: Infer the most appropriate domain from: machine_learning, data_science, systems, theory, scientific_computing, nlp, computer_vision, reinforcement_learning, artificial_intelligence
   - Use "artificial_intelligence" for LLM/AI research, prompt engineering, AI agents
   - Use "nlp" for traditional NLP (non-LLM)
   - Use "machine_learning" for model training/evaluation

2. **Hypothesis**: Extract or formulate a clear, testable hypothesis from the description

3. **Methodology**: Design a reasonable experimental approach including:
   - Steps to execute the research
   - Appropriate baselines
   - Relevant metrics

4. **Constraints**: Specify reasonable constraints:
   - For AI/LLM research: cpu_only, budget: "$50-150", time_limit: 3600-7200
   - For ML research: gpu_required if needed, appropriate time limits

5. **Expected Outputs**: Define what the research should produce (metrics, visualizations, reports)

6. **Evaluation Criteria**: List clear success criteria

7. **Background**: Expand on the idea's context and motivation

Be comprehensive but realistic. The resulting YAML should be directly usable for running experiments.

# Output Format

Return ONLY the YAML content, starting with "idea:". Do not include markdown code fences or explanations.
"""

    try:
        print("   Calling GPT API...")
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert research assistant that converts research ideas into structured YAML format. You always return valid YAML without markdown formatting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=8000
        )

        yaml_content = response.choices[0].message.content.strip()

        # Remove markdown code fences if present
        yaml_content = re.sub(r'^```ya?ml\s*\n', '', yaml_content)
        yaml_content = re.sub(r'\n```\s*$', '', yaml_content)
        yaml_content = yaml_content.strip()

        print("   ✓ Conversion complete")

        # Parse YAML to validate
        try:
            parsed = yaml.safe_load(yaml_content)
            return parsed
        except yaml.YAMLError as e:
            print(f"⚠️  Warning: Generated YAML may have issues: {e}")
            print("   Attempting to fix...")
            # Try to return anyway
            return yaml.safe_load(yaml_content)

    except Exception as e:
        print(f"❌ Error calling GPT API: {e}")
        sys.exit(1)


def save_yaml_file(idea_data: dict, url: str) -> Path:
    """
    Save the idea as a YAML file.

    Args:
        idea_data: Parsed YAML data
        url: Original IdeaHub URL

    Returns:
        Path to saved file
    """
    # Generate filename from title or URL
    if 'idea' in idea_data and 'title' in idea_data['idea']:
        title = idea_data['idea']['title']
        # Sanitize title for filename
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '_', filename)
        filename = filename[:50]  # Limit length
    else:
        # Extract ID from URL
        match = re.search(r'/idea/([A-Za-z0-9]+)', url)
        if match:
            filename = f"ideahub_{match.group(1)}"
        else:
            filename = "ideahub_idea"

    # Add metadata about source
    if 'idea' not in idea_data:
        idea_data = {'idea': idea_data}

    if 'metadata' not in idea_data['idea']:
        idea_data['idea']['metadata'] = {}

    idea_data['idea']['metadata']['source'] = 'IdeaHub'
    idea_data['idea']['metadata']['source_url'] = url

    # Save to ideas/ directory
    ideas_dir = Path(__file__).parent.parent.parent / "ideas"
    ideas_dir.mkdir(exist_ok=True)

    output_path = ideas_dir / f"{filename}.yaml"

    # Check if file exists
    counter = 1
    while output_path.exists():
        output_path = ideas_dir / f"{filename}_{counter}.yaml"
        counter += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(idea_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return output_path


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch research ideas from IdeaHub and convert to Idea Explorer YAML format"
    )
    parser.add_argument(
        "url",
        help="IdeaHub idea URL (e.g., https://hypogenic.ai/ideahub/idea/...)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output YAML file path (default: auto-generate in ideas/)",
        default=None
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Automatically submit the idea after conversion"
    )

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith('http'):
        print(f"❌ Error: Invalid URL: {args.url}")
        print("   URL should start with http:// or https://")
        sys.exit(1)

    print("=" * 80)
    print("IdeaHub to Idea Explorer Converter")
    print("=" * 80)

    # Step 1: Fetch content
    ideahub_content = fetch_ideahub_content(args.url)

    if ideahub_content.get('title'):
        print(f"\n✓ Found idea: {ideahub_content['title']}")

    # Step 2: Convert with GPT
    idea_data = convert_to_yaml(ideahub_content)

    # Step 3: Save file
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(idea_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    else:
        output_path = save_yaml_file(idea_data, args.url)

    print(f"\n✅ Idea saved to: {output_path}")

    # Step 4: Optionally submit
    if args.submit:
        print("\n📤 Submitting idea to Idea Explorer...")
        from core.idea_manager import IdeaManager

        manager = IdeaManager()
        idea_id = manager.submit_idea(idea_data['idea'], validate=True)

        print(f"\n✓ Idea submitted successfully: {idea_id}")
        print(f"\nTo run this research:")
        print(f"  python src/core/runner.py {idea_id}")
    else:
        print(f"\nTo submit this idea:")
        print(f"  python src/cli/submit.py {output_path}")

    print("\n" + "=" * 80)
    print("Done!")
    print("=" * 80)


if __name__ == "__main__":
    main()
