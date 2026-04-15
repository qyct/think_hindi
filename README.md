# हिंदी शब्द संग्रह | Hindi Words Collection

A simple web application for learning Hindi words through frequency-based vocabulary practice.

## Features

- 🎲 **Random Word Selection**: Generate random Hindi words from frequency-ordered datasets
- 🔢 **Dual Input Control**: 
  - **Words to Draw**: Number of words to randomly select (default: 50)
  - **FROM MOST FREQ**: Total words to load from most frequent (range: 500-30,000)
- 📊 **Frequency-Based Learning**: Words organized by usage frequency — most common words first
- 📋 **One-Click Copy**: Copy selected words or learning prompts to clipboard
- 🌐 **Modern Dark Theme**: Beautiful, responsive UI with gradient accents
- ⚡ **Fast & Lightweight**: Pure HTML/CSS/JS, no dependencies
- 📱 **Mobile Friendly**: Works seamlessly on desktop and mobile devices

## Quick Start

Simply open `index.html` in your web browser. No build process or dependencies required!

## How It Works

### Word Data Structure

The app fetches Hindi words from GitHub-hosted files, each containing 3,000 words in frequency order:

```
hw01.txt → Words 1-3,000      (most common)
hw02.txt → Words 3,001-6,000
hw03.txt → Words 6,001-9,000
...
hw10.txt → Words 27,001-30,000 (least common)
```

### Input Controls

**Words to Draw**: How many words to randomly select from your loaded pool
- Default: 50 words
- Range: 1 to the total words loaded

**FROM MOST FREQ**: How many total words to load (starting from most frequent)
- Default: 3,000 words
- Range: 500 to 30,000 words

### Example Usage

| FROM MOST FREQ | Files Loaded | Vocabulary Level | Best For |
|----------------|--------------|------------------|----------|
| 500 | hw01.txt (partial) | Beginner basics | Absolute starters |
| 3,000 | hw01.txt (full) | Conversational | Daily conversations |
| 10,000 | hw01-hw04.txt | Advanced | Professional/academic |
| 30,000 | hw01-hw10.txt | Comprehensive | Near-complete vocabulary |

## Using the App

1. **Set your parameters**: Adjust "Words to Draw" and "FROM MOST FREQ"
2. **Click "Draw"**: Randomly selects words from your specified frequency range
3. **Copy words**: Click "Copy Words" for comma-separated list
4. **Copy prompt**: Click "Copy Prompt" for AI-generated learning exercises

The learning prompt creates Hindi paragraphs with your selected words, complete with:
- Hindi paragraphs (~30 words each)
- English translations
- Grammar explanations
- Alternative usage examples

## Deployment

### GitHub Pages

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`, folder: `/ (root)`
   - Click Save

3. **Access your site**:
   ```
   https://YOUR_USERNAME.github.io/think-hindi/
   ```

### Other Static Hosting

Works with any static hosting service:
- Netlify
- Vercel
- Cloudflare Pages
- Surge.sh

Simply upload the entire folder and set `index.html` as the entry point.

## Browser Compatibility

Works in all modern browsers with JavaScript enabled:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Project Structure

```
think-hindi/
├── index.html       # Self-contained app (HTML + CSS + JS)
├── favicon.svg     # Site icon
├── README.md       # This file
└── .gitignore      # Git ignore rules
```

## Word Data Source

Words are fetched from: `https://qyct.github.io/freq-hindi/words/`

Based on the [FrequencyWords](https://github.com/hermitdave/FrequencyWords) project — Hindi words ranked by usage frequency in everyday language.

## Customization

### Adjust Default Values

Edit `index.html` to change defaults:

```html
<!-- Words to Draw default -->
<input type="number" id="wordCount" value="50">

<!-- FROM MOST FREQ default -->
<input type="number" id="totalWords" value="3000">
```

### Modify Learning Prompt

Edit `index.html`, find the `renderWords()` method in the `<script>` section and modify the `this.promptText.value` line.

## Browser Compatibility

Requires JavaScript and fetch API support. Works offline after first load (files may be cached).

## License

This project is open source and available under the MIT License.

## Credits

- **Word Data**: [FrequencyWords Project](https://github.com/hermitdave/FrequencyWords) by hermitdave
- **Hosted Files**: [qyct/freq-hindi](https://github.com/qyct/freq-hindi) GitHub repository

---

Made with ❤️ for Hindi language learners

**Last Updated**: 2026-04-15
**Version**: 4.0 (Single-file edition)
**Total Vocabulary**: Up to 30,000 frequency-ordered Hindi words
