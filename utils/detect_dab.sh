#!/bin/bash

detect_dab() {
    VENV_DIR="${DAB_DETECTION_FOLDER}venv"
    REQUIREMENTS_FILE="${DAB_DETECTION_FOLDER}requirements.txt"
    SCRIPT="${DAB_DETECTION_FOLDER}main.py"

    # Check if the venv directory exists
    if [ ! -d "$VENV_DIR" ]; then
        echo "Virtual environment not found. Creating one..."
        python3 -m venv "$VENV_DIR"
    fi

    source "$VENV_DIR/bin/activate"

    requirements_installed() {
        pip freeze | grep -F -xf "$REQUIREMENTS_FILE" > /dev/null
    }

    if requirements_installed; then
        echo "All requirements are already installed."
    else
        echo "Installing requirements..."
        pip install -r "$REQUIREMENTS_FILE"
    fi

    python3 "$SCRIPT"
    deactivate
}