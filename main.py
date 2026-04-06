#!/usr/bin/env python3
"""
Hindi Words Collection CLI
Main command-line interface for managing Hindi word collection
"""

import argparse
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from wordutils import (
    read_words, save_words, clean_words, remove_duplicates,
    check_purity, get_statistics, print_separator, print_stats
)
from fetchwords import (
    fetch_frequency_words, fetch_wikipedia_articles, test_all_sources
)

def cmd_clean(args):
    """Remove non-Hindi words from collection"""
    print_separator()
    print("🧹 CLEANING: Removing Non-Hindi Words")
    print_separator()

    words = read_words()
    print(f"\n📂 Current word count: {len(words):,}")

    if not args.yes:
        response = input("\n⚠️  This will remove all non-Hindi words. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            return

    clean_words_set, removed_count = clean_words(words)

    print(f"\n✅ Cleaning complete!")
    print(f"   Words removed: {removed_count:,}")
    print(f"   Remaining words: {len(clean_words_set):,}")

    if not args.dry_run:
        if save_words(clean_words_set):
            print(f"\n💾 Saved to: thraw/thraw.txt")
    else:
        print(f"\n🔍 Dry run - no changes saved")

def cmd_deduplicate(args):
    """Remove duplicate words from collection"""
    print_separator()
    print("🔍 DEDUPLICATING: Removing Duplicate Words")
    print_separator()

    words = read_words()
    print(f"\n📂 Current word count: {len(words):,}")

    unique_words, duplicates_removed = remove_duplicates(words)

    print(f"\n✅ Deduplication complete!")
    print(f"   Duplicates found: {duplicates_removed:,}")
    print(f"   Unique words: {len(unique_words):,}")

    if duplicates_removed > 0 and not args.dry_run:
        if save_words(unique_words):
            print(f"\n💾 Saved to: thraw/thraw.txt")
    elif duplicates_removed == 0:
        print(f"\n✅ No duplicates found - already clean!")
    else:
        print(f"\n🔍 Dry run - no changes saved")

def cmd_check_purity(args):
    """Check purity of word collection"""
    print_separator()
    print("🔍 CHECKING: Word Purity")
    print_separator()

    words = read_words()
    pure_count, impure_count, impure_words = check_purity(words)

    total = len(words)
    purity_pct = (pure_count / total * 100) if total > 0 else 0

    print(f"\n📊 Results:")
    print(f"   Total words:     {total:,}")
    print(f"   ✅ Pure Hindi:   {pure_count:,} ({purity_pct:.2f}%)")
    print(f"   ❌ Non-Hindi:    {impure_count:,}")

    if impure_words and args.verbose:
        print(f"\n⚠️  Non-Hindi words found:")
        for i, word in enumerate(impure_words[:20], 1):
            print(f"   {i}. {word}")
        if len(impure_words) > 20:
            print(f"   ... and {len(impure_words) - 20} more")
    elif impure_words:
        print(f"\n⚠️  Use --verbose to see non-Hindi words")
    else:
        print(f"\n🎉 All words are pure Hindi!")

def cmd_compile(args):
    """Basic compilation from Frequency Words and Wikipedia sample"""
    print_separator()
    print("📚 COMPILING: Basic Word Collection")
    print_separator()
    print("This will fetch from:")
    print("  1. Frequency Words (GitHub)")
    print("  2. Wikipedia (sample articles)")

    if not args.yes:
        response = input("\n⚠️  This will overwrite existing words. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            return

    # Fetch words
    freq_words = fetch_frequency_words()
    wiki_words = fetch_wikipedia_articles(limit=10)

    # Combine
    all_words = freq_words | wiki_words

    print_separator()
    print("💾 SAVING")
    print_separator()
    print(f"Total words: {len(all_words):,}")

    if not args.dry_run:
        if save_words(all_words):
            print(f"✅ Saved to: thraw/thraw.txt")
    else:
        print(f"🔍 Dry run - no changes saved")

def cmd_accumulate(args):
    """Accumulate from 2 best sources"""
    print_separator()
    print("📚 ACCUMULATING: From 2 Best Sources")
    print_separator()
    print("This will:")
    print("  1. Keep existing words")
    print("  2. Add Frequency Words")
    print("  3. Add Wikipedia articles")

    existing_words = read_words()
    print(f"\n📂 Existing words: {len(existing_words):,}")

    # Fetch words
    freq_words = fetch_frequency_words()
    wiki_words = fetch_wikipedia_articles(limit=10)

    # Accumulate
    all_words = existing_words | freq_words | wiki_words
    new_words = all_words - existing_words

    print_separator()
    print("💾 SAVING")
    print_separator()
    print(f"Existing words:   {len(existing_words):,}")
    print(f"New words:        {len(new_words):,}")
    print(f"Total words:      {len(all_words):,}")

    if not args.dry_run:
        if save_words(all_words):
            print(f"✅ Saved to: thraw/thraw.txt")
    else:
        print(f"🔍 Dry run - no changes saved")

def cmd_expand(args):
    """Extended Wikipedia fetch (144 articles)"""
    print_separator()
    print("📚 EXPANDING: Extended Wikipedia Fetch")
    print_separator()
    print("This will fetch from ~144 Wikipedia articles")

    existing_words = read_words()
    print(f"\n📂 Existing words: {len(existing_words):,}")

    if not args.yes:
        response = input("\n⚠️  This may take several minutes. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            return

    # Fetch extended Wikipedia
    wiki_words = fetch_wikipedia_articles()

    # Accumulate
    all_words = existing_words | wiki_words
    new_words = all_words - existing_words

    print_separator()
    print("💾 SAVING")
    print_separator()
    print(f"Existing words:   {len(existing_words):,}")
    print(f"New words:        {len(new_words):,}")
    print(f"Total words:      {len(all_words):,}")

    if not args.dry_run:
        if save_words(all_words):
            print(f"✅ Saved to: thraw/thraw.txt")
    else:
        print(f"🔍 Dry run - no changes saved")

def cmd_test_sources(args):
    """Test Hindi word sources"""
    if args.full:
        print_separator()
        print("🧪 COMPREHENSIVE SOURCE TESTING")
        print_separator()

        # Run full test (would use comprehensive_source_test.py logic)
        print("⚠️  Full testing requires comprehensive testing script")
        print("Running quick test instead...\n")

    results = test_all_sources()

    print_separator()
    print("✅ Testing complete!")
    print_separator()
    print("💡 Use 'python main.py test-sources --full' for detailed testing")

def cmd_fetch_all(args):
    """Run all fetchers"""
    print_separator()
    print("🚀 FETCHING FROM ALL SOURCES")
    print_separator()

    if not args.yes:
        response = input("\n⚠️  This will run all fetchers. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            return

    existing_words = read_words()
    print(f"\n📂 Existing words: {len(existing_words):,}")

    # Fetch from all sources
    freq_words = fetch_frequency_words()
    wiki_words = fetch_wikipedia_articles()

    # Combine all
    all_words = existing_words | freq_words | wiki_words
    new_words = all_words - existing_words

    print_separator()
    print("💾 SAVING")
    print_separator()
    print(f"New words added:  {len(new_words):,}")
    print(f"Total words:      {len(all_words):,}")

    if not args.dry_run:
        if save_words(all_words):
            print(f"✅ Saved to: thraw/thraw.txt")

def cmd_stats(args):
    """Show word collection statistics"""
    stats = get_statistics()
    print_stats(stats)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Hindi Words Collection - Manage Hindi word collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py stats              Show statistics
  python main.py check-purity       Check word purity
  python main.py clean              Remove non-Hindi words
  python main.py compile            Compile from basic sources
  python main.py expand             Expand with Wikipedia

For more help on a command:
  python main.py <command> --help
        """
    )

    # Global flags
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without saving')
    parser.add_argument('--yes', '-y', action='store_true',
                       help='Skip confirmation prompts')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # clean command
    subparsers.add_parser('clean', help='Remove non-Hindi words')

    # deduplicate command
    subparsers.add_parser('deduplicate', help='Remove duplicate words')

    # check-purity command
    check_purity_parser = subparsers.add_parser('check-purity',
                                                  help='Check word purity')
    check_purity_parser.add_argument('-v', '--verbose', action='store_true',
                                     help='Show non-Hindi words')

    # compile command
    subparsers.add_parser('compile', help='Basic compilation')

    # accumulate command
    subparsers.add_parser('accumulate', help='Accumulate from 2 best sources')

    # expand command
    subparsers.add_parser('expand', help='Extended Wikipedia fetch')

    # test-sources command
    test_sources_parser = subparsers.add_parser('test-sources',
                                                 help='Test word sources')
    test_sources_parser.add_argument('--full', action='store_true',
                                     help='Run comprehensive testing')

    # fetch-all command
    subparsers.add_parser('fetch-all', help='Run all fetchers')

    # stats command
    subparsers.add_parser('stats', help='Show statistics')

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command
    if not args.command:
        parser.print_help()
        return

    # Execute command
    commands = {
        'clean': cmd_clean,
        'deduplicate': cmd_deduplicate,
        'check-purity': cmd_check_purity,
        'compile': cmd_compile,
        'accumulate': cmd_accumulate,
        'expand': cmd_expand,
        'test-sources': cmd_test_sources,
        'fetch-all': cmd_fetch_all,
        'stats': cmd_stats,
    }

    command_func = commands.get(args.command)
    if command_func:
        try:
            command_func(args)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
