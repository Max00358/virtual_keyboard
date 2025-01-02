import math
import cv2
from time import sleep
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos    # (x, y) top-left coordinate
        self.text = text  # keyboard letter
        self.size = size  # width, height


def drawAll(frame):
    for button in button_list:
        x1, y1 = button.pos
        x2, y2 = x1 + button.size[0], y1 + button.size[1]
        cv2.rectangle(frame,
                      (x1, y1),         # top-left point
                      (x2, y2),         # bottom-right point
                      (255, 144, 51),   # color (BGR)
                      )
        cv2.putText(frame,
                    button.text,
                    (x1 + 30, y1 + 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 100, 51),
                    2)
    return frame


def virtual_keyboard():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8)
    output = ""
    while True:
        ret, frame = cap.read()
        hands, frame = detector.findHands(frame, draw=True)
        frame = drawAll(frame)

        if hands:
            for i in range(len(hands)):
                hand = hands[i]
                lmList = hand["lmList"]
                bbox = hand["bbox"]
                handType = hand["type"]

                if lmList:
                    for button in button_list:
                        x1, y1 = button.pos
                        x2, y2 = x1 + button.size[0], y1 + button.size[1]
                        x1_finger, y1_finger = lmList[8][0], lmList[8][1]      # index finger coordinate
                        if x1 <= x1_finger <= x2 and y1 <= y1_finger <= y2:    # index finger in bbox
                            x2_finger, y2_finger = lmList[4][0], lmList[4][1]  # thumb finger tip

                            # Calculate the Euclidean distance between the index & thumb
                            dist = math.sqrt((x2_finger - x1_finger) ** 2 + (y2_finger - y1_finger) ** 2)
                            if dist < 35:
                                cv2.rectangle(frame,
                                              (x1-10, y1-10),  # top-left point
                                              (x2+10, y2+10),  # bottom-right point
                                              (255, 100, 51),  # deeper color
                                              cv2.FILLED)
                                cv2.putText(frame,
                                            button.text,
                                            (x1 + 30, y1 + 50),
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            1,
                                            (255, 255, 255),
                                            2)
                                if button.text == "Del":
                                    output = output[:-1]  # up to & not include last element ~ remove last element
                                elif len(output) < 42:
                                    output += button.text
                                sleep(0.09)

        # draw display area & display selected key
        cv2.rectangle(frame,
                      (100, 500),
                      (1190, 650),
                      (255, 144, 51),
                      cv2.FILLED)
        if len(output) <= 21:
            cv2.putText(frame,
                        output,
                        (110, 570),
                        cv2.FONT_HERSHEY_PLAIN,
                        5,
                        (255, 255, 255),
                        5)
        else:
            cv2.putText(frame,
                        output[:21],
                        (110, 570),
                        cv2.FONT_HERSHEY_PLAIN,
                        5,
                        (255, 255, 255),
                        5)
            cv2.putText(frame,
                        output[21:],
                        (110, 640),
                        cv2.FONT_HERSHEY_PLAIN,
                        5,
                        (255, 255, 255),
                        5)
        if len(output) >= 42:
            cv2.putText(frame,
                        'Buffer full, please clear inputs',
                        (10, 65),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (49, 49, 245),
                        2,
                        cv2.LINE_AA
                        )

        cv2.putText(frame,
                    'Pinch to select | Press "Q" to quit',
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 144, 51),
                    2,
                    cv2.LINE_AA
                    )
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    button_list = []
    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Del"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

    for i in range(len(keys)):
        for j in range(len(keys[i])):
            button_list.append(Button([100*j+100, 100*i+150], keys[i][j]))

    virtual_keyboard()
