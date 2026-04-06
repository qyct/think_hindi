# हिंदी शब्द संग्रह | Hindi Words Collection

A simple web application to display random Hindi words, compiled from various public datasets including frequency word lists, Wikipedia, and other sources.

## Features

- 🎲 **Random Word Display**: Generate random Hindi words with one click
- 🔢 **Adjustable Count**: Choose how many words to display (1-1000)
- 📋 **Copy to Clipboard**: One-click copy of comma-separated words
- 🌐 **Modern Dark Theme**: Beautiful UI with gradient accents
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Fast & Lightweight**: Pure HTML/CSS/JS, no dependencies

## Quick Start

### Option 1: Use Pre-compiled Words
The `thraw/thraw.txt` file already contains 21,909+ unique Hindi words. Simply:
1. Open `index.html` in your browser, or
2. Deploy this folder to GitHub Pages

### Option 2: Compile Your Own Words
```bash
# Compile words from sources
python3 scripts/compile_hindi_words.py
```

## Project Structure

```
think_hindi/
├── index.html          # Main web page
├── app.js              # Application logic
├── styles.css          # Styling (dark theme with Syne + Noto Sans Devanagari fonts)
├── thraw/              # Compiled Hindi word file
│   └── thraw.txt       # Single file with all unique words (21,909+ words)
├── scripts/            # Word compilation scripts
│   ├── compile_hindi_words.py  # Main compilation script
│   ├── advanced_compile.py     # Advanced compilation options
│   ├── sources.txt             # List of data sources
│   └── temp/                   # Temporary download folder (gitignored)
└── .gitignore          # Git ignore rules
```

## Data Sources

Words are compiled from these public datasets:

- **Frequency Words** - Hindi word frequency list with ~50,000 most common words
- **Hindi Wikipedia** - Hindi language Wikipedia content
- **HuggingFace Datasets** (for future expansion):
  - OSCAR Corpus (`oscar-corpus/community-oscar`)
  - MC4 (`mc4`)
  - FineWeb-2 (`HuggingFaceFW/fineweb-2`)
  - Wikipedia (`wikipedia`)
  - RedPajama (`togethercomputer/RedPajama-Data-1T`)
- **Other Sources**:
  - CommonCrawl (`commoncrawl.org`)
  - Wikimedia dumps (`dumps.wikimedia.org`)
  - The Pile (`pile.eleuther.ai`)

All source URLs are documented in `scripts/sources.txt`.

## Design Decisions

### Architecture
- **Single File Approach**: All words consolidated into `thraw/thraw.txt` for simplicity
- **Clean Scripts Folder**: Contains only Python scripts and sources.txt
- **Temporary Downloads**: All downloads go to `scripts/temp/` (gitignored)
- **Source References**: `sources.txt` documents all available data sources

### UI/UX
- **Dark Theme**: Modern dark background with gold accents for better readability
- **Typography**: Syne font for UI, Noto Sans Devanagari for Hindi text
- **Three Controls**: Count input, Generate button, Copy button (minimal interface)
- **Horizontal Scrolling**: Words display in single row with horizontal scroll
- **Visual Feedback**: Button states show success/error for copy operations

### Data Processing
- **Unique Words**: Compilation script removes duplicates automatically
- **Sorted Output**: Words are sorted alphabetically in thraw.txt
- **Progress Indicators**: Downloads show progress percentage
- **Error Handling**: Failed downloads are logged but don't stop compilation

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

## Customization

### Adjust Word Display Limits
Edit `index.html`:
```html
<input type="number" id="wordCount" min="1" max="1000" value="100">
```

Edit `app.js`:
```javascript
// Change max word limit
if (value > 1000) this.wordCountInput.value = 1000;
```

### Compile Additional Words
1. Add new source URLs to `scripts/sources.txt`
2. Run `python3 scripts/compile_hindi_words.py`
3. Words will be added to `thraw/thraw.txt`

### Modify Theme
Edit `styles.css` to customize colors:
```css
:root {
    --bg: #0c0c0f;          /* Background color */
    --accent: #e8b86d;       /* Accent color (gold) */
    --text: #f0ede8;         /* Text color */
    /* ... more variables ... */
}
```

## Development

### Local Testing
```bash
# Using Python's built-in server
python3 -m http.server 8000

# Or using Node.js http-server
npx http-server
```

Then open `http://localhost:8000`

### Python Requirements
No external dependencies required for basic functionality. The compilation script uses:
- `requests` - for downloading word lists
- `pathlib` - for file path operations
- `re` - for text processing

To install dependencies:
```bash
pip install requests
```

## File Management

### Adding Words
1. Place word files in `thraw/` folder
2. Or run compilation script to fetch from sources
3. Words are automatically deduplicated and sorted

### Cleaning Up
- `scripts/temp/` - Contains temporary downloads (safe to delete)
- Old `words_*.txt` files have been consolidated into `thraw.txt`

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

This project is open source and available under the MIT License.

## Contributing

Contributions welcome! Feel free to:
- Add more word sources
- Improve word compilation
- Enhance the UI/UX
- Fix bugs
- Add new features

---

Made with ❤️ for Hindi language learners and enthusiasts
