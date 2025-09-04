import cv2
from mistral_api import query
from detection import detect_objects
from segmentation import segment_objects
from flask import Flask, render_template, Response, jsonify, request
from markdown2 import Markdown


app = Flask(__name__)

camera = cv2.VideoCapture(0)

markdowner = Markdown()

classes = 0
flag = True
disco = False

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if flag:
                frame = detect_objects(frame, classes)
            else:
                frame = segment_objects(frame, classes, disco)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Définition du répertoire statique
app.static_folder = 'static'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detection', methods=['POST'])
def detection():
    global flag, disco
    flag = True
    disco = False
    return jsonify({'success': True})


@app.route('/segmentation', methods=['POST'])
def segmentation():
    global flag, disco
    flag = False
    disco = False
    return jsonify({'success': True})


@app.route('/segmentation_disco', methods=['POST'])
def segmentation_disco():
    global flag, disco
    flag = False
    disco = True
    return jsonify({'success': True})


@app.route('/submit', methods=['POST'])
def submit():
    global classes
    choice = request.form.get('choix')
    if classNames.count(choice) == 1:
        classes = classNames.index(choice)
    return jsonify({'success': True})


@app.route('/ask', methods=['POST'])
def ask():
    global classes
    user_message = request.form['user_message']
    result = markdowner.convert(query(user_message))
    return jsonify({'response': result})


if __name__ == '__main__':
    app.run(debug=True)  # , host="192.168.0.153"
