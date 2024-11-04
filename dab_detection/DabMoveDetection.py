import cv2
import tkinter as tk
import mediapipe as mp
from PIL import Image, ImageTk, ImageSequence
import warnings
from utils.angle_between_lines import angle_between_lines

warnings.filterwarnings("ignore", category=UserWarning)

class VideoCapture:
    def __init__(self, video_path, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.cap = cv2.VideoCapture(video_path)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.holistic = mp.solutions.holistic.Holistic(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def read_frame(self):
        """Capture and process a single frame from the video feed."""
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return image, self.holistic.process(image)

    def draw_landmarks(self, image, results):
        """Draw pose landmarks on the image if detected."""
        annotated_image = image.copy()
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )
        return annotated_image

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


class PoseAnalyzer:
    def __init__(self, mp_pose):
        self.mp_pose = mp_pose
        
    def calculate_angles(self, landmarks):
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]

        angle1 = abs(angle_between_lines(left_shoulder.x, left_shoulder.y, left_elbow.x, left_elbow.y, left_wrist.x, left_wrist.y))
        angle2 = abs(angle_between_lines(left_hip.x, left_hip.y, left_shoulder.x, left_shoulder.y, left_elbow.x, left_elbow.y))
        angle3 = abs(angle_between_lines(right_hip.x, right_hip.y, right_shoulder.x, right_shoulder.y, right_elbow.x, right_elbow.y))
        angle4 = abs(angle_between_lines(right_shoulder.x, right_shoulder.y, right_elbow.x, right_elbow.y, right_wrist.x, right_wrist.y))
        
        return [angle1, angle2, angle3, angle4]

    def is_dab_pose(self, landmarks):
        if not landmarks:
            return False
            
        angles = self.calculate_angles(landmarks)
        conditions = [
            0 < angles[0] <= 45,     # Left arm angle
            60 < angles[1] < 155,    # Left shoulder angle
            75 < angles[2] < 145,    # Right shoulder angle
            0 < angles[3] < 30       # Right arm angle
        ]
        return all(conditions)


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


class DabMoveDetection:
    def __init__(self, master, video_path, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.master = master
        self.video_capture = VideoCapture(video_path, min_detection_confidence, min_tracking_confidence)
        self.pose_analyzer = PoseAnalyzer(self.video_capture.mp_pose)
        
        self.setup_ui()
        self.animation_manager = AnimationManager(self.canvas, "fireworks.gif")
        
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
