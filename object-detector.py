import cv2
import matplotlib.pyplot as plt
import numpy as np


model = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
classes = []
with open ('coco.names','r') as f:
    classes=[line.strip() for line in f.readlines()]
cam=cv2.VideoCapture(0)
while True:
    ret,img = cam.read()
    

    img = cv2.resize(img, (800, 500))
    height, width, _ = img.shape
    ln = model.getLayerNames()
    ln = [ln[i-1] for i in model.getUnconnectedOutLayers()]

            # converting before feeding to yolo model
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), swapRB=True, crop=False)
    model.setInput(blob)
            # getting last layer output
    Layer_out = model.forward(ln)
            # prediction
    boxes = []
    confidences = []
    class_ids = []

    for output in Layer_out:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.70:
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

            # method for bounding boxes
            # index method

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes)))
    results = []
            # drawing
    if (len(indexes)) > 0.95:
        for i in indexes.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label + "  " + confidence, (x, y - 5), font, 1, (0, 0, 0), 2)
            results.append(label)
            # results.extend(results)
    cv2.imshow("Object DETECTED", img)

    k = cv2.waitKey(1) & 0xFF
    if k == ord("e"):
        break        

cam.release()
cv2.destroyAllWindows()