detect_dab() {
    source "${DAB_DETECTION_FOLDER}venv/bin/activate"
    pip install -r "$DAB_DETECTION_REQUIREMENTS_FILE"
    python "$DAB_DETECTION_SCRIPT"
    deactivate
}