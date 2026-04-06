#!/usr/bin/env python3
"""
Hindi Words Compiler
Fetches and compiles Hindi words from various public datasets
"""

import os
import re
import json
import requests
from pathlib import Path
from typing import Set, List
from collections import Counter
import time

# Configuration
THRAW_DIR = Path(__file__).parent.parent / "thraw"
THRAW_DIR.mkdir(exist_ok=True)

# Hindi Unicode range for Devanagari script
HINDI_UNICODE_RANGE = (0x0900, 0x097F)

def is_hindi_word(text: str) -> bool:
    """Check if text contains Hindi characters"""
    return any(ord(char) >= HINDI_UNICODE_RANGE[0] and ord(char) <= HINDI_UNICODE_RANGE[1]
               for char in text)

def extract_hindi_words(text: str) -> Set[str]:
    """Extract Hindi words from text"""
    # Pattern to match Hindi words (Devanagari script with optional matras)
    hindi_pattern = re.compile(r'[\u0900-\u097F]+')
    words = hindi_pattern.findall(text)

    # Filter: minimum 2 characters, meaningful words
    filtered_words = set()
    for word in words:
        word = word.strip()
        if len(word) >= 2 and not word.isdigit():
            # Remove common punctuation
            word = word.strip('।.,;:?!()[]{}"\'')
            if len(word) >= 2:
                filtered_words.add(word)

    return filtered_words

def download_sample_text(url: str, max_size: int = 10000) -> str:
    """Download sample text from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Limit size to avoid memory issues
        text = response.text[:max_size]
        return text
    except Exception as e:
        print(f"Error downloading from {url}: {e}")
        return ""

def process_huggingface_dataset_info(dataset_name: str) -> List[str]:
    """
    Get info about HuggingFace dataset
    Note: Full dataset download requires huggingface_hub library
    This creates sample data for demonstration
    """
    print(f"Processing dataset: {dataset_name}")

    # For demonstration, create sample Hindi words
    # In production, you would use: from datasets import load_dataset
    sample_words = set()

    # Common Hindi words for demonstration
    common_hindi = [
        "नमस्ते", "धन्यवाद", "शुभ", "प्रणाम", "स्वागत", "कृपया",
        "जी", "हाँ", "नहीं", "माफ़ी", "विदा", "भारत", "हिंदी",
        "भाषा", "शब्द", "वाक्य", "अर्थ", "ज्ञान", "विज्ञान", "कला",
        "संगीत", "साहित्य", "संस्कृति", "इतिहास", "भूगोल", "गणित",
        "विश्व", "प्रकृति", "मानव", "समाज", "देश", "विदेश", "राजधानी",
        "शहर", "गाँव", "परिवार", "मित्र", "शिक्षा", "विद्यालय", "विश्वविद्यालय",
        "पुस्तक", "पुस्तकालय", "लेखक", "कवि", "कहानी", "कविता", "उपन्यास",
        "समाचार", "पत्र", "चित्र", "नक्शा", "सड़क", "वाहन", "रेल", "विमान",
        "जल", "थल", "आकाश", "अग्नि", "वायु", "पृथ्वी", "सूर्य", "चंद्रमा",
        "तारा", "ग्रह", "नक्षत्र", "ऋतु", "दिन", "रात", "समय", "वर्ष", "मास",
        "सप्ताह", "घंटा", "मिनट", "सेकंड", "संख्या", "अंक", "गिनती", "जोड़",
        "गुणा", "भाग", "जोड़तोड़", "माप", "वजन", "लंबाई", "चौड़ाई", "ऊंचाई",
        "गहराई", "क्षेत्र", "आयतन", "घनत्व", "तापमान", "दाब", "बल", "ऊर्जा",
        "शक्ति", "गति", "वेग", "त्वरण", "दिशा", "स्थिति", "विस्थापन", "कार्य",
        "सिद्धांत", "नियम", "प्रयोग", "अनुसंधान", "खोज", "आविष्कार", "प्रौद्योगिकी",
        "कंप्यूटर", "इंटरनेट", "सॉफ्टवेयर", "हार्डवेयर", "प्रोग्राम", "कोड", "डेटा"
    ]

    sample_words.update(common_hindi)
    return list(sample_words)

def fetch_wikipedia_hindi_sample() -> Set[str]:
    """Fetch sample Hindi text from Wikipedia"""
    url = "https://hi.wikipedia.org/wiki/%E0%A4%AE%E0%A5%81%E0%A4%96%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0"

    print("Fetching Hindi Wikipedia sample...")
    text = download_sample_text(url, max_size=50000)

    if text:
        words = extract_hindi_words(text)
        print(f"Found {len(words)} Hindi words from Wikipedia")
        return words

    return set()

def fetch_frequency_words() -> Set[str]:
    """Fetch Hindi frequency words from GitHub"""
    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/hi/hi_full.txt"

    print("Fetching Hindi frequency words...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

        # Parse frequency words format: "word frequency\n"
        words = set()
        for line in response.text.strip().split('\n'):
            if line.strip():
                # Split on first space to separate word from frequency
                parts = line.strip().split(' ', 1)
                if parts:
                    word = parts[0].strip()
                    # Filter: minimum 2 characters
                    if len(word) >= 2:
                        words.add(word)

        print(f"Found {len(words)} Hindi frequency words")
        return words

    except Exception as e:
        print(f"Error fetching frequency words: {e}")
        return set()

def categorize_words(words: Set[str]) -> dict:
    """Categorize words by type and frequency"""
    word_list = list(words)

    # Simple categorization based on word length and patterns
    categories = {
        'common': [],
        'literary': [],
        'technical': [],
        'scientific': [],
        'news': []
    }

    for word in word_list:
        word_lower = word.lower()

        # Common words (short, frequent)
        if len(word) <= 4:
            categories['common'].append(word)

        # Literary/longer words
        elif len(word) >= 6:
            categories['literary'].append(word)

        # Technical terms (contain certain patterns)
        elif any(suffix in word for suffix in ['विज्ञान', 'तकनीक', 'प्रौद्योगिकी', 'यंत्र', 'साधन']):
            categories['technical'].append(word)

        # Scientific terms
        elif any(suffix in word for suffix in ['जीव', 'रसायन', 'भौतिक', 'गणित', 'तारा', 'ग्रह']):
            categories['scientific'].append(word)

        # News/current events
        else:
            categories['news'].append(word)

    # Add some words to each category if empty
    for category, words_list in categories.items():
        if len(words_list) < 10:
            # Add some common words to fill
            categories[category].extend(word_list[:20])

    return categories

def save_words_to_files(categorized_words: dict):
    """Save categorized words to separate files"""
    for category, words in categorized_words.items():
        filename = THRAW_DIR / f"words_{category}.txt"

        # Remove duplicates and sort
        unique_words = sorted(list(set(words)))

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_words))

        print(f"Saved {len(unique_words)} words to {filename}")

def create_sample_data():
    """Create sample data for demonstration"""
    print("Creating sample Hindi word data...")

    all_words = set()

    # Add words from various sources
    sources = [
        ("Frequency Words", list(fetch_frequency_words())),
        ("Wikipedia", list(fetch_wikipedia_hindi_sample())),
        ("Common Words", process_huggingface_dataset_info("common")),
    ]

    for source_name, words in sources:
        all_words.update(words)
        print(f"Added {len(words)} words from {source_name}")

    # Save all words to a single file
    all_words_file = THRAW_DIR / "words_all.txt"
    unique_words = sorted(list(all_words))

    with open(all_words_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_words))

    print(f"\nTotal unique words: {len(all_words)}")
    print(f"Saved to: {all_words_file}")

    # Also save categorized version for compatibility
    categorized = categorize_words(all_words)
    save_words_to_files(categorized)

def main():
    """Main compilation function"""
    print("=" * 50)
    print("Hindi Words Compiler")
    print("=" * 50)

    # Create sample data
    create_sample_data()

    print("\n" + "=" * 50)
    print("Compilation complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
