import cv2
import numpy as np


class Dashboard:

    def __init__(self, width=400, height=720):
        self.width = width
        self.height = height


    def draw(self, info):

        panel = np.zeros(
            (self.height, self.width, 3),
            dtype=np.uint8
        )

        panel[:] = (28, 28, 28)


        # ===========================
        # HEADER
        # ===========================

        cv2.rectangle(
            panel,
            (0,0),
            (self.width,90),
            (45,45,45),
            -1
        )


        cv2.putText(
            panel,
            "OmniCare AI",
            (20,38),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (255,255,255),
            2
        )


        cv2.putText(
            panel,
            "Smart Elderly Monitoring",
            (20,68),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (180,180,180),
            1
        )


        # ===========================
        # INFORMATION
        # ===========================

        y = 110

        max_y = self.height - 190


        for key,value in info.items():


            # tránh đè alert box
            if y > max_y:
                break


            cv2.rectangle(
                panel,
                (15,y),
                (385,y+40),
                (45,45,45),
                -1
            )


            cv2.putText(
                panel,
                key,
                (28,y+26),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (170,170,170),
                1
            )


            color = (255,255,255)


            # STATUS COLOR

            if key == "Status":

                if value == "FALL DETECTED":
                    color=(0,0,255)

                elif value in [
                    "WARNING",
                    "FALLING",
                    "LYING"
                ]:
                    color=(0,255,255)

                else:
                    color=(0,255,0)



            # POSE COLOR

            elif key == "Pose":

                if value=="Detected":
                    color=(0,255,0)

                else:
                    color=(0,0,255)



            # FALL SCORE COLOR

            elif key=="Fall Score":

                try:

                    score=int(
                        float(
                            str(value)
                            .replace("%","")
                        )
                    )

                    if score>=80:
                        color=(0,0,255)

                    elif score>=50:
                        color=(0,255,255)

                    else:
                        color=(0,255,0)

                except:
                    pass



            cv2.putText(
                panel,
                str(value),
                (220,y+26),
                cv2.FONT_HERSHEY_DUPLEX,
                0.65,
                color,
                2
            )


            y += 48



        # ===========================
        # ALERT BOX
        # ===========================

        status = info.get(
            "Status",
            "NORMAL"
        )


        if status=="FALL DETECTED":

            alert_color=(0,0,180)
            text="EMERGENCY"


        elif status in [
            "FALLING",
            "LYING",
            "WARNING"
        ]:

            alert_color=(0,180,255)
            text="WARNING"


        else:

            alert_color=(0,120,0)
            text="SAFE"



        cv2.rectangle(
            panel,
            (20,self.height-130),
            (380,self.height-65),
            alert_color,
            -1
        )


        cv2.putText(
            panel,
            text,
            (95,self.height-88),
            cv2.FONT_HERSHEY_DUPLEX,
            1.1,
            (255,255,255),
            2
        )



        # ===========================
        # FOOTER
        # ===========================

        cv2.line(
            panel,
            (15,self.height-45),
            (385,self.height-45),
            (80,80,80),
            1
        )


        cv2.putText(
            panel,
            "VKU Hackathon 2026",
            (20,self.height-18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (170,170,170),
            1
        )


        return panel