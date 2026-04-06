#!/usr/bin/env python3
"""
Master script to fetch Hindi words from all sources
Runs all fetcher scripts and combines results
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMP_DIR = SCRIPT_DIR / "temp"
OUTPUT_DIR = SCRIPT_DIR.parent / "thraw"

# Create directories
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def run_fetcher(script_name: str, description: str) -> bool:
    """Run a fetcher script"""
    print(f"\n{'=' * 60}")
    print(f"🚀 Running: {description}")
    print(f"{'=' * 60}")

    script_path = SCRIPT_DIR / script_name

    if not script_path.exists():
        print(f"⚠️  Script not found: {script_name}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=SCRIPT_DIR,
            capture_output=False,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"⚠️  {description} failed with code {result.returncode}")
            return False

    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def combine_all_temp_files() -> set:
    """Combine all word files from temp directory"""
    print(f"\n{'=' * 60}")
    print("🔗 Combining all word files")
    print(f"{'=' * 60}")

    all_words = set()
    temp_files = list(TEMP_DIR.glob("*_hindi_words.txt"))
    temp_files.extend(TEMP_DIR.glob("hi_*.txt"))

    for filepath in temp_files:
        print(f"  Processing: {filepath.name}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                words = set(line.strip() for line in f if line.strip())
                print(f"    Found {len(words)} words")
                all_words.update(words)
        except Exception as e:
            print(f"    Error: {e}")

    return all_words

def save_combined_words(words: set):
    """Save combined words to thraw.txt"""
    print(f"\n{'=' * 60}")
    print("💾 Saving combined word list")
    print(f"{'=' * 60}")

    output_file = OUTPUT_DIR / "thraw.txt"

    # Sort and save
    sorted_words = sorted(list(words))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted_words))

    print(f"✅ Saved {len(sorted_words):,} unique Hindi words to {output_file}")

def main():
    """Main function to run all fetchers"""
    print("=" * 60)
    print("🌟 Master Hindi Words Fetcher")
    print("=" * 60)
    print("This script will fetch Hindi words from all available sources")
    print("This may take a while and require significant bandwidth")

    # List of fetchers to run
    fetchers = [
        ("compile_hindi_words.py", "Basic Compilation (Frequency + Wikipedia)"),
        ("fetch_huggingface.py", "HuggingFace Datasets (OSCAR, MC4, FineWeb-2, RedPajama)"),
        ("fetch_wikipedia.py", "Extended Wikipedia Fetcher"),
        ("fetch_commoncrawl.py", "CommonCrawl / Indian Web"),
        ("fetch_pile.py", "The Pile Dataset"),
    ]

    print(f"\n📋 Will run {len(fetchers)} fetchers:")
    for i, (script, desc) in enumerate(fetchers, 1):
        print(f"  {i}. {desc}")

    # Ask for confirmation
    response = input("\n⚠️  This may take 30+ minutes and use several GB of data. Continue? (y/n): ")

    if response.lower() != 'y':
        print("❌ Aborted by user")
        return

    # Run all fetchers
    successful = 0
    for script, desc in fetchers:
        if run_fetcher(script, desc):
            successful += 1

    # Combine all results
    print(f"\n{'=' * 60}")
    print(f"📊 Summary: {successful}/{len(fetchers)} fetchers completed")
    print(f"{'=' * 60}")

    all_words = combine_all_temp_files()

    # Save combined results
    if all_words:
        save_combined_words(all_words)

        print(f"\n{'=' * 60}")
        print("🎉 All done!")
        print(f"{'=' * 60}")
        print(f"📊 Total unique Hindi words: {len(all_words):,}")
        print(f"💾 Saved to: {OUTPUT_DIR / 'thraw.txt'}")
        print(f"\n💡 Tip: You can now refresh your web app to use the expanded word list")
    else:
        print("\n⚠️  No words found to save")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
