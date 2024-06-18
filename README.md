# Git Groove
## Bring Some Groove to Your Git Commands
Are you tired of the same old git commands every day? Add some fun to your development workflow with Git Groove! This script plays sounds and displays ASCII art animations every time you run specific git commands.

## Features
- Custom Sounds: Play specific sounds for git push, git pull, and more.
- ASCII Art Animations: Display colorful ASCII art animations for various git commands.
- Configurable: Easily configure and customize the sounds and animations for different commands.

## Getting Started
Follow these steps to set up Git Groove on your machine.

Prerequisites
- macOS
- Git
- Terminal
- Python3 (only for dab detection)

## Installation

1. Clone the Repository
```
git clone https://github.com/yourusername/git-groove.git
cd git-groove
```

2. Make the Script Executable
```
chmod +x git-sound.sh
```

3. Add an Alias to Your Shell Configuration
Add the following line to your .bashrc or .zshrc file to use the script for git commands:
```
alias git='/path/to/your/git-sound.sh'
```
Replace /path/to/your/git-sound.sh with the actual path to your git-sound.sh script.

4. Reload Your Shell Configuration
```
source ~/.bashrc  # or ~/.zshrc
```

## Configuration
### Sounds
Place your sound files in the sounds directory. Configure the paths to your sound files in the script if necessary.

### ASCII Art Images
Place your ASCII art images in the images directory. Configure the paths to your images files in the script if necessary.

### ASCII Art Animations
Place your ASCII art frames in separate directories under animations. Each frame should be a .txt file, and frames should be named sequentially (e.g., frame1.txt, frame2.txt, etc.).

Directory structure example:

````
animations/
  ├── commit_animation/
  │   ├── frame1.txt
  │   ├── frame2.txt
  │   └── ...
  ├── push_animation/
  │   ├── frame1.txt
  │   ├── frame2.txt
  │   └── ...
  ├── pull_animation/
  │   ├── frame1.txt
  │   ├── frame2.txt
  │   └── ...
  └── stash_pop_animation/
      ├── frame1.txt
      ├── frame2.txt
      └── ...
````

## Usage
Once everything is set up, use your git commands as usual. The script will automatically play the sounds and display animations for the configured commands.

## Contributing
We welcome contributions! 

## Acknowledgments
Thanks to the contributors and the open-source community for their support.

Thanks to MuhammadTayyab777 for his awesome contribution on dab detection. See his code here : https://github.com/MuhammadTayyab777/Posedetector_python_mediapipe_solution.

Enjoy your new groovy git experience! If you have any issues or suggestions, please open an issue or submit a pull request.
