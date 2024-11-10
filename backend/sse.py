from flask import Flask, Response
import random
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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