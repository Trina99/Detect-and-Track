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
    # print(request.headers)
    # print(request.cookies)
    print(request.data)
    # print(request.args)
    # print(request.form)
    # print(request.endpoint)
    # print(request.method)
    # print(request.remote_addr)
    # record = request.get_json()
    # window = record['window']
    # img_path = record['img']
    # threshold = record['threshold']
    # print("IMAGE_PATH: " + img_path)
    window = request.form.get('window')
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
    thr = threading.Thread(target=execute, args=(window, threshold), kwargs={})
    thr.start() # Will run "foo"
    # print(windows)
    response = jsonify({'windows': 'running'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app.run()