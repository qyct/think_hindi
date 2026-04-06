#!/usr/bin/env python3
"""
Remove Purna Viram from Words
Remove purna viram (।) character from words while keeping the words
"""

import re
from pathlib import Path
from wordutils import read_words, save_words, print_separator

# Configuration
THRAW_FILE = Path(__file__).parent.parent / "thraw" / "thraw.txt"

def remove_purna_viram(words):
    """Remove purna viram from words"""
    print_separator()
    print("🧹 REMOVING PURNA VIRAM (।)")
    print_separator()

    # Find words with purna viram
    words_with_purna = [word for word in words if '।' in word]

    print(f"\n📊 Statistics:")
    print(f"  Total words: {len(words):,}")
    print(f"  Words with purna viram: {len(words_with_purna)}")

    # Remove purna viram from words
    cleaned_words = set()
    removed_count = 0

    for word in words:
        if '।' in word:
            # Remove purna viram
            cleaned_word = word.replace('।', '')
            if cleaned_word:  # Only add if not empty after removal
                cleaned_words.add(cleaned_word)
            removed_count += 1
        else:
            cleaned_words.add(word)

    # Check if removing purna viram created duplicates
    duplicate_count = len(words) - len(cleaned_words)

    print(f"\n✅ Processing complete:")
    print(f"  Words processed: {len(words_with_purna)}")
    print(f"  Duplicates created: {duplicate_count}")
    print(f"  Final word count: {len(cleaned_words):,}")

    return cleaned_words

def main():
    """Main function"""
    try:
        # Read words
        words = read_words()
        print(f"\n📂 Read {len(words):,} words from thraw.txt")

        # Remove purna viram
        cleaned_words = remove_purna_viram(words)

        # Save cleaned words
        print(f"\n💾 Saving to {THRAW_FILE}...")
        save_words(cleaned_words)

        print(f"✅ Saved {len(cleaned_words):,} unique Hindi words")

        # Show sample of cleaned words
        words_with_purna_before = [w for w in words if '।' in w]
        if words_with_purna_before:
            print(f"\n📋 Sample of words cleaned:")
            for word in words_with_purna_before[:10]:
                cleaned = word.replace('।', '')
                print(f"  '{word}' → '{cleaned}'")

        print("\n" + "=" * 60)
        print("🎉 Purna Viram Removal Complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
