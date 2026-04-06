#!/usr/bin/env python3
"""
Hindi Words from CommonCrawl
Fetches Hindi words from CommonCrawl data snapshots
"""

import re
import requests
import gzip
from pathlib import Path
from typing import Set
import io

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

def get_commoncrawl_indices() -> list:
    """Get available CommonCrawl indices"""
    print("\n📡 Fetching CommonCrawl indices...")

    try:
        url = "https://index.commoncrawl.org/collinfo.json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        indices = response.json()

        print(f"✓ Found {len(indices)} available indices:")
        for idx in indices:
            print(f"  - {idx.get('id', 'unknown')}")

        return indices

    except Exception as e:
        print(f"✗ Error fetching indices: {e}")
        return []

def search_commoncrawl_ccindex(query: str, index_id: str = None, limit: int = 100) -> Set[str]:
    """Search CommonCrawl CC-Index for Hindi content"""
    print(f"\n🔍 Searching CommonCrawl for Hindi content...")

    if not index_id:
        # Use latest index
        indices = get_commoncrawl_indices()
        if indices:
            index_id = indices[0].get('id', '')
        else:
            return set()

    print(f"  Using index: {index_id}")

    all_words = set()
    url = f"https://index.commoncrawl.org/{index_id}-index"

    # Search for Hindi language pages
    params = {
        'url': '*.hi',  # Hindi language URLs
        'output': 'json',
        'fl': 'url',    # Only return URLs
        'limit': limit
    }

    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()

        lines = response.text.strip().split('\n')
        print(f"  Found {len(lines)} URLs")

        # We would need to fetch the actual content from these URLs
        # This is a simplified version - in practice, you'd download the WARC files
        print("  Note: Full content extraction requires WARC file processing")
        print("  Consider using pre-extracted Hindi datasets instead")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    return all_words

def download_warc_sample(warc_path: str, max_records: int = 100) -> Set[str]:
    """Download and process a sample WARC file"""
    print(f"\n📥 Processing WARC file: {warc_path}")

    all_words = set()

    try:
        # Download WARC file (sample)
        base_url = "https://data.commoncrawl.org/"
        url = base_url + warc_path

        print(f"  Downloading: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; HindiWordsBot/1.0)'
        }

        response = requests.get(url, headers=headers, timeout=120, stream=True)

        # Process WARC file (this is simplified)
        # In practice, you'd use warcio library
        print("  Note: WARC processing requires warcio library")
        print("  Install: pip install warcio")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    return all_words

def fetch_indian_web_samples() -> Set[str]:
    """Fetch Hindi content from Indian web domains"""
    print("\n🌐 Fetching from Indian web domains...")

    all_words = set()

    # List of Indian domains with Hindi content
    indian_domains = [
        "https://pib.gov.in/hindi/",  # Press Information Bureau
        "https://hindi.oneindia.com/",
        "https://www.bbc.com/hindi",
        "https://www.jagran.com/",
    ]

    for domain in indian_domains:
        try:
            print(f"  Fetching: {domain}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(domain, headers=headers, timeout=30)
            response.raise_for_status()

            # Try to detect encoding
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

    print(f"✓ Indian web: Found {len(all_words)} unique Hindi words")
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
    print("🌍 CommonCrawl Hindi Words Fetcher")
    print("=" * 60)

    all_words = set()

    # Get available indices
    indices = get_commoncrawl_indices()

    # Method 1: Search CC-Index (metadata only)
    # all_words.update(search_commoncrawl_ccindex("lang:hi"))

    # Method 2: Fetch from Indian web domains (more practical)
    all_words.update(fetch_indian_web_samples())

    # Note: Full CommonCrawl processing requires:
    # 1. Downloading WARC/WAT/WET files
    # 2. Using warcio library for parsing
    # 3. Significant bandwidth and storage
    # Consider using pre-processed Hindi datasets instead

    # Save results
    if all_words:
        save_words(all_words, "commoncrawl_hindi_words.txt")

        print("\n" + "=" * 60)
        print("✅ CommonCrawl fetching complete!")
        print("=" * 60)
        print(f"📊 Total unique words: {len(all_words):,}")
        print(f"💾 Saved to: {TEMP_DIR / 'commoncrawl_hindi_words.txt'}")
    else:
        print("\n⚠️  No words fetched")

    print("\n📝 Note: For comprehensive CommonCrawl processing:")
    print("  1. Install warcio: pip install warcio")
    print("  2. Download WET files (extracted text)")
    print("  3. Process for Hindi language content")
    print("  4. Or use pre-processed Hindi datasets")

if __name__ == "__main__":
    main()
