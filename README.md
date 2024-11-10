## Intro

This is code for event: https://www.meetup.com/lets-learn-together/events/304130308/?eventOrigin=home_page_upcoming_events$all

## Hands tracking

Setup conda

```bash
conda create -n hand-tracking
conda activate hand-tracking
```

install libs

```bash
conda install opencv
pip install mediapipe
```

Learn more about them
- [opencv](https://docs.opencv.org/4.x/d1/dfb/intro.html)
- [mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide)

Add backed code to detect hands `hands-tracking.py`

```python
import cv2
import mediapipe as mp
import time

# check your index of camera
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
```

## SSE

Learn sse:

- [sse client](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- [sse backend](https://medium.com/@nandagopal05/server-sent-events-with-python-fastapi-f1960e0c8e4b)

On backend add

```bash
conda install flask
```

and run

```python
from flask import Flask, Response
import random
import time

app = Flask(__name__)

def generate_random_numbers():
    while True:
        # Send a random number every second
        time.sleep(1)
        yield f"data: {random.randint(1, 100)}\n\n"

@app.route('/numbers')
def stream_random_numbers():
    return Response(generate_random_numbers(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
```

It will start at `http://127.0.0.1:5000` on route `/nubers`

Add frontend code by

```bash
npm create vite@latest .
```

then
- vanilla
- typescript yes

start project by

```bash
pnpm i && pnpm dev
```

Fronted will be available on `http://localhost:5173/`

If we just connect by `sse.ts`

```ts
export function setupSSEReceiver(element: HTMLElement) {
  const eventSource = new EventSource('http://127.0.0.1:5000/numbers')
  eventSource.onmessage = (event) => {
    element.innerHTML = event.data
  }
}
```

and `main.ts`

```ts
import './style.css'
import { setupSSEReceiver } from './sse.ts'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
     <p id="sse"></p>
  </div>
`

setupSSEReceiver(document.querySelector<HTMLElement>('#sse')!)
```

we will see CORS problem

```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at http://127.0.0.1:5000/numbers. (Reason: CORS header ‘Access-Control-Allow-Origin’ missing). Status code: 200.
```

We can fix by.:

```bash
conda install Flask-CORS
```

and lines in `sse.py`

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
```

On this stage we should be able to see random numbers on screen.