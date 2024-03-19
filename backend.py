import numpy as np
import cv2,os
from PIL import ImageTk, Image

def detectobj(file):
    net = cv2.dnn.readNet("./weights/yolov3.weights", "./weights/yolov3.cfg")
    classes = []
    with open("./weights/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]
    img = cv2.imread(file)
    height, width, channels = img.shape
    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
     
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    detect = []

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])

            detect.append(label)
            color = np.random.uniform(0, 255, size=(i+1, 3))[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 1, color, 1)
         
            
    de = list(set(detect))
    cv2.imwrite("temp.png", img)
    lt = os.listdir('data')
    dirc = []

    for i in detect:
        for j in lt:
            if i in j or j in i:
                dirc.append('./data/'+j)

    return dirc,de

