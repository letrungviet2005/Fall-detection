from pathlib import Path
from ultralytics import YOLO


class PersonDetector:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent
        MODEL_PATH = BASE_DIR / "models" / "yolo11n.pt"

        self.model = YOLO(str(MODEL_PATH))

    def detect(self, frame):

        results = self.model(frame, verbose=False)

        persons = []

        for result in results:
            for box in result.boxes:

                cls = int(box.cls[0])

                # Class 0 = Person
                if cls != 0:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                persons.append({
                    "bbox": (x1, y1, x2, y2),
                    "conf": conf
                })

        return persons