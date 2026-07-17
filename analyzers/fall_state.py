from collections import deque
import time


class FallState:

    def __init__(self):

        self.state = "NORMAL"

        self.angle_history = deque(maxlen=10)

        self.start_lying = None

    def update(self, angle, movement):

        self.angle_history.append(angle)

        # -------------------------
        # NORMAL
        # -------------------------
        if self.state == "NORMAL":

            if len(self.angle_history) >= 5:

                diff = self.angle_history[-1] - self.angle_history[0]

                if diff > 40:

                    self.state = "FALLING"

        # -------------------------
        # FALLING
        # -------------------------
        elif self.state == "FALLING":

            if angle > 70:

                self.state = "LYING"

                self.start_lying = time.time()

            else:

                self.state = "NORMAL"

        # -------------------------
        # LYING
        # -------------------------
        elif self.state == "LYING":

            if movement > 0.02:

                self.state = "NORMAL"

                self.start_lying = None

            else:

                if time.time() - self.start_lying > 3:

                    self.state = "FALL"


        elif self.state == "FALL":

            pass

        return self.state