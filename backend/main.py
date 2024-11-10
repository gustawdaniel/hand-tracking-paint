import cv2
import mediapipe as mp
import time
from flask import Flask, Response
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)
# OpenCV video capture
cap = cv2.VideoCapture(0)

# Set up MediaPipe hand tracking
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

# def generate_hand_positions():
#     global cap
#     global mpHands
#     global hands
#     global mpDraw
#     global pTime
#     global cTime

while True:
    success, img = cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    hand_positions = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 4:  # Track the tip of the thumb
                    hand_positions.append(f"{cx},{cy}")
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    # if hand_positions:
    #     yield f"data: {','.join(hand_positions)}\n\n"

    # FPS calculation for display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

# generate_hand_positions()

# @app.route('/stream')
# def stream_hand_positions():
#     return Response(generate_hand_positions(), mimetype="text/event-stream")
#
#
# if __name__ == "__main__":
#     app.run(debug=True, threaded=True)
