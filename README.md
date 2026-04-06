# हिंदी शब्द संग्रह | Hindi Words Collection

A simple web application to display random Hindi words, compiled from comprehensive testing and selection of the best Hindi word sources.

## Features

- 🎲 **Random Word Display**: Generate random Hindi words with one click
- 🔢 **Adjustable Count**: Choose how many words to display (1-1000)
- 📋 **Copy to Clipboard**: One-click copy of comma-separated words
- 🌐 **Modern Dark Theme**: Beautiful UI with gradient accents
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Fast & Lightweight**: Pure HTML/CSS/JS, no dependencies
- 📊 **Comprehensive Collection**: 48,814+ unique Hindi words from tested sources
- 🛠️ **CLI Tool**: Easy command-line interface for word collection management

## Quick Start

### Option 1: Use Pre-compiled Words
The `thraw/thraw.txt` file contains **48,814** unique Hindi words. Simply:
1. Open `index.html` in your browser, or
2. Deploy this folder to GitHub Pages

### Option 2: Use CLI Tool
```bash
# Show statistics
python main.py stats

# Expand word collection
python main.py expand
```

## Project Structure

```
think_hindi/
├── main.py                  # CLI tool (main interface)
├── index.html               # Main web page
├── app.js                   # Application logic
├── styles.css               # Styling (dark theme)
├── thraw/                   # Compiled Hindi word file
│   └── thraw.txt            # 48,814 unique Hindi words
├── scripts/                 # Core utilities
│   ├── word_utils.py        # Word processing utilities
│   ├── fetchers.py          # Data fetching functions
│   ├── sources.json         # Source data with metadata
│   ├── advanced_compile.py  # Advanced compilation (reference)
│   └── temp/                # Temporary downloads (gitignored)
└── .gitignore               # Git ignore rules
```

## CLI Usage

The `main.py` CLI tool provides all functionality for managing the Hindi word collection.

### Basic Commands

```bash
# Show statistics
python main.py stats

# Check word purity
python main.py check-purity

# Check purity with verbose output
python main.py check-purity --verbose
```

### Word Management

```bash
# Remove non-Hindi words
python main.py clean

# Remove duplicate words
python main.py deduplicate

# Basic compilation from Frequency Words + Wikipedia sample
python main.py compile

# Accumulate from 2 best sources (adds to existing)
python main.py accumulate

# Extended Wikipedia fetch (144 articles)
python main.py expand
```

### Testing

```bash
# Test word sources (quick test)
python main.py test-sources

# Test sources with full analysis
python main.py test-sources --full

# Fetch from all sources
python main.py fetch-all
```

### Global Flags

```bash
# Dry run (preview changes without saving)
python main.py --dry-run clean

# Skip confirmation prompts
python main.py --yes expand

# Verbose output
python main.py --verbose check-purity

# Combine flags
python main.py --dry-run --yes clean
```

### Examples

```bash
# Check current status
python main.py stats

# Clean and verify
python main.py --yes clean && python main.py check-purity

# Expand collection (takes several minutes)
python main.py --yes expand

# Test before expanding
python main.py test-sources && python main.py expand
```

## Data Sources

### 🏆 Top 2 Recommended Sources (Tested & Selected)

**#1. Frequency Words (GitHub) - Score: 15/15**
- **Ease**: 5/5 - Direct URL download, no dependencies
- **Quality**: 5/5 - 100% pure Hindi, clean frequency list format
- **Quantity**: 5/5 - ~50,000 words
- **URL**: https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/hi/hi_full.txt
- **Status**: ✅ USED - Primary source for common Hindi words

**#2. Hindi Wikipedia - Score: 11/15**
- **Ease**: 3/5 - Web scraping with standard libraries
- **Quality**: 4/5 - Clean encyclopedia content
- **Quantity**: 4/5 - ~100,000+ words available
- **URL**: https://hi.wikipedia.org/
- **Status**: ✅ USED - Fetched 144 articles for diverse vocabulary

### Other Sources Tested

| Source | Score | Status | Notes |
|--------|-------|--------|-------|
| Wikimedia Dumps | 10/15 | ⚠️ Complex | Use web scraping instead |
| CommonCrawl | 8/15 | ❌ Not Rec. | WARC processing required |
| The Pile | 8/15 | ❌ Not Rec. | 825GB+, Hindi sparse |
| RedPajama | 8/15 | ❌ Not Rec. | 1TB+, not practical |
| FineWeb-2 | 7/15 | ⚠️ Untested | Hindi quality uncertain |
| OSCAR | 6/15 | ⚠️ Gated | Requires HF auth |
| MC4 | 1/15 | ❌ Deprecated | Scripts no longer supported |

**See `scripts/sources.json` for detailed test results and scoring criteria.**

## Word Collection Process

### Phase 1: Source Testing
1. Tested 9 different Hindi word sources
2. Rated each on Ease (1-5), Quality (1-5), Quantity (1-5)
3. Selected top 2 sources based on total score
4. Documented results in `scripts/sources.json`

### Phase 2: Data Collection
1. **Frequency Words**: Downloaded complete dataset (~21K lines → 20K words)
2. **Wikipedia**: Fetched 144 articles covering:
   - Indian states & cities (25 articles)
   - Academic subjects (13 articles)
   - Culture & Arts (6 articles)
   - Religion & Spirituality (8 articles)
   - Nature & Environment (7 articles)
   - Technology & Modern topics (8 articles)
   - Sports (6 articles)
   - Food & Health (7 articles)
   - Education (5 articles)
   - Society & Family (5 articles)
   - Language & Literature (7 articles)
   - Important figures (5 articles)
   - Science & Discovery (6 articles)
   - Economy & Industry (6 articles)
   - Infrastructure (8 articles)
   - Miscellaneous topics (15 articles)

### Phase 3: Data Cleaning
1. Removed all non-Hindi characters
2. Filtered to pure Devanagari script (U+0900-U+097F)
3. Removed duplicates
4. Sorted alphabetically

### Final Statistics
- **Starting words**: 21,431 (cleaned from original mixed content)
- **Frequency Words added**: 20,041 (0 new - already covered)
- **Wikipedia added**: 37,798 words (23,668 new)
- **Final count**: **48,814 unique Hindi words**

## Development

### Python Requirements

For CLI functionality:
```bash
pip install requests
# Optional: for HuggingFace datasets
pip install datasets huggingface_hub
```

### Naming Conventions

**Python Files:**
- Use lowercase only (no underscores, no hyphens)
- Examples: `wordutils.py`, `fetchwords.py`, `cleanpurnaviram.py`
- Multi-word names are concatenated: `cleanpurnaviram.py` (not `clean_purna_viram.py`)

**Rationale:**
- Simpler imports: `from wordutils import` vs `from word_utils import`
- Consistent, clean filenames
- Easier to work with across different systems

### Project Architecture

**Core Modules:**
- `main.py` - CLI interface with argparse
- `scripts/wordutils.py` - Word processing utilities
- `scripts/fetchwords.py` - Data fetching functions
- `scripts/cleanpurnaviram.py` - Purna viram removal script
- `scripts/sources.json` - Source data with metadata

**Key Functions:**
- `is_pure_hindi()` - Check Devanagari script
- `extract_hindi_words()` - Extract from text
- `read_words()` / `save_words()` - File I/O
- `clean_words()` - Remove non-Hindi
- `remove_duplicates()` - Deduplication
- `check_purity()` - Purity verification
- `fetch_frequency_words()` - GitHub fetcher
- `fetch_wikipedia_articles()` - Wikipedia fetcher

### Adding New Commands

To add a new CLI command:

1. Add function to `main.py`:
```python
def cmd_myfunction(args):
    """My function description"""
    # Your code here
    pass
```

2. Register in `commands` dictionary:
```python
commands = {
    # ... existing commands
    'myfunction': cmd_myfunction,
}
```

3. Add subparser:
```python
subparsers.add_parser('myfunction', help='My function help')
```

### Testing

```bash
# Test individual components
python -m pytest tests/  # (if tests exist)

# Manual testing
python main.py stats
python main.py check-purity --verbose
python main.py --dry-run clean
```

## Deployment to GitHub Pages

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` folder: `/ (root)`
   - Click Save

3. **Access your site**:
   ```
   https://YOUR_USERNAME.github.io/think_hindi/
   ```

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## File Management

### Adding Words
```bash
# Using CLI
python main.py expand

# Or manually edit thraw/thraw.txt
# (one word per line, UTF-8 encoding)
```

### Cleaning Up
```bash
# Remove non-Hindi words
python main.py clean

# Remove duplicates
python main.py deduplicate

# Check purity
python main.py check-purity
```

### Backup
```bash
# Backup current collection
cp thraw/thraw.txt thraw/thraw.txt.backup

# Restore backup
cp thraw/thraw.txt.backup thraw/thraw.txt
```

## Troubleshooting

### Common Issues

**Q: CLI not working?**
```bash
# Make sure you're using the correct Python
~/PYENV/bin/python main.py stats

# Or add to PATH
export PATH="$HOME/PYENV/bin:$PATH"
python main.py stats
```

**Q: Words not displaying in web app?**
- Check `thraw/thraw.txt` exists and has content
- Verify browser console for errors
- Ensure UTF-8 encoding

**Q: Fetching sources fails?**
- Check internet connection
- Some sources may require authentication (OSCAR)
- Wikipedia may rate-limit (delays built in)

### Getting Help

```bash
# General help
python main.py --help

# Command-specific help
python main.py expand --help
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions welcome! Focus areas:
- Add new word sources (update `sources.json`)
- Improve word collection algorithms
- Enhance CLI functionality
- Add web app features
- Improve documentation

## Credits

- **Frequency Words Dataset**: [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords)
- **Hindi Wikipedia**: [hi.wikipedia.org](https://hi.wikipedia.org/)
- **CLI Framework**: Built with argparse

---

Made with ❤️ for Hindi language learners and enthusiasts

**Last Updated**: 2026-04-06
**Word Count**: 48,814 unique Hindi words
**CLI Version**: 2.0
