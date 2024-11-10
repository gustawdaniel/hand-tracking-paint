import redis
import time
from flask import Flask, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Route to stream SSE
@app.route('/stream')
def stream_hand_positions():
    def generate_hand_positions():
        while True:
            # Retrieve the thumb position from Redis
            thumb_position = r.get('thumb_position')

            if thumb_position:
                thumb_position = thumb_position.decode('utf-8')  # Decode byte string to regular string
                yield f"data: {thumb_position}\n\n"
            else:
                yield "data: No data\n\n"

            time.sleep(0.1)  # Adjust this to control the frequency of updates

    return Response(generate_hand_positions(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
