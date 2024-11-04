import mediapipe as mp
import cv2

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