from dbm import dumb
import json
import sys
from flask import Flask, jsonify, request
from tese.main import *
from tese.windowcapture import WindowCapture
import threading
from flask_cors import CORS
# from tese.main import run

app = Flask(__name__)
CORS(app)

def dumb_function():
    while True:
        time.sleep(1)

order66 = False
thr = threading.Thread(target=dumb_function)
running = False

@app.route('/', methods=['GET'])
def index():
    return jsonify({'name': 'trina', 'email': 'trina@gmail.com'})

# shows all the open window names
@app.route('/getWindows', methods=['GET'])
def getWindows():
    windows = WindowCapture.list_window_names()
    # print(windows)
    response = jsonify({'windows': windows})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route('/run', methods=['POST'])  
def run():
    global order66
    global thr
    try:
        if not thr.is_alive():
            print(request.data)
            window = request.form.get('window')
            if window != "" and not window in WindowCapture.list_window_names():
                return "Error: Window not found. Try selecting the window again", 202
            img = request.files['file']
            threshold = request.form.get('threshold')
            print(window)
            print(threshold)
            print(img)
            # C:\\Users\\António Cruz\\Documents\\Github\\Detect-and-Track\\\rest_api\\tese\\
            folderPath = os.path.join(os.getcwd(), "imgs")
            print(folderPath)
            img.save(os.path.join('imgs', "target.png"))
            print(window)
            order66 = False
            thr = threading.Thread(target=execute, args=(window, threshold, lambda: order66), kwargs={})
            thr.start() # Will run "foo"
            thr.join(timeout=10)
            # print(windows)
            response = jsonify({'windows': 'running'})
        else:
            response = jsonify({'windows': 'Already running'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        print("error{}".format(e.message))
        return "ERROR: {0}".format(e.message), 202

@app.route('/stop', methods=['POST'])
def stop():
    global order66
    global thr
    order66 = True
    ans = "Order 66 activated"
    print(ans)
    if thr.is_alive():
        thr.join()
    print("order66: {0}".format(order66))
    response = jsonify({'status': ans})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app.run()