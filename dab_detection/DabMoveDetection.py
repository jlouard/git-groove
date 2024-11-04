import cv2
import tkinter as tk
from tkinter import filedialog
import mediapipe as mp
from PIL import Image, ImageTk
import warnings

from utils.angle_between_lines import angle_between_lines

warnings.filterwarnings("ignore", category=UserWarning)


class DabMoveDetection:
    def __init__(self, master, video_path, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.master = master
        self.cap = cv2.VideoCapture(video_path)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose  # Import Pose separately
        self.holistic = mp.solutions.holistic.Holistic(
            min_detection_confidence=min_detection_confidence, 
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.setup_ui()
        self.dab_detected = False
        self.video_running = True
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

    def is_dab_correct(self, conditions):
        return all(conditions)

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

    def detect_pose(self, results):
        if results.pose_landmarks:
            angles = self.calculate_angles(results.pose_landmarks.landmark)
            conditions = [
                0 < angles[0] <= 45,     # Left arm angle
                60 < angles[1] < 155,    # Left shoulder angle
                75 < angles[2] < 145,    # Right shoulder angle
                0 < angles[3] < 30       # Right arm angle
            ]

            if self.is_dab_correct(conditions):
                self.dab_detected = True
                self.dab_label.config(text="Wow, what a DAB!", fg="green")
                self.master.after(2000, self.quit)

    def video_detection(self):
        if not self.video_running:
            return

        ret, frame = self.cap.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.holistic.process(image)

            annotated_image = image.copy()
            self.mp_drawing.draw_landmarks(
                annotated_image, 
                results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS
            )

            self.detect_pose(results)

            resized_image = cv2.resize(annotated_image, (640, 480))
            self.annotated_image = ImageTk.PhotoImage(Image.fromarray(resized_image))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.annotated_image)

        self.master.after(50, self.video_detection)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
