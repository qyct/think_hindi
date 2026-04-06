#!/usr/bin/env python3
"""
Hindi Word Utilities
Core utility functions for Hindi word processing
"""

import re
import json
from pathlib import Path
from typing import Set, List, Tuple

# Constants
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
THRAW_FILE = PROJECT_ROOT / "thraw" / "thraw.txt"
SOURCES_FILE = SCRIPT_DIR / "sources.json"
TEMP_DIR = SCRIPT_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# Hindi Unicode pattern for Devanagari script
HINDI_PATTERN = re.compile(r'[\u0900-\u097F]+')
PURE_HINDI_PATTERN = re.compile(r'^[\u0900-\u097F]+$')

def is_pure_hindi(word: str) -> bool:
    """Check if word contains ONLY Hindi characters (Devanagari script)"""
    return bool(PURE_HINDI_PATTERN.match(word.strip()))

def extract_hindi_words(text: str) -> Set[str]:
    """Extract pure Hindi words from text"""
    words = HINDI_PATTERN.findall(text)
    filtered = set()
    for word in words:
        word = word.strip()
        if len(word) >= 2 and is_pure_hindi(word):
            filtered.add(word)
    return filtered

def read_words(filepath: Path = None) -> Set[str]:
    """Read words from file, default to thraw.txt"""
    if filepath is None:
        filepath = THRAW_FILE

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            words = set(line.strip() for line in f if line.strip())
        return words
    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
        return set()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return set()

def save_words(words: Set[str], filepath: Path = None) -> bool:
    """Save words to file, sorted alphabetically"""
    if filepath is None:
        filepath = THRAW_FILE

    try:
        sorted_words = sorted(list(words))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted_words))
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def load_sources() -> dict:
    """Load sources from sources.json"""
    try:
        with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Sources file not found: {SOURCES_FILE}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing sources.json: {e}")
        return {}

def clean_words(words: Set[str] = None) -> Tuple[Set[str], int]:
    """
    Remove non-Hindi words from the set
    Returns: (clean_words, removed_count)
    """
    if words is None:
        words = read_words()

    original_count = len(words)
    clean_words = set(word for word in words if is_pure_hindi(word))
    removed_count = original_count - len(clean_words)

    return clean_words, removed_count

def remove_duplicates(words: Set[str] = None) -> Tuple[Set[str], int]:
    """
    Remove duplicate words (already handled by Set, but for completeness)
    Returns: (unique_words, duplicates_removed)
    """
    if words is None:
        words = read_words()

    # If input is a list, convert to set to remove duplicates
    if isinstance(words, list):
        original_count = len(words)
        unique_words = set(words)
        duplicates_removed = original_count - len(unique_words)
        return unique_words, duplicates_removed

    # If already a set, no duplicates possible
    return words, 0

def check_purity(words: Set[str] = None, show_examples: bool = False) -> Tuple[int, int, List[str]]:
    """
    Check purity of words (pure Hindi vs non-Hindi)
    Returns: (pure_count, impure_count, impure_words_list)
    """
    if words is None:
        words = read_words()

    pure_words = []
    impure_words = []

    for word in words:
        if is_pure_hindi(word):
            pure_words.append(word)
        else:
            impure_words.append(word)

    return len(pure_words), len(impure_words), impure_words

def get_statistics() -> dict:
    """Get statistics about the current word collection"""
    words = read_words()
    pure_count, impure_count, impure_words = check_purity(words)

    return {
        'total_words': len(words),
        'pure_hindi': pure_count,
        'non_hindi': impure_count,
        'purity_percentage': (pure_count / len(words) * 100) if words else 0,
        'filepath': str(THRAW_FILE)
    }

def print_separator(char: str = "=", length: int = 70):
    """Print a separator line"""
    print(char * length)

def print_stats(stats: dict):
    """Print statistics in a formatted way"""
    print_separator()
    print("📊 WORD COLLECTION STATISTICS")
    print_separator()
    print(f"📁 File: {stats['filepath']}")
    print(f"📊 Total words:     {stats['total_words']:,}")
    print(f"✅ Pure Hindi:      {stats['pure_hindi']:,} ({stats['purity_percentage']:.2f}%)")
    if stats['non_hindi'] > 0:
        print(f"❌ Non-Hindi:       {stats['non_hindi']:,}")
    print_separator()
