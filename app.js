class HindiWordsApp {
    constructor() {
        this.allWords = [];
        this.currentWords = [];
        this.init();
    }

    async init() {
        this.cacheDOM();
        this.bindEvents();
        await this.loadAllWords();
    }

    cacheDOM() {
        this.wordCountInput = document.getElementById('wordCount');
        this.randomBtn = document.getElementById('randomBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.wordsContainer = document.getElementById('wordsContainer');
    }

    bindEvents() {
        this.randomBtn.addEventListener('click', () => this.displayRandomWords());
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        this.wordCountInput.addEventListener('change', () => this.validateInput());
    }

    validateInput() {
        let value = parseInt(this.wordCountInput.value);
        if (value < 1) this.wordCountInput.value = 1;
        if (value > 1000) this.wordCountInput.value = 1000;
    }

    async loadAllWords() {
        try {
            // Load words from the merged word file
            const response = await fetch('thraw/thraw.txt');

            if (!response.ok) {
                throw new Error('Failed to load words');
            }

            const text = await response.text();
            this.allWords = text.split('\n').map(word => word.trim()).filter(word => word.length > 0);

            console.log(`Loaded ${this.allWords.length} unique Hindi words`);
        } catch (error) {
            console.error('Error loading words:', error);
            this.wordsContainer.innerHTML = '<div class="error">Failed to load words. Please refresh the page.</div>';
        }
    }

    displayRandomWords() {
        if (this.allWords.length === 0) {
            this.wordsContainer.innerHTML = '<div class="error">No words loaded yet. Please wait.</div>';
            return;
        }

        const count = Math.min(parseInt(this.wordCountInput.value), this.allWords.length);
        this.currentWords = this.getRandomWords(count);
        this.renderWords();
    }

    getRandomWords(count) {
        const shuffled = [...this.allWords].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, count);
    }

    copyToClipboard() {
        if (this.currentWords.length === 0) {
            this.showCopyFeedback('No words to copy!', false);
            return;
        }

        const commaSeparatedWords = this.currentWords.join(', ');

        navigator.clipboard.writeText(commaSeparatedWords).then(() => {
            this.showCopyFeedback('Copied to clipboard!', true);
        }).catch(err => {
            console.error('Failed to copy:', err);
            this.showCopyFeedback('Failed to copy', false);
        });
    }

    showCopyFeedback(message, success) {
        const originalText = this.copyBtn.innerHTML;
        this.copyBtn.innerHTML = `<span>${success ? '✓' : '✗'}</span> ${message}`;
        this.copyBtn.classList.add(success ? 'success' : 'error');

        setTimeout(() => {
            this.copyBtn.innerHTML = originalText;
            this.copyBtn.classList.remove('success', 'error');
        }, 2000);
    }

    renderWords() {
        if (this.currentWords.length === 0) {
            this.wordsContainer.innerHTML = '<div class="placeholder">Click "Random Words" to display Hindi words</div>';
            return;
        }

        // Display words as comma-separated single rows
        const wordsText = this.currentWords.join(', ');
        this.wordsContainer.innerHTML = `<div class="words-text">${this.escapeHtml(wordsText)}</div>`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new HindiWordsApp();
});
