from collections import deque
import math


class MotionAnalyzer:

    def __init__(self, history=15):

        self.history = deque(maxlen=history)

    def update(self, x, y):

        self.history.append((x, y))

        if len(self.history) < 2:
            return {
                "distance": 0,
                "velocity": 0,
                "still": False
            }

        x0, y0 = self.history[-2]
        x1, y1 = self.history[-1]

        distance = math.sqrt(
            (x1 - x0) ** 2 +
            (y1 - y0) ** 2
        )

        velocity = distance

        still = velocity < 0.003

        return {
            "distance": distance,
            "velocity": velocity,
            "still": still
        }