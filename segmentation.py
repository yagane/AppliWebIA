from ultralytics import YOLO
import numpy as np
import random
import cv2

model = YOLO("yolo-Weights/yolov9c-seg.pt")
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

classes_ids = [classNames.index(clas) for clas in classNames]
colors = [random.choices(range(256), k=3) for _ in classes_ids]


def segment_objects(frame, classes, disco):
    global colors
    results = model(frame, stream=True, verbose=False, classes=classes)

    if disco:
        colors = [random.choices(range(256), k=3) for _ in classes_ids]
    else:
        colors[classes] = (165, 225, 25)

    for r in results:
        if r.masks:
            for mask, box in zip(r.masks.xy, r.boxes):
                points = np.int32([mask])
                color_number = classes_ids.index(int(box.cls[0]))
                cv2.fillPoly(frame, points, colors[color_number])

    return frame