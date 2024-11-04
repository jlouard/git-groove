from utils.angle_between_lines import angle_between_lines

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
