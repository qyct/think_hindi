# हिंदी शब्द संग्रह | Hindi Words Collection

A simple web application to display random Hindi words, compiled from various public datasets including OSCAR, MC4, FineWeb-2, CommonCrawl, Wikipedia, The Pile, and RedPajama.

## Features

- 🎲 **Random Word Display**: Click to get random Hindi words
- 🔢 **Adjustable Count**: Choose how many words to display (1-100)
- 🔀 **Shuffle**: Shuffle the current word set
- 📊 **Word Statistics**: See total available words
- 🌐 **GitHub Pages Ready**: Deploy directly from this folder

## Quick Start

### Option 1: Use Pre-compiled Words
The `thraw/` folder already contains compiled Hindi words. Simply:
1. Open `index.html` in your browser, or
2. Deploy this folder to GitHub Pages

### Option 2: Compile Your Own Words
```bash
# Quick method using helper script
./scripts/run_with_pyenv.sh python scripts/compile_hindi_words.py

# Or use the advanced version
./scripts/run_with_pyenv.sh python scripts/advanced_compile.py --sample-only

# Manual activation
source ~/PYENV/bin/activate
python3 scripts/compile_hindi_words.py
```

## Project Structure

```
think_hindi/
├── index.html          # Main web page
├── app.js              # Application logic
├── styles.css          # Styling
├── thraw/              # Compiled Hindi word files
│   ├── words_common.txt
│   ├── words_literary.txt
│   ├── words_technical.txt
│   ├── words_scientific.txt
│   └── words_news.txt
└── scripts/            # Word compilation scripts
    ├── compile_hindi_words.py
    ├── advanced_compile.py
    ├── requirements.txt
    └── README.md
```

## Deployment to GitHub Pages

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/think-hindi.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` folder: `/ (root)`
   - Click Save

3. **Access your site**:
   ```
   https://YOUR_USERNAME.github.io/think-hindi/
   ```

## Data Sources

Words are compiled from these public datasets:

- **OSCAR Corpus** - `oscar-corpus/community-oscar`
- **MC4** - `mc4`
- **FineWeb-2** - `HuggingFaceFW/fineweb-2`
- **CommonCrawl** - `commoncrawl.org`
- **Wikipedia** - `dumps.wikimedia.org` (Hindi)
- **The Pile** - `pile.eleuther.ai`
- **RedPajama** - `togethercomputer/RedPajama-Data-1T`

See `scripts/README.md` for compilation details.

## Customization

### Add More Words
1. Edit word files in `thraw/` folder
2. Or run compilation scripts with `--real-data` flag

### Adjust Word Display Limits
Edit `app.js`:
```javascript
// Change max word limit
if (value > 100) this.wordCountInput.value = 100;
```

### Modify Categories
Edit `scripts/compile_hindi_words.py` or `advanced_compile.py` to change word categorization logic.

## Development

### Local Testing
```bash
# Using the test script (recommended)
./scripts/test_webapp.sh

# Or manually with Python's built-in server
source ~/PYENV/bin/activate
python3 -m http.server 8000

# Or using Node.js http-server
npx http-server
```

Then open `http://localhost:8000`

### Python Environment
The project uses a virtual environment at `~/PYENV` with all required dependencies pre-installed.

To activate: `source ~/PYENV/bin/activate`

To install additional packages:
```bash
source ~/PYENV/bin/activate
pip install <package-name>
```

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

This project is open source and available under the MIT License.

## Contributing

Contributions welcome! Feel free to:
- Add more word categories
- Improve word compilation
- Enhance the UI/UX
- Fix bugs
- Add new features

---

Made with ❤️ for Hindi language learners and enthusiasts
