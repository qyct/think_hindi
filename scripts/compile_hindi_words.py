#!/usr/bin/env python3
"""
Hindi Words Compiler
Fetches and compiles Hindi words from various public datasets
Uses sources.txt for reference and downloads to temp folder
"""

import os
import re
import requests
from pathlib import Path
from typing import Set, List
import urllib.parse

# Configuration
SCRIPT_DIR = Path(__file__).parent
TEMP_DIR = SCRIPT_DIR / "temp"
THRAW_DIR = SCRIPT_DIR.parent / "thraw"
SOURCES_FILE = SCRIPT_DIR / "sources.txt"

# Create directories
TEMP_DIR.mkdir(exist_ok=True)
THRAW_DIR.mkdir(exist_ok=True)

# Hindi Unicode range for Devanagari script
HINDI_UNICODE_RANGE = (0x0900, 0x097F)

def is_hindi_word(text: str) -> bool:
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

def download_to_file(url: str, filename: str) -> bool:
    """Download URL to temp folder with progress indication"""
    try:
        print(f"  Downloading: {url}")
        print(f"  Saving to: {filename}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=60, stream=True)
        response.raise_for_status()

        filepath = TEMP_DIR / filename
        total_size = int(response.headers.get('content-length', 0))

        with open(filepath, 'wb') as f:
            if total_size > 0:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total_size) * 100
                        print(f"  Progress: {percent:.1f}%", end='\r')
                print()  # New line after progress
            else:
                f.write(response.content)

        print(f"  ✓ Downloaded: {filepath}")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def fetch_frequency_words() -> Set[str]:
    """Fetch Hindi frequency words from GitHub"""
    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/hi/hi_full.txt"

    print("\n📥 Fetching Hindi frequency words...")

    filename = "hi_frequency_words.txt"
    if download_to_file(url, filename):
        filepath = TEMP_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            words = set()
            for line in f:
                if line.strip():
                    parts = line.strip().split(' ', 1)
                    if parts:
                        word = parts[0].strip()
                        if len(word) >= 2:
                            words.add(word)

        print(f"✓ Found {len(words)} Hindi frequency words")
        return words

    return set()

def fetch_wikipedia_hindi_sample() -> Set[str]:
    """Fetch sample Hindi text from Wikipedia"""
    print("\n📥 Fetching Hindi Wikipedia sample...")

    url = "https://hi.wikipedia.org/wiki/%E0%A4%AE%E0%A5%81%E0%A4%96%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0"

    filename = "hi_wikipedia_sample.txt"
    if download_to_file(url, filename):
        filepath = TEMP_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        words = extract_hindi_words(text)
        print(f"✓ Found {len(words)} Hindi words from Wikipedia")
        return words

    return set()

def process_temp_files() -> Set[str]:
    """Process all downloaded files in temp folder"""
    print("\n📂 Processing downloaded files...")

    all_words = set()
    temp_files = list(TEMP_DIR.glob("*.txt"))

    for filepath in temp_files:
        print(f"  Processing: {filepath.name}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if filepath.name.startswith("hi_"):
                # Process frequency words format
                words = set()
                for line in content.split('\n'):
                    if line.strip():
                        parts = line.strip().split(' ', 1)
                        if parts:
                            word = parts[0].strip()
                            if len(word) >= 2:
                                words.add(word)
                all_words.update(words)
                print(f"    Extracted {len(words)} words")
            else:
                # Process as plain text
                words = extract_hindi_words(content)
                all_words.update(words)
                print(f"    Extracted {len(words)} words")

        except Exception as e:
            print(f"    Error: {e}")

    return all_words

def add_common_hindi_words() -> Set[str]:
    """Add common Hindi words as base vocabulary"""
    print("\n📚 Adding common Hindi words...")

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

    print(f"✓ Added {len(common_hindi)} common Hindi words")
    return set(common_hindi)

def compile_words():
    """Compile Hindi words from all sources"""
    print("=" * 60)
    print("🔤 Hindi Words Compiler")
    print("=" * 60)
    print(f"📂 Temp directory: {TEMP_DIR}")
    print(f"📂 Output directory: {THRAW_DIR}")
    print(f"📄 Sources file: {SOURCES_FILE}")

    # Read sources file for reference
    if SOURCES_FILE.exists():
        print(f"\n📚 Available sources from {SOURCES_FILE.name}:")
        with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
            sources = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            for i, source in enumerate(sources[:10], 1):  # Show first 10
                print(f"  {i}. {source}")
            if len(sources) > 10:
                print(f"  ... and {len(sources) - 10} more sources")

    all_words = set()

    # Add common words
    all_words.update(add_common_hindi_words())

    # Fetch frequency words (main source)
    all_words.update(fetch_frequency_words())

    # Fetch Wikipedia sample
    all_words.update(fetch_wikipedia_hindi_sample())

    # Process any downloaded temp files
    all_words.update(process_temp_files())

    # Remove duplicates and sort
    unique_words = sorted(list(all_words))

    # Save to single thraw.txt file
    output_file = THRAW_DIR / "thraw.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_words))

    print("\n" + "=" * 60)
    print("✅ Compilation complete!")
    print("=" * 60)
    print(f"📊 Total unique words: {len(unique_words):,}")
    print(f"💾 Saved to: {output_file}")
    print(f"📁 Temp files in: {TEMP_DIR}")

    return unique_words

def main():
    """Main compilation function"""
    try:
        compile_words()
    except KeyboardInterrupt:
        print("\n\n⚠ Compilation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during compilation: {e}")
        raise

if __name__ == "__main__":
    main()
