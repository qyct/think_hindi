#!/bin/bash
# Helper script to run Python scripts with the ~/PYENV virtual environment

# Activate the virtual environment
source ~/PYENV/bin/activate

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Run the requested script or Python command
if [ $# -eq 0 ]; then
    # No arguments: show help
    echo "Hindi Words Compiler - Run with PYENV"
    echo ""
    echo "Usage: ./scripts/run_with_pyenv.sh <command> [args]"
    echo ""
    echo "Examples:"
    echo "  ./scripts/run_with_pyenv.sh python scripts/compile_hindi_words.py"
    echo "  ./scripts/run_with_pyenv.sh python scripts/advanced_compile.py"
    echo "  ./scripts/run_with_pyenv.sh python scripts/advanced_compile.py --real-data"
    echo "  ./scripts/run_with_pyenv.sh pip list"
else
    # Execute the command with arguments
    "$@"
fi
