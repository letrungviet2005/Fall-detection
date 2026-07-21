import cv2
import numpy as np
from pathlib import Path

from detectors.person_detector import PersonDetector
from detectors.pose_detector import PoseDetector
from detectors.fall_detector import FallDetector
from analyzers.motion_analyzer import MotionAnalyzer
from ui.dashboard import Dashboard

# ===================================
# CONFIG
# ===================================
BASE_DIR = Path(__file__).resolve().parent
VIDEO_PATH = BASE_DIR / "videos" / "fall5.mp4"

print(f"Loading video: {VIDEO_PATH}")

video = cv2.VideoCapture(str(VIDEO_PATH))

if not video.isOpened():
    print(f"Không mở được video: {VIDEO_PATH}")
    exit()

# ===================================
# INIT
# ===================================
person_detector = PersonDetector()
pose_detector = PoseDetector()
fall_detector = FallDetector()
motion_analyzer = MotionAnalyzer()
dashboard = Dashboard()


while True:

    ret, frame = video.read()

    if not ret:
        break


    body_angle = "--"
    pose_status = "Not Found"

    motion = {
        "distance": 0,
        "velocity": 0,
        "still": False
    }

    fall_score = 0
    status = "NORMAL"
    confidence = 0


    persons = person_detector.detect(frame)

    pose_result = pose_detector.detect(frame)

    if pose_result.pose_landmarks:

        pose_status = "Detected"

        pose_detector.drawer.draw_landmarks(
            frame,
            pose_result.pose_landmarks,
            pose_detector.mp_pose.POSE_CONNECTIONS
        )

        landmarks = pose_result.pose_landmarks.landmark


        body_angle = fall_detector.body_angle(landmarks)
        left_hip = landmarks[
            pose_detector.mp_pose.PoseLandmark.LEFT_HIP
        ]

        right_hip = landmarks[
            pose_detector.mp_pose.PoseLandmark.RIGHT_HIP
        ]

        hip_x = (left_hip.x + right_hip.x) / 2
        hip_y = (left_hip.y + right_hip.y) / 2

        motion = motion_analyzer.update(
            hip_x,
            hip_y
        )

    # ===================================
    # FALL DETECTION
    # ===================================
    if len(persons) > 0 and body_angle != "--":

        confidence = max(
            p["conf"] for p in persons
        )

        bbox = persons[0]["bbox"]

        result = fall_detector.detect(
            body_angle,
            bbox,
            motion
        )

        fall_score = result["score"]
        status = result["state"]

    # ===================================
    # DRAW PERSON
    # ===================================
    for p in persons:

        x1, y1, x2, y2 = p["bbox"]

        if status == "FALL DETECTED":
            color = (0, 0, 255)

        elif status in ["FALLING", "LYING"]:
            color = (0, 255, 255)

        else:
            color = (0, 255, 0)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cv2.putText(
            frame,
            f"{p['conf']:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # ===================================
    # DASHBOARD
    # ===================================
    info = {
        "Person": len(persons),
        "Confidence": f"{confidence * 100:.1f} %",
        "Pose": pose_status,
        "Body Angle": "--" if body_angle == "--" else f"{body_angle:.1f}°",
        "Velocity": f"{motion['velocity']:.4f}",
        "Still": motion["still"],
        "Fall Score": f"{fall_score}",
        "Status": status
    }

    panel = dashboard.draw(info)
    panel = cv2.resize(panel, (350, frame.shape[0]))

    display = np.hstack((frame, panel))

    cv2.imshow("OmniCare AI", display)

    key = cv2.waitKey(1)

    if key == 27:
        break

video.release()
cv2.destroyAllWindows()