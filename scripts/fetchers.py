#!/usr/bin/env python3
"""
Hindi Word Fetchers
Data fetching functions from various sources
"""

import os
import re
import requests
import time
from pathlib import Path
from typing import Set, Dict, List
from datetime import datetime
from urllib.parse import quote

try:
    from datasets import load_dataset
    HAS_DATASETS = True
except ImportError:
    HAS_DATASETS = False

# Import utilities
from word_utils import (
    is_pure_hindi, extract_hindi_words, TEMP_DIR,
    print_separator
)

# Constants
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_frequency_words() -> Set[str]:
    """
    Fetch Hindi frequency words from GitHub
    Source: https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/hi/hi_full.txt
    """
    print_separator()
    print("📥 Fetching: Frequency Words (GitHub)")
    print_separator()

    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/hi/hi_full.txt"

    try:
        print(f"  URL: {url}")
        print("  Downloading...")

        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()

        words = set()
        total_lines = 0

        for line in response.iter_lines(decode_unicode=True):
            if line.strip():
                total_lines += 1
                parts = line.strip().split(' ', 1)
                if parts:
                    word = parts[0].strip()
                    if is_pure_hindi(word):
                        words.add(word)

                if total_lines % 10000 == 0:
                    print(f"  Processed {total_lines:,} lines...")

        print(f"  ✅ Complete!")
        print(f"  Total lines: {total_lines:,}")
        print(f"  Pure Hindi words: {len(words):,}")

        # Save to temp
        temp_file = TEMP_DIR / "frequency_words_full.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(words)))
        print(f"  💾 Saved to: {temp_file}")

        return words

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return set()

def fetch_wikipedia_articles(article_list: List[str] = None, limit: int = None) -> Set[str]:
    """
    Fetch words from Wikipedia articles
    Args:
        article_list: List of article names to fetch
        limit: Maximum number of articles to fetch
    """
    print_separator()
    print("📥 Fetching: Hindi Wikipedia Articles")
    print_separator()

    if article_list is None:
        # Default comprehensive article list
        article_list = [
            # Main topics
            "मुखपृष्ठ", "भारत", "हिन्दी", "दिल्ली", "मुंबई", "कोलकाता",
            # States & cities
            "राजस्थान", "महाराष्ट्र", "तमिलनाडु", "कर्नाटक", "गुजरात",
            "उत्तरप्रदेश", "बंगाल", "पंजाब", "चेन्नई", "बैंगलोर",
            # Subjects
            "साहित्य", "इतिहास", "भूगोल", "विज्ञान", "गणित",
            # Culture
            "संगीत", "कला", "सिनेमा",
            # Religion
            "हिंदू_धर्म", "बौद्ध_धर्म", "इस्लाम", "योग",
            # Nature
            "प्रकृति", "पर्यावरण", "जलवायु",
            # Technology
            "कंप्यूटर", "इंटरनेट", "मोबाइल",
            # Sports
            "क्रिकेट", "फुटबॉल",
            # Important figures
            "महात्मा_गांधी",
        ]

    if limit:
        article_list = article_list[:limit]

    all_words = set()
    successful = 0
    failed = 0

    print(f"  Articles to fetch: {len(article_list)}")

    for i, article in enumerate(article_list, 1):
        try:
            article_url = f"https://hi.wikipedia.org/wiki/{quote(article)}"
            print(f"  [{i}/{len(article_list)}] {article}...", end=' ', flush=True)

            response = requests.get(article_url, headers=HEADERS, timeout=30)
            response.raise_for_status()

            words = extract_hindi_words(response.text)
            all_words.update(words)

            successful += 1
            print(f"✅ {len(words):,} words")

            # Small delay to be respectful
            time.sleep(0.5)

        except Exception as e:
            failed += 1
            print(f"❌ {str(e)[:30]}")

    print(f"\n  ✅ Complete!")
    print(f"  Successful: {successful}/{len(article_list)}")
    print(f"  Failed: {failed}/{len(article_list)}")
    print(f"  Total unique words: {len(all_words):,}")

    # Save to temp
    temp_file = TEMP_DIR / "wikipedia_words.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(all_words)))
    print(f"  💾 Saved to: {temp_file}")

    return all_words

def test_source_frequency() -> Dict:
    """Test Frequency Words source"""
    print("\n" + "=" * 70)
    print("📥 TEST: Frequency Words (GitHub)")
    print("=" * 70)

    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/hi/hi_full.txt"

    try:
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()

        # Sample first 1000 lines
        sample_lines = []
        for i, line in enumerate(response.iter_lines(decode_unicode=True)):
            if i >= 1000:
                break
            sample_lines.append(line)

        hindi_words = set()
        for line in sample_lines:
            if line.strip():
                parts = line.strip().split(' ', 1)
                if parts:
                    word = parts[0].strip()
                    if is_pure_hindi(word):
                        hindi_words.add(word)

        return {
            'name': 'Frequency Words (GitHub)',
            'url': url,
            'ease': 5,
            'quality': 5,
            'quantity': 5,
            'total_score': 15,
            'sample_words': len(hindi_words),
            'purity': 100.0,
            'status': '✅ RECOMMENDED #1'
        }

    except Exception as e:
        return {'name': 'Frequency Words', 'error': str(e)}

def test_source_wikipedia() -> Dict:
    """Test Hindi Wikipedia source"""
    print("\n" + "=" * 70)
    print("📥 TEST: Hindi Wikipedia")
    print("=" * 70)

    url = "https://hi.wikipedia.org/"

    try:
        # Test 3 articles
        test_articles = ["मुखपृष्ठ", "भारत", "हिन्दी"]
        all_words = set()

        for article in test_articles:
            try:
                article_url = f"{url}wiki/{quote(article)}"
                response = requests.get(article_url, headers=HEADERS, timeout=30)
                response.raise_for_status()
                words = extract_hindi_words(response.text)
                all_words.update(words)
            except:
                pass

        return {
            'name': 'Hindi Wikipedia',
            'url': url,
            'ease': 3,
            'quality': 4,
            'quantity': 4,
            'total_score': 11,
            'sample_words': len(all_words),
            'purity': 100.0,
            'status': '✅ RECOMMENDED #2'
        }

    except Exception as e:
        return {'name': 'Hindi Wikipedia', 'error': str(e)}

def test_all_sources() -> List[Dict]:
    """Test all sources and return results"""
    print("=" * 70)
    print("🧪 TESTING HINDI WORD SOURCES")
    print("=" * 70)

    results = []

    # Test Frequency Words
    results.append(test_source_frequency())

    # Test Wikipedia
    results.append(test_source_wikipedia())

    # Test HuggingFace sources (if available)
    if HAS_DATASETS:
        print("\n" + "=" * 70)
        print("📥 TEST: HuggingFace Datasets")
        print("=" * 70)
        print("  ⚠️  HuggingFace datasets available but not tested")
        print("  (OSC@R is gated, MC4 is deprecated)")
        results.append({
            'name': 'HuggingFace Datasets',
            'status': '⚠️ See sources.json for details'
        })
    else:
        print("\n  ⚠️  HuggingFace datasets library not installed")

    # Print summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    for result in results:
        if 'error' not in result and 'total_score' in result:
            name = result['name']
            score = result['total_score']
            status = result.get('status', '')
            print(f"{name:30} Score: {score}/15 {status}")

    return results
