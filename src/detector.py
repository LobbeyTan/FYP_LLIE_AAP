import os
import random
from datetime import datetime
from time import time

from PIL import Image, ImageDraw
from yolov7_package import Yolov7Detector

from src import labels


class ObjectDetector:

    def __init__(self) -> None:
        random.seed(2022)

        self.det = Yolov7Detector(traced=False, img_size=[256, 256], agnostic_nms=True)
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in labels]
        self.running_time = 0

    def predict(self, original: Image, enhanced: Image):
        start = time()
        classes, boxes, scores = map(lambda x: x[0], self.det.detect(enhanced))
        self.running_time = time() - start

        original = self.__drawBBox(original, boxes, scores, classes)

        enhanced = self.__drawBBox(enhanced,  boxes, scores, classes)

        path = os.getcwd() + r'/temp/output'

        with open(path + "/%s.txt" % (datetime.now().strftime("%Y%m%d")), 'w') as file:
            for i in range(len(classes)):
                x1, y1, x2, y2 = boxes[i]
                bbox = [x1, y1, x2 - x1, y2 - y1]

                file.write(f"{classes[i]} {' '.join(map(str, bbox))} {scores[i]}\n")

        return original, enhanced

    def __drawBBox(self, img, boxes, scores, classes):
        img = img.copy()
        draw = ImageDraw.Draw(img)

        for i in range(len(classes)):
            color = tuple(self.colors[int(classes[i])])

            label = f' {labels[int(classes[i])]} {scores[i]:.2f} '
            x1, y1, x2, y2 = boxes[i]

            draw.rectangle((x1, y1, x2, y2), outline=color, width=2)

            bbox = draw.textbbox((x1, y1 - 12), label)
            draw.rectangle(bbox, fill=color)
            draw.text((x1, y1 - 12), label)

        return img
