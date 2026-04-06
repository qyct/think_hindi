# Hindi Words Compilation Scripts

This folder contains scripts to compile Hindi words from various public datasets.

## Python Environment Setup

The project uses a virtual environment at `~/PYENV`. It's already set up with all required dependencies.

To activate the environment:
```bash
source ~/PYENV/bin/activate
```

## Quick Start

### Option 1: Sample Data (Recommended - Fast)
Run with pre-loaded sample words:
```bash
source ~/PYENV/bin/activate
python scripts/compile_hindi_words.py
```

### Option 2: Advanced Compilation
For advanced users who want to fetch real data:

```bash
# Using the helper script (recommended)
./scripts/run_with_pyenv.sh python scripts/advanced_compile.py --sample-only

# Or manually activate the environment
source ~/PYENV/bin/activate
python scripts/advanced_compile.py --sample-only

# Run with real data fetching (slower, requires internet)
python scripts/advanced_compile.py --real-data
```

## Data Sources

The scripts are designed to work with these public datasets:

- **OSCAR Corpus**: `oscar-corpus/community-oscar` - Massive web-scale text corpus
- **MC4**: `mc4` - Multilingual colossal cleaned common crawl
- **FineWeb-2**: `HuggingFaceFW/fineweb-2` - High-quality web dataset
- **CommonCrawl**: `commoncrawl.org` - Web crawl data
- **Wikipedia**: `dumps.wikimedia.org` - Hindi Wikipedia dumps
- **The Pile**: `pile.eleuther.ai` - Diverse text dataset
- **RedPajama**: `togethercomputer/RedPajama-Data-1T` - Large language model dataset

## Output Files

Words are categorized and saved to the `thraw/` folder:

- `words_common.txt` - Everyday common words
- `words_literary.txt` - Literary and longer words
- `words_technical.txt` - Technology and technical terms
- `words_scientific.txt` - Scientific and academic terms
- `words_news.txt` - News and current affairs vocabulary
- `words_all.txt` - Master file with all words

## Web App Usage

Once words are compiled, simply open `index.html` in a browser or deploy to GitHub Pages.

The web app will:
1. Load all word files from `thraw/`
2. Display random words based on your count preference
3. Allow shuffling and regenerating word sets

## Notes

- **Sample Mode**: Uses built-in Hindi word database (fast, no internet needed)
- **Real Data Mode**: Fetches from actual datasets (requires `datasets` library, slower)
- For GitHub Pages deployment, all files in `thraw/` will be served directly
- The web app automatically loads all available `words_*.txt` files

## Troubleshooting

**Issue**: Scripts don't run
- Make sure Python 3.7+ is installed
- Check file permissions: `chmod +x scripts/*.py`

**Issue**: Real data fetching fails
- Install dependencies: `pip install -r scripts/requirements.txt`
- Check internet connection
- Some datasets may require HuggingFace authentication

**Issue**: Words not displaying in web app
- Check that `thraw/` folder contains `words_*.txt` files
- Ensure files are UTF-8 encoded
- Check browser console for errors
