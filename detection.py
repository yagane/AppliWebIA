from ultralytics import YOLO
import math
import cv2

model = YOLO("yolo-Weights/yolov9c.pt")
model.to('cuda')

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


def detect_objects(frame, classes):
    results = model(frame, stream=True, verbose=False, classes=classes)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            # confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100

            if confidence > 0.8:

                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                # put box in cam
                cv2.rectangle(frame, (x1, y1), (x2, y2), (165, 225, 25, 0.2), 3)

                # class name
                cls = int(box.cls[0])

                # object details
                org = [x1, y1-10]
                font = cv2.FONT_HERSHEY_DUPLEX
                fontScale = 0.75
                color = (0, 0, 0)
                thickness = 2

                tag = classNames[cls] + " " + str(confidence)

                cv2.putText(frame, tag, org, font, fontScale, color, thickness)

    return frame