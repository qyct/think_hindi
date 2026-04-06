#!/usr/bin/env python3
"""
Hindi Words from HuggingFace Datasets
Fetches Hindi text from various HuggingFace datasets
"""

import os
import re
from pathlib import Path
from typing import Set, Optional
import json

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
            word = word.strip('।.,;:?!()[]{}"\'')
            if len(word) >= 2:
                filtered_words.add(word)

    return filtered_words

def fetch_oscar_hindi(max_samples: int = 1000) -> Set[str]:
    """Fetch Hindi text from OSCAR corpus"""
    if not HF_AVAILABLE:
        return set()

    print("\n📥 Fetching from OSCAR Corpus (Hindi)...")
    words = set()

    try:
        # Load OSCAR dataset for Hindi
        dataset = load_dataset("oscar-corpus/OSCAR-2201", "hi", split="train", streaming=True)

        count = 0
        for item in dataset:
            if count >= max_samples:
                break

            text = item.get('text', '')
            if is_hindi_text(text):
                extracted = extract_hindi_words(text)
                words.update(extracted)
                count += 1

                if count % 100 == 0:
                    print(f"  Processed {count} samples, found {len(words)} unique words")

        print(f"✓ OSCAR: Found {len(words)} unique Hindi words")
        return words

    except Exception as e:
        print(f"✗ Error fetching OSCAR: {e}")
        return set()

def fetch_mc4_hindi(max_samples: int = 1000) -> Set[str]:
    """Fetch Hindi text from MC4 dataset"""
    if not HF_AVAILABLE:
        return set()

    print("\n📥 Fetching from MC4 (Hindi)...")
    words = set()

    try:
        # Load MC4 dataset for Hindi
        dataset = load_dataset("mc4", "hi", split="train", streaming=True)

        count = 0
        for item in dataset:
            if count >= max_samples:
                break

            text = item.get('text', '')
            if is_hindi_text(text):
                extracted = extract_hindi_words(text)
                words.update(extracted)
                count += 1

                if count % 100 == 0:
                    print(f"  Processed {count} samples, found {len(words)} unique words")

        print(f"✓ MC4: Found {len(words)} unique Hindi words")
        return words

    except Exception as e:
        print(f"✗ Error fetching MC4: {e}")
        return set()

def fetch_fineweb2_hindi(max_samples: int = 500) -> Set[str]:
    """Fetch Hindi text from FineWeb-2 dataset"""
    if not HF_AVAILABLE:
        return set()

    print("\n📥 Fetching from FineWeb-2 (Hindi)...")
    words = set()

    try:
        # FineWeb-2 might have language codes
        dataset = load_dataset("HuggingFaceFW/fineweb-2", split="train", streaming=True)

        count = 0
        hindi_found = 0

        for item in dataset:
            if hindi_found >= max_samples:
                break

            text = item.get('text', '')
            if is_hindi_text(text):
                extracted = extract_hindi_words(text)
                if extracted:  # Only count if we found Hindi words
                    words.update(extracted)
                    hindi_found += 1

                count += 1
                if hindi_found % 50 == 0:
                    print(f"  Found {hindi_found} Hindi samples, {len(words)} unique words")

        print(f"✓ FineWeb-2: Found {len(words)} unique Hindi words")
        return words

    except Exception as e:
        print(f"✗ Error fetching FineWeb-2: {e}")
        return set()

def fetch_redpajama_hindi(max_samples: int = 500) -> Set[str]:
    """Fetch Hindi text from RedPajama dataset"""
    if not HF_AVAILABLE:
        return set()

    print("\n📥 Fetching from RedPajama (Hindi)...")
    words = set()

    try:
        # RedPajama is large, we'll sample from it
        dataset = load_dataset("togethercomputer/RedPajama-Data-1T", split="train", streaming=True)

        count = 0
        hindi_found = 0

        for item in dataset:
            if hindi_found >= max_samples:
                break

            text = item.get('text', '')
            if is_hindi_text(text):
                extracted = extract_hindi_words(text)
                if extracted:
                    words.update(extracted)
                    hindi_found += 1

                count += 1
                if hindi_found % 50 == 0:
                    print(f"  Found {hindi_found} Hindi samples, {len(words)} unique words")

        print(f"✓ RedPajama: Found {len(words)} unique Hindi words")
        return words

    except Exception as e:
        print(f"✗ Error fetching RedPajama: {e}")
        return set()

def save_words(words: Set[str], filename: str):
    """Save words to file"""
    output_file = TEMP_DIR / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        sorted_words = sorted(list(words))
        f.write('\n'.join(sorted_words))
    print(f"💾 Saved {len(words)} words to {output_file}")

def main():
    """Main function to fetch from all HuggingFace sources"""
    if not HF_AVAILABLE:
        print("\n❌ HuggingFace datasets library not available")
        print("Install with: pip install datasets")
        return

    print("=" * 60)
    print("🤗 HuggingFace Hindi Words Fetcher")
    print("=" * 60)

    all_words = set()

    # Fetch from different datasets
    all_words.update(fetch_oscar_hindi(max_samples=1000))
    all_words.update(fetch_mc4_hindi(max_samples=1000))
    all_words.update(fetch_fineweb2_hindi(max_samples=500))
    all_words.update(fetch_redpajama_hindi(max_samples=500))

    # Save combined results
    if all_words:
        save_words(all_words, "huggingface_hindi_words.txt")

        print("\n" + "=" * 60)
        print("✅ HuggingFace fetching complete!")
        print("=" * 60)
        print(f"📊 Total unique words from HuggingFace: {len(all_words):,}")
        print(f"💾 Saved to: {TEMP_DIR / 'huggingface_hindi_words.txt'}")
    else:
        print("\n⚠️  No words fetched from HuggingFace sources")

if __name__ == "__main__":
    main()
