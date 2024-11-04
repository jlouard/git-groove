from PIL import Image, ImageSequence

class AnimationManager:
    def __init__(self, canvas, animation_path):
        self.canvas = canvas
        self.current_frame = 0
        self.animation_frames = self._load_animation(animation_path)

    def _load_animation(self, file_path):
        background_image = Image.open(file_path)
        return [frame.copy() for frame in ImageSequence.Iterator(background_image)]

    def get_next_frame(self, size=(640, 480)):
        if not self.animation_frames:
            return None
            
        frame = self.animation_frames[self.current_frame]
        frame = frame.resize(size, Image.LANCZOS)
        self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        return frame