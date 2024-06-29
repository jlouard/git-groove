import cv2
import tkinter as tk
from tkinter import *
import mediapipe as mp
from PIL import Image, ImageTk
import threading
from tkinter import filedialog
from utils.angle_between_lines import angle_between_lines

class DabMoveDetection:
    def __init__(self, master, video_path, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        
        self.master = master
        self.count1 = False
        self.count2 = False
        self.count3 = False
        self.count4 = False
        self.dab_detected = False
        self.c1, self.c2, self.c3, self.c4 = 0, 0, 0, 0

        self.cap = cv2.VideoCapture(video_path)
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=min_detection_confidence, 
            min_tracking_confidence=min_tracking_confidence
            )
        
        # title on canvas
        self.master = master
        self.master.title("Please DAB to push your work")
        #  creation of canvas with dimensions 
        self.canvas = tk.Canvas(self.master, width=640, height=480, bg="black")
        self.canvas.pack()
        #  title on left upper corner
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.LEFT)
        # self.button_frame.configure(bg="blue")
        
        #  Add the following line to create a new label to show the leg lift count
        self.dab_detected_label = tk.Label(self.master, text=f"Incorrect Dab Move", fg="red", font=("Arial Black", 20, "bold"))
        self.dab_detected_label.place(x=420, y=240, anchor='ne') 
        self.DabMove_image = None
        self.video_running = True
        self.video_detection()
          
    
    # function for pose detection ***********************************************************************************************************

    def quit(self):
        self.running = False
        self.master.quit()

    def is_dab_correct(self):
        if self.c1 and self.c2  and self.c4 and self.c3:
            return False
        return self.count1 and self.count2 and self.count3 and self.count4

    def detect_pose(self, results):
        if results.pose_landmarks:
        
        
            # Get the coordinates of the left hip and right hip
            left_shoulder = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_SHOULDER]

            
            # angle1 between left parts points 11, 13, 15
            # left_shoulder = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_SHOULDER]
            left_elbow = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_ELBOW]
            left_wrist = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_WRIST]
            
            
            if results.pose_landmarks is not None:
                angle1 = abs(angle_between_lines(left_shoulder.x, left_shoulder.y, left_elbow.x, left_elbow.y, left_wrist.x, left_wrist.y))
            else:
                angle1=0
            
            # angle2 between left parts points 23, 11, 13
            left_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_HIP]
            
            if results.pose_landmarks is not None:
                angle2 = abs(angle_between_lines(left_hip.x, left_hip.y,left_shoulder.x, left_shoulder.y, left_elbow.x, left_elbow.y))
            else:
                angle2=0

            # angle3 between left parts points 24, 12, 14
            right_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_HIP]
            right_elbow = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_ELBOW]
            
            if results.pose_landmarks is not None:
                angle3 = abs(angle_between_lines(right_hip.x, right_hip.y, right_shoulder.x, right_shoulder.y, right_elbow.x, right_elbow.y))
            else:
                angle3=0

            # angle4 between left parts points 24, 12, 14
            right_wrist = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST]
            
            if results.pose_landmarks is not None:
                angle4 = abs(angle_between_lines(right_shoulder.x, right_shoulder.y, right_elbow.x, right_elbow.y, right_wrist.x, right_wrist.y))
            else:
                angle4=0
            if (angle1 > 0 and angle1 <= 45):
                self.count1 = True
            else:
                self.count1 = False
            if (60< angle2 < 155):
                self.count2 = True
            else:
                self.count2 = False
            if (angle3 > 75 and angle3 < 145):
                self.count3 = True
            else:
                self.count3 = False
            if (angle4 > 0 and angle4 < 30):
                self.count4 = True
            else:
                self.count4 = False
            
            if self.is_dab_correct():
                self.dab_detected = True

            if self.dab_detected:
                self.dab_detected_label.config(text="Wow, what a DAB !", fg="green")
                self.master.after(2000, self.quit)
                    
            self.c1=self.count1
            self.c2=self.count2
            self.c3=self.count3
            self.c4=self.count4
        
        
    def video_detection(self):
        ret, frame = self.cap.read()
            
        if ret:
            # Convert the image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Make a detection
            results = self.holistic.process(image)

            # Draw the detection points on the image
            annotated_image = image.copy()
            self.mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)

            self.detect_pose(results)
            Bally_Button = self.Bally_Button(results)
            
            # Draw a circle at the Bally_Button
            if Bally_Button:
                cv2.circle(annotated_image, (int(Bally_Button[0] * annotated_image.shape[1]), int(Bally_Button[1] * annotated_image.shape[0])), 5, (255, 0, 0), -1)

            # # Show the annotated image
            # Resize the image to match the size of the canvas
            resized_image = cv2.resize(annotated_image, (640, 480))
            self.leg_lift_image = ImageTk.PhotoImage(Image.fromarray(resized_image))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.leg_lift_image)
        
            # Exit if the user presses the 'q' key
        if self.video_running:
            self.master.after(50, self.video_detection)

        # Release the webcam and close the window
    def __del__(self):
            self.cap.release()
            cv2.destroyAllWindows()
    

    def Bally_Button(self, results):
        if results.pose_landmarks:
            left_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_HIP]
            midpoint = ((left_hip.x + right_hip.x) / 2, (left_hip.y + right_hip.y) / 2)
            distance_from_hip= (abs(midpoint[0]-left_hip.x), abs(midpoint[1] - left_hip.y))
            bally_button=(midpoint[0], (midpoint[1] - distance_from_hip[0])-distance_from_hip[0])
            return bally_button
        
    
