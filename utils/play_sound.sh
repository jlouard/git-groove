play_sound() {
    for arg in "$@"; do
        if [ "$arg" = "--no-sound" ]; then
            return 0
        fi
    done

    if [ -f "$1" ]; then
        afplay "$1" || echo "Error playing sound file: $1"
    else
        echo "Sound file not found: $1"
    fi
}