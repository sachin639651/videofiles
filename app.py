from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import keyboard
import json
import pyautogui
from screeninfo import get_monitors
import io
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
thread.start()





@socketio.on('connect')
def handle_connect():
    print('A user connected')
    emit('message_from_server', 'We are connected buddy')
    
    

@socketio.on('message_from_client')
def handle_message_from_client(data):
    print('Message from client:', data)

@socketio.on('reply_to_python')
def handle_message_from_client(data):
    emit('response_from_server', data + " we got you")
    autotype(data)

@socketio.on('key_from_clint')
def handle_message_from_client(data):
    pyautogui.keyDown(data)






@socketio.on('voluem')
def handle_message_from_client(data):
    if(data=='ctab'):
        pyautogui.hotkey('alt','tab')
    if(data=='ntab'):
        pyautogui.hotkey('ctrl','shift','N')
    if(data=='closetab'):
        pyautogui.hotkey('ctrl','w')



@socketio.on('mouse')
def mouse_event(data):
   pyautogui.moveTo((json.loads(data)['x']/100)*1920,(json.loads(data)['y']/100)*1080)  


@socketio.on('click')
def mouse_event(data):
    pyautogui.click((json.loads(data)['x']/100)*1920,(json.loads(data)['y']/100)*1080)




def autotype(data):
    keyboard.write(data)

@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')

# def on_key_press(event):
#     socketio.start_background_task(emit_key_pressed, event.name)

# def emit_key_pressed(key):
#     with app.app_context():
#             if key == 'enter':
#                 # Take a screenshot
#                 screenshot = pyautogui.screenshot()
                
#                 # Convert the image to bytes
#                 img_byte_array = io.BytesIO()
#                 screenshot.save(img_byte_array, format='PNG')
#                 img_byte_array.seek(0)
                
#                 # Emit the screenshot
#                 socketio.emit('image_from_server', img_byte_array.getvalue())


# keyboard.on_press(on_key_press)



if __name__ == '__main__':
    socketio.run(app, port=3000)

