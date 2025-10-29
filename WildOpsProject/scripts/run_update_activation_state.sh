#!/bin/bash

# Get the base directory (two levels up from the current script directory)
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Activate the virtual environment
source "$BASE_DIR/WildOpsProject/wildops_venv/bin/activate"

# Navigate to the project directory
cd "$BASE_DIR"

# Ensure the logs directory exists
mkdir -p "$BASE_DIR/WildOpsProject/scripts/logs"

# Run the Django management command and log the output
python3 WildOpsProject/manage.py update_activation_state >> "$BASE_DIR/WildOpsProject/scripts/logs/update_activation_state.log" 2>&1