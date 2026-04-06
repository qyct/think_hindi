#!/bin/bash
# Test script to verify the web app works

echo "Testing Hindi Words Web App..."
echo ""

# Activate virtual environment
source ~/PYENV/bin/activate

# Check if required word files exist
echo "1. Checking word files..."
if [ -d "thraw" ]; then
    word_files=$(ls -1 thraw/words_*.txt 2>/dev/null | wc -l)
    echo "   ✓ Found $word_files word files in thraw/"
else
    echo "   ✗ thraw/ directory not found"
fi

# Check HTML, CSS, JS files
echo ""
echo "2. Checking web app files..."
for file in index.html app.js styles.css; do
    if [ -f "$file" ]; then
        echo "   ✓ $file exists"
    else
        echo "   ✗ $file missing"
    fi
done

# Start HTTP server
echo ""
echo "3. Starting HTTP server on http://localhost:8000"
echo "   Press Ctrl+C to stop the server"
echo ""

python -m http.server 8000
