display_animation() {
    local animation_path=$1
    local repeat_count=$2
    local frame_delay=$3
    local frame_count=$(ls -1q "$animation_path"/*.txt | wc -l)

    for ((r=1; r<=repeat_count; r++)); do
        for i in $(seq 1 $frame_count); do
            clear
            while IFS= read -r line; do
                echo -e "$line"
            done < "$animation_path/frame$i.txt"
            sleep $frame_delay
        done
    done
}