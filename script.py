from flask import Flask, render_template
from flask_socketio import SocketIO,emit
import mss
import base64
import numpy as np
import cv2
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def send_frame():
    while True:
        with mss.mss() as sct:
            # Capture the screen
            screen = sct.grab(sct.monitors[1])  # Change monitor index as needed

            # Convert screen capture to numpy array
            frame = np.array(screen)

            # Convert the frame to base64 string
            _, buffer = cv2.imencode('.jpg', frame)
            frame_str = base64.b64encode(buffer).decode('utf-8')

            # Emit the frame to all connected clients
            socketio.emit('frame', frame_str)
            time.sleep(0.1)  # Adjust frame rate as needed

# Start send_frame() function in a separate thread
thread = threading.Thread(target=send_frame)
thread.daemon = True


@socketio.on('connect')
def handle_connect():
    print('A user connected')
    emit('connection','We are connected')
    thread.start()


@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')

if __name__ == '__main__':
    socketio.run(app, port=3000)






