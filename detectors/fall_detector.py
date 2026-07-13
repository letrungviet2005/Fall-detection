import math
import mediapipe as mp
from collections import deque
import time


class FallDetector:

    def __init__(self):

        self.pose = mp.solutions.pose

        # lưu 15 frame gần nhất
        self.angle_history = deque(maxlen=15)

        self.state = "NORMAL"

        self.lying_start = None

    # =======================================
    # Body Angle
    # =======================================

    def body_angle(self, landmarks):

        ls = landmarks[self.pose.PoseLandmark.LEFT_SHOULDER]
        rs = landmarks[self.pose.PoseLandmark.RIGHT_SHOULDER]

        lh = landmarks[self.pose.PoseLandmark.LEFT_HIP]
        rh = landmarks[self.pose.PoseLandmark.RIGHT_HIP]

        sx = (ls.x + rs.x) / 2
        sy = (ls.y + rs.y) / 2

        hx = (lh.x + rh.x) / 2
        hy = (lh.y + rh.y) / 2

        dx = sx - hx
        dy = sy - hy

        angle = abs(math.degrees(math.atan2(dx, dy)))

        return angle

    # =======================================
    # Main
    # =======================================

    def detect(self, angle, bbox, motion):

        self.angle_history.append(angle)

        score = 0

        # -----------------------
        # BODY ANGLE
        # -----------------------

        if angle > 75:
            score += 40

        elif angle > 60:
            score += 25

        elif angle > 45:
            score += 10

        # -----------------------
        # ANGLE CHANGE
        # -----------------------

        angle_speed = 0

        if len(self.angle_history) >= 5:

            angle_speed = abs(
                self.angle_history[-1] -
                self.angle_history[0]
            )

        if angle_speed > 35:
            score += 25

        # -----------------------
        # BBOX RATIO
        # -----------------------

        x1, y1, x2, y2 = bbox

        w = x2 - x1
        h = y2 - y1

        ratio = w / (h + 1e-6)

        if ratio > 1.2:
            score += 20

        elif ratio > 1:
            score += 10

        # -----------------------
        # STILL
        # -----------------------

        if motion["still"]:
            score += 15

        score = min(score, 100)

        # =====================================
        # STATE MACHINE
        # =====================================

        # NORMAL

        if self.state == "NORMAL":

            if angle_speed > 35:

                self.state = "FALLING"

        # FALLING

        elif self.state == "FALLING":

            if angle > 70:

                self.state = "LYING"

                self.lying_start = time.time()

            else:

                self.state = "NORMAL"

        # LYING

        elif self.state == "LYING":

            if not motion["still"]:

                self.state = "NORMAL"

                self.lying_start = None

            else:

                lying_time = time.time() - self.lying_start

                if lying_time >= 3:

                    self.state = "FALL DETECTED"

        # FALL DETECTED

        elif self.state == "FALL DETECTED":

            pass

        return {

            "score": score,

            "state": self.state,

            "angle_speed": round(angle_speed, 2),

            "ratio": round(ratio, 2)

        }