play_sound() {
    if [ -f "$1" ]; then
        afplay "$1" || echo "Error playing sound file: $1"
    else
        echo "Sound file not found: $1"
    fi
}