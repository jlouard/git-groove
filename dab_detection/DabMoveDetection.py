import cv2
import tkinter as tk
import warnings
from PIL import Image, ImageTk
import os

from VideoCapture import VideoCapture
from PoseAnalyzer import PoseAnalyzer
from AnimationManager import AnimationManager

warnings.filterwarnings("ignore", category=UserWarning)

class DabMoveDetection:
    def __init__(self, master, video_path, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.master = master
        self.video_capture = VideoCapture(video_path, min_detection_confidence, min_tracking_confidence)
        self.pose_analyzer = PoseAnalyzer(self.video_capture.mp_pose)
        
        self.setup_ui()
        animation_path = os.path.join(os.path.dirname(__file__), "fireworks.gif")
        self.animation_manager = AnimationManager(self.canvas, animation_path)
        
        self.dab_detected = False
        self.video_running = True
        self.dab_detected_time = None
        self.master.after(50, self.video_detection)

    def setup_ui(self):
        self.master.title("Please DAB to push your work")
        self.canvas = tk.Canvas(self.master, width=640, height=480, bg="black")
        self.canvas.pack()
        self.dab_label = tk.Label(self.master, text="Incorrect Dab Move", fg="red", font=("Arial Black", 20, "bold"))
        self.dab_label.place(x=420, y=240, anchor='ne')

    def quit(self):
        self.video_running = False
        self.master.quit()
        self.master.destroy()

    def _prepare_display_image(self, image, results):
        annotated_image = self.video_capture.draw_landmarks(image, results)
        base_image = Image.fromarray(cv2.resize(annotated_image, (640, 480))).convert("RGBA")
        
        if self.dab_detected:
            animation_frame = self.animation_manager.get_next_frame()
            if animation_frame:
                base_image = Image.alpha_composite(base_image, animation_frame.convert("RGBA"))
        
        return base_image

    def video_detection(self):
        if not self.video_running:
            return

        image, results = self.video_capture.read_frame()
        if image is None:
            return

        if results.pose_landmarks and self.pose_analyzer.is_dab_pose(results.pose_landmarks.landmark):
            if not self.dab_detected:
                self.dab_detected = True
                self.dab_detected_time = self.master.after(5000, self.quit)
                self.dab_label.config(text="Wow, what a DAB!", fg="green")

        display_image = self._prepare_display_image(image, results)
        self.annotated_image = ImageTk.PhotoImage(display_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.annotated_image)

        self.master.after(50, self.video_detection)

    def __del__(self):
        self.video_capture.release()
