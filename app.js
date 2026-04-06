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
        this.copyPromptBtn = document.getElementById('copyPromptBtn');
        this.wordsContainer = document.getElementById('wordsContainer');
        this.promptText = document.getElementById('promptText');
    }

    bindEvents() {
        this.randomBtn.addEventListener('click', () => this.displayRandomWords());
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        this.copyPromptBtn.addEventListener('click', () => this.copyPromptToClipboard());
        this.wordCountInput.addEventListener('change', () => this.validateInput());
    }

    validateInput() {
        let value = parseInt(this.wordCountInput.value);
        if (value < 1) this.wordCountInput.value = 1;
        if (value > 100) this.wordCountInput.value = 100;
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
            this.showCopyFeedback(this.copyBtn, 'No words to copy!', false);
            return;
        }

        const commaSeparatedWords = this.currentWords.join(', ');

        navigator.clipboard.writeText(commaSeparatedWords).then(() => {
            this.showCopyFeedback(this.copyBtn, 'Copied!', true);
        }).catch(err => {
            console.error('Failed to copy:', err);
            this.showCopyFeedback(this.copyBtn, 'Failed', false);
        });
    }

    copyPromptToClipboard() {
        if (this.currentWords.length === 0) {
            this.showCopyFeedback(this.copyPromptBtn, 'No words!', false);
            return;
        }

        // Get the text from the editable textarea
        const promptText = this.promptText.value;

        if (!promptText.trim()) {
            this.showCopyFeedback(this.copyPromptBtn, 'No prompt!', false);
            return;
        }

        navigator.clipboard.writeText(promptText).then(() => {
            this.showCopyFeedback(this.copyPromptBtn, 'Prompt copied!', true);
        }).catch(err => {
            console.error('Failed to copy:', err);
            this.showCopyFeedback(this.copyPromptBtn, 'Failed', false);
        });
    }

    showCopyFeedback(button, message, success) {
        const originalText = button.innerHTML;
        button.innerHTML = `<span>${success ? '✓' : '✗'}</span> ${message}`;
        button.classList.add(success ? 'success' : 'error');

        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('success', 'error');
        }, 2000);
    }

    generateLearningPrompt(words) {
        const wordList = words.join(', ');
        return `[Your Hindi words here] — ${wordList}

Using only these words, create meaningful sentences in Hindi that help me understand their usage in everyday conversation. Explain the meaning of each sentence in English, highlight grammar points, and suggest alternative ways to use these words naturally. Make it engaging, beginner-friendly, and progressively build complexity so I can practice speaking, reading, and writing Hindi.`;
    }

    renderWords() {
        if (this.currentWords.length === 0) {
            this.wordsContainer.innerHTML = '<div class="placeholder">Click "Random Words" to display Hindi words</div>';
            this.promptText.value = '';
            return;
        }

        // Display words as comma-separated
        const wordsText = this.currentWords.join(', ');
        this.wordsContainer.innerHTML = `<div class="words-text">${this.escapeHtml(wordsText)}</div>`;

        // Generate and update learning prompt
        const learningPrompt = this.generateLearningPrompt(this.currentWords);
        this.promptText.value = learningPrompt;
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
