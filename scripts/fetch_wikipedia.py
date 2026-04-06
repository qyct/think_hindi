#!/usr/bin/env python3
"""
Hindi Words from Wikipedia
Fetches Hindi words from Wikipedia dumps and live Wikipedia
"""

import re
import requests
from pathlib import Path
from typing import Set, List
import random
import html

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

def get_wikipedia_articles(count: int = 50) -> List[str]:
    """Get list of Hindi Wikipedia articles"""
    print(f"\n📥 Fetching {count} random Hindi Wikipedia articles...")

    # Hindi Wikipedia API endpoint for random articles
    url = "https://hi.wikipedia.org/w/api.php"

    articles = []
    seen = set()

    attempts = 0
    max_attempts = count * 3  # Try up to 3x to get enough articles

    while len(articles) < count and attempts < max_attempts:
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'random',
                'rnnamespace': 0,  # Main namespace only
                'rnlimit': 20
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            random_pages = data.get('query', {}).get('random', [])

            for page in random_pages:
                title = page.get('title', '')
                if title and title not in seen:
                    seen.add(title)
                    articles.append(title)
                    if len(articles) >= count:
                        break

            if len(articles) < count:
                print(f"  Collected {len(articles)}/{count} articles...")

        except Exception as e:
            print(f"  ✗ Error: {e}")

        attempts += 1

    print(f"✓ Found {len(articles)} unique articles")
    return articles

def fetch_article_content(title: str) -> str:
    """Fetch content of a Wikipedia article"""
    url = "https://hi.wikipedia.org/w/api.php"

    try:
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'titles': title,
            'explaintext': True,
            'exsectionformat': 'plain'
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'extract' in page_data:
                return page_data['extract']

    except Exception as e:
        print(f"  ✗ Error fetching '{title}': {e}")

    return ""

def fetch_wikipedia_hindi(article_count: int = 100) -> Set[str]:
    """Fetch Hindi words from Wikipedia articles"""
    print(f"\n📚 Fetching words from {article_count} Wikipedia articles...")

    articles = get_wikipedia_articles(article_count)
    all_words = set()

    for i, title in enumerate(articles, 1):
        if i % 10 == 0:
            print(f"  Processing {i}/{len(articles)} articles...")

        content = fetch_article_content(title)

        if content:
            words = extract_hindi_words(content)
            all_words.update(words)

    print(f"✓ Wikipedia: Found {len(all_words)} unique Hindi words")
    return all_words

def fetch_wikipedia_categories(categories: List[str], articles_per_category: int = 10) -> Set[str]:
    """Fetch articles from specific Wikipedia categories"""
    print(f"\n📚 Fetching from {len(categories)} Wikipedia categories...")

    all_words = set()

    for category in categories:
        print(f"  Category: {category}")
        try:
            # Get category members
            url = "https://hi.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'categorymembers',
                'cmtitle': f'श्रेणी:{category}',
                'cmlimit': articles_per_category * 2,
                'cmnamespace': 0
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            members = data.get('query', {}).get('categorymembers', [])

            # Get articles from this category
            articles = [m.get('title', '') for m in members if m.get('ns') == 0][:articles_per_category]

            for title in articles:
                content = fetch_article_content(title)
                if content:
                    words = extract_hindi_words(content)
                    all_words.update(words)

        except Exception as e:
            print(f"    ✗ Error: {e}")

    print(f"✓ Categories: Found {len(all_words)} unique Hindi words")
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
    print("📖 Wikipedia Hindi Words Fetcher")
    print("=" * 60)

    all_words = set()

    # Method 1: Random articles
    all_words.update(fetch_wikipedia_hindi(article_count=150))

    # Method 2: Specific categories (you can add more)
    categories = [
        "भारत",  # India
        "विज्ञान",  # Science
        "इतिहास",  # History
        "साहित्य",  # Literature
        "भाषा",  # Language
        "संस्कृति",  # Culture
        "भूगोल",  # Geography
        "गणित",  # Mathematics
    ]

    all_words.update(fetch_wikipedia_categories(categories, articles_per_category=20))

    # Save combined results
    if all_words:
        save_words(all_words, "wikipedia_hindi_words.txt")

        print("\n" + "=" * 60)
        print("✅ Wikipedia fetching complete!")
        print("=" * 60)
        print(f"📊 Total unique words from Wikipedia: {len(all_words):,}")
        print(f"💾 Saved to: {TEMP_DIR / 'wikipedia_hindi_words.txt'}")
    else:
        print("\n⚠️  No words fetched from Wikipedia")

if __name__ == "__main__":
    main()
