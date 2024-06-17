#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to folders
ROOT_FOLDER="$SCRIPT_DIR/"
UTILS_FOLDER="${ROOT_FOLDER}utils/"
SOUNDS_FOLDER="${ROOT_FOLDER}sounds/"
ANIMATIONS_FOLDER="${ROOT_FOLDER}animations/"
DAB_DETECTION_FOLDER="${ROOT_FOLDER}dab_detection/"
IMAGES_FOLDER="${ROOT_FOLDER}dab_detection/"

# Source utility 
source "$UTILS_FOLDER/play_sound.sh"
source "$UTILS_FOLDER/display_ascii.sh"
source "$UTILS_FOLDER/display_animation.sh"
source "$UTILS_FOLDER/detect_dab.sh"

# Path to sound files
PULL_SOUND="${SOUNDS_FOLDER}poule.mp3"
POP_SOUND="${SOUNDS_FOLDER}pop.mp3"

# Animation variables
PULL_FRAME_DELAY=0.3  # Delay between frames in seconds
STASH_FRAME_DELAY=0.05  # Delay between frames in seconds
REPEAT_COUNT=1

case "$1 $2" in
    "stash pop"*)
        git "$@"
        play_sound "$POP_SOUND"
        ;;
    "push dab"*)
        detect_dab
        git "$@"
        ;;
    "poule"*)
        git pull
        GIT_PULL_STATUS=$?
        if [ $GIT_PULL_STATUS -eq 0 ]; then
            display_animation "$ANIMATIONS_FOLDER/poule" $REPEAT_COUNT $PULL_FRAME_DELAY & 
            play_sound "$PULL_SOUND" &
        else
            display_animation "$ANIMATIONS_FOLDER/poulet" $REPEAT_COUNT $PULL_FRAME_DELAY &
        fi
        wait
        ;;
    "stache"*)
        display_animation "$ANIMATIONS_FOLDER/moustache" $REPEAT_COUNT $STASH_FRAME_DELAY
        git stash
        ;;
    "pooulet"*)
        display_animation "$ANIMATIONS_FOLDER/poulet" $REPEAT_COUNT $PULL_FRAME_DELAY
        ;;
    *)
        git "$@"
        ;;
esac
