display_ascii() {
    if [ -f "$1" ]; then
        while IFS= read -r line; do
            echo -e "$line"
        done < "$1"
    else
        echo "ASCII art file not found: $1"
    fi
}