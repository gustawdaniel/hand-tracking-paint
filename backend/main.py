from flask import Flask, Response
from flask_cors import CORS
import cv2
import mediapipe as mp
import time
import threading
import queue

app = Flask(__name__)
CORS(app)

# Hand tracking setup with mediapipe
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Queue for sending hand landmark data to the Flask app
data_queue = queue.Queue(maxsize=1)


def hand_tracking():
    print("Hand tracking thread started.")
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera.")
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 4:  # Specific landmark for example (e.g., the tip of the thumb)
                        print(f"Hand landmark detected at: ({cx}, {cy})")  # Debugging output
                        if data_queue.full():
                            data_queue.get()  # Remove old data if queue is full
                        data_queue.put((cx, cy))  # Place the latest coordinates in the queue
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show FPS
        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def generate_hand_positions():
    print("Starting SSE generator.")
    while True:
        try:
            # Get the latest data from the queue, blocking until available
            cx, cy = data_queue.get(timeout=1)
            print(f"Sending data via SSE: cx={cx}, cy={cy}")  # Debugging output
            yield f"data: {{\"cx\": {cx}, \"cy\": {cy}}}\n\n"
        except queue.Empty:
            print("No data in queue; retrying...")  # Debugging output
            continue


@app.route('/hand-position')
def stream_hand_position():
    return Response(generate_hand_positions(), mimetype="text/event-stream")


if __name__ == "__main__":
    # Start hand-tracking in a separate thread
    threading.Thread(target=hand_tracking, daemon=True).start()
    # Run Flask app
    print("Starting Flask server.")
    app.run(debug=True, threaded=True)
