from flask import Flask, Response
from flask_cors import CORS
import cv2
import mediapipe as mp
import time
import threading

app = Flask(__name__)
CORS(app)

# Variables for hand-tracking
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Shared data for hand landmarks
cx, cy = None, None

# SSE generator function to stream hand landmark data
def generate_hand_positions():
    global cx, cy
    while True:
        print('generate', cx, cy)
        if cx is not None and cy is not None:
            yield f"data: {{\"cx\": {cx}, \"cy\": {cy}}}\n\n"
        time.sleep(0.1)  # Adjust to control data emission rate

@app.route('/hand-position')
def stream_hand_position():
    return Response(generate_hand_positions(), mimetype="text/event-stream")

def hand_tracking():
    global cx, cy
    pTime = 0
    while True:
        success, img = cap.read()
        if not success:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)  # Update cx, cy with latest values
                    print('update', cx, cy)
                    if id == 4:  # Drawing circle on a specific landmark
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # FPS display
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run Flask server and hand-tracking in separate threads
if __name__ == "__main__":
    # Start hand-tracking in a separate thread
    threading.Thread(target=hand_tracking).start()
    # Run Flask app
    app.run(debug=True, threaded=True)
