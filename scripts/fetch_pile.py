#!/usr/bin/env python3
"""
Hindi Words from The Pile
Fetches Hindi words from The Pile dataset (EleutherAI)
"""

import re
import requests
from pathlib import Path
from typing import Set, Optional

try:
    from datasets import load_dataset
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("⚠️  HuggingFace datasets library not installed. Install with: pip install datasets")

SCRIPT_DIR = Path(__file__).parent
TEMP_DIR = SCRIPT_DIR / "temp"
OUTPUT_DIR = SCRIPT_DIR.parent / "thraw"

# Create directories
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Hindi Unicode range
HINDI_UNICODE_RANGE = (0x0900, 0x097F)

def is_hindi_text(text: str) -> bool:
    """Check if text contains Hindi characters"""
    return any(ord(char) >= HINDI_UNICODE_RANGE[0] and ord(char) <= HINDI_UNICODE_RANGE[1]
               for char in text)

def extract_hindi_words(text: str) -> Set[str]:
    """Extract Hindi words from text"""
    hindi_pattern = re.compile(r'[\u0900-\u097F]+')
    words = hindi_pattern.findall(text)

    filtered_words = set()
    for word in words:
        word = word.strip()
        if len(word) >= 2 and not word.isdigit():
            word = word.strip('।.,;:?!()[]{}"\'-')
            if len(word) >= 2:
                filtered_words.add(word)

    return filtered_words

def fetch_pile_hindi(max_samples: int = 500) -> Set[str]:
    """Fetch Hindi text from The Pile dataset"""
    if not HF_AVAILABLE:
        return set()

    print("\n📚 Fetching from The Pile (Hindi content)...")

    words = set()

    try:
        # The Pile is a large dataset, we'll stream it
        dataset = load_dataset("EleutherAI/the_pile", split="train", streaming=True)

        count = 0
        hindi_count = 0
        total_checked = 0

        print("  Searching for Hindi content...")

        for item in dataset:
            if hindi_count >= max_samples:
                break

            total_checked += 1

            text = item.get('text', '')
            metadata = item.get('meta', {})

            # Check if this might be Hindi content
            if is_hindi_text(text):
                extracted = extract_hindi_words(text)
                if extracted:
                    words.update(extracted)
                    hindi_count += 1

                    if hindi_count % 50 == 0:
                        print(f"    Found {hindi_count} Hindi samples, {len(words)} unique words")

            # Progress update
            if total_checked % 10000 == 0:
                print(f"    Checked {total_checked} documents, found {hindi_count} Hindi samples")

        print(f"✓ The Pile: Found {len(words)} unique Hindi words from {hindi_count} samples")
        return words

    except Exception as e:
        print(f"✗ Error fetching The Pile: {e}")
        return set()

def fetch_pile_components() -> Set[str]:
    """Fetch from specific Pile components that might have Hindi"""
    if not HF_AVAILABLE:
        return set()

    print("\n📚 Fetching from Pile components...")

    all_words = set()

    # Some Pile components that might have Hindi content
    components = [
        "EuroParliament",  # Parliamentary proceedings
        "Enron",           # Email corpus (unlikely but possible)
        "Github",          # Code (unlikely)
        "Books3",          # Books (possible)
    ]

    # The Pile doesn't separate components in HF
    # This is a placeholder for component-specific fetching
    print("  Note: Component-specific filtering requires metadata filtering")
    print("  Using general Pile search instead...")

    all_words.update(fetch_pile_hindi(max_samples=500))

    return all_words

def fetch_indian_corpora_sample() -> Set[str]:
    """Fetch from publicly available Indian corpora"""
    print("\n🇮🇳 Fetching from Indian corpora samples...")

    all_words = set()

    # Sample URLs for Indian government Hindi content
    sources = [
        {
            "name": "India.gov.in Hindi",
            "url": "https://www.india.gov.in/hindi",
            "description": "Official Indian government portal"
        },
        {
            "name": "MyGov Hindi",
            "url": "https://www.mygov.in/hindi/",
            "description": "MyGov platform Hindi section"
        },
    ]

    for source in sources:
        try:
            print(f"  Fetching: {source['name']}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(source['url'], headers=headers, timeout=30)
            response.raise_for_status()

            # Handle encoding
            if response.encoding == None:
                response.encoding = response.apparent_encoding

            text = response.text

            if is_hindi_text(text):
                words = extract_hindi_words(text)
                all_words.update(words)
                print(f"    Found {len(words)} Hindi words")
            else:
                print(f"    No Hindi content found")

        except Exception as e:
            print(f"    ✗ Error: {e}")

    print(f"✓ Indian corpora: Found {len(all_words)} unique Hindi words")
    return all_words

def save_words(words: Set[str], filename: str):
    """Save words to file"""
    output_file = TEMP_DIR / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        sorted_words = sorted(list(words))
        f.write('\n'.join(sorted_words))
    print(f"💾 Saved {len(words)} words to {output_file}")

def main():
    """Main function"""
    print("=" * 60)
    print("📚 The Pile Hindi Words Fetcher")
    print("=" * 60)

    if not HF_AVAILABLE:
        print("\n❌ HuggingFace datasets library not available")
        print("Install with: pip install datasets")
        return

    all_words = set()

    # Fetch from The Pile
    all_words.update(fetch_pile_hindi(max_samples=1000))

    # Fetch from Indian corpora
    all_words.update(fetch_indian_corpora_sample())

    # Save results
    if all_words:
        save_words(all_words, "pile_hindi_words.txt")

        print("\n" + "=" * 60)
        print("✅ The Pile fetching complete!")
        print("=" * 60)
        print(f"📊 Total unique words: {len(all_words):,}")
        print(f"💾 Saved to: {TEMP_DIR / 'pile_hindi_words.txt'}")
    else:
        print("\n⚠️  No words fetched from The Pile")

if __name__ == "__main__":
    main()
