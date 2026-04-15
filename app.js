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
        this.totalWordsInput = document.getElementById('totalWords');
        this.randomBtn = document.getElementById('randomBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.copyPromptBtn = document.getElementById('copyPromptBtn');
        this.wordsContainer = document.getElementById('wordsContainer');
        this.promptText = document.getElementById('promptText');
        this.wordCountBadge = document.getElementById('wordCountBadge');
    }

    bindEvents() {
        this.randomBtn.addEventListener('click', () => this.displayRandomWords());
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        this.copyPromptBtn.addEventListener('click', () => this.copyPromptToClipboard());
        this.wordCountInput.addEventListener('change', () => this.validateWordCount());
        this.totalWordsInput.addEventListener('change', () => this.validateTotalWords());
    }

    validateWordCount() {
        let value = parseInt(this.wordCountInput.value);
        const totalWords = parseInt(this.totalWordsInput.value);
        if (isNaN(value) || value < 1) this.wordCountInput.value = 1;
        if (value > totalWords) this.wordCountInput.value = totalWords;
    }

    validateTotalWords() {
        let value = parseInt(this.totalWordsInput.value);
        if (isNaN(value) || value < 500) this.totalWordsInput.value = 500;
        if (value > 30000) this.totalWordsInput.value = 30000;
        // Reload words when total words changes
        this.loadAllWords();
    }

    async loadAllWords() {
        try {
            const totalWordsRequested = parseInt(this.totalWordsInput.value) || 3000;

            // Calculate how many files to load (each has 3000 words)
            const filesNeeded = Math.ceil(totalWordsRequested / 3000);
            let allLoadedWords = [];

            // Load files sequentially
            for (let i = 1; i <= filesNeeded; i++) {
                const fileNum = i.toString().padStart(2, '0');
                const url = `https://qyct.github.io/freq-hindi/words/hw${fileNum}.txt`;
                const words = await this.fetchLevelWords(url);
                allLoadedWords = allLoadedWords.concat(words);
            }

            // Slice to the exact number requested
            this.allWords = allLoadedWords.slice(0, totalWordsRequested);
            this.updateWordCountBadge();

            console.log(`Loaded ${this.allWords.length} Hindi words from ${filesNeeded} file(s)`);
        } catch (error) {
            console.error('Error loading words:', error);
            this.wordsContainer.innerHTML = '<div class="error-msg">Failed to load words. Please refresh the page.</div>';
        }
    }

    async fetchLevelWords(url) {
        try {
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Failed to load words`);
            }

            const text = await response.text();
            const lines = text.split('\n').filter(line => line.trim().length > 0);

            // Parse word,frequency format
            const wordsWithFreq = lines.map(line => {
                const parts = line.split(',');
                return parts[0].trim();
            }).filter(word => word.length > 0);

            return wordsWithFreq;
        } catch (error) {
            console.error(`Error fetching words:`, error);
            return [];
        }
    }

    updateWordCountBadge() {
        if (this.wordCountBadge) {
            this.wordCountBadge.textContent = `${this.allWords.length.toLocaleString()} words`;
        }
    }

    displayRandomWords() {
        if (this.allWords.length === 0) {
            this.wordsContainer.innerHTML = '<div class="error-msg">No words loaded yet. Please wait.</div>';
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

        const promptText = this.promptText.value;

        if (!promptText.trim()) {
            this.showCopyFeedback(this.copyPromptBtn, 'No prompt!', false);
            return;
        }

        navigator.clipboard.writeText(promptText).then(() => {
            this.showCopyFeedback(this.copyPromptBtn, 'Copied!', true);
        }).catch(err => {
            console.error('Failed to copy:', err);
            this.showCopyFeedback(this.copyPromptBtn, 'Failed', false);
        });
    }

    showCopyFeedback(button, message, success) {
        const originalHTML = button.innerHTML;
        const icon = success
            ? `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`
            : `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;

        button.innerHTML = `${icon} ${message}`;
        button.classList.add(success ? 'success' : 'error');

        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.classList.remove('success', 'error');
        }, 2000);
    }

    generateLearningPrompt(words) {
        const wordList = words.join(', ');
        return `${wordList}

Using these words, create meaningful paragraphs in Hindi with around 30 words, each can have multiple sentences, that help understand their usage in everyday conversations. Explain the meaning of each sentence of paragraphs in English, highlight grammar points, and suggest alternative ways to use these words naturally. Make it engaging so that one can practice speaking, reading, and writing Hindi.`;
    }

    renderWords() {
        if (this.currentWords.length === 0) {
            this.wordsContainer.innerHTML = '<div class="placeholder">Draw words to begin</div>';
            this.wordsContainer.classList.remove('has-words');
            this.promptText.value = '';
            return;
        }

        const wordsText = this.currentWords.join(', ');
        this.wordsContainer.innerHTML = `<div class="words-text">${this.escapeHtml(wordsText)}</div>`;
        this.wordsContainer.classList.add('has-words');

        const learningPrompt = this.generateLearningPrompt(this.currentWords);
        this.promptText.value = learningPrompt;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new HindiWordsApp();
});
