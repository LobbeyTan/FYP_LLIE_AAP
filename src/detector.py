import os
import numpy as np
from yolov7_package import Yolov7Detector
from PIL import Image
from datetime import datetime


class ObjectDetector:

    def __init__(self) -> None:
        self.det = Yolov7Detector(traced=False, img_size=[256, 256], agnostic_nms=True)

    def predict(self, original: Image, enhanced: Image):
        original = np.array(original)
        enhanced = np.array(enhanced)

        classes, boxes, scores = self.det.detect(enhanced)

        original = self.det.draw_on_image(original, boxes[0], scores[0], classes[0])

        enhanced = self.det.draw_on_image(enhanced,  boxes[0], scores[0], classes[0])

        original = Image.fromarray(original)
        enhanced = Image.fromarray(enhanced)

        path = os.getcwd() + r'/temp/output'

        original.save(path + "/%s_DO.png" % (datetime.now().strftime("%Y%m%d")))

        enhanced.save(path + "/%s_DE.png" % (datetime.now().strftime("%Y%m%d")))

        with open(path + "/%s.txt" % (datetime.now().strftime("%Y%m%d")), 'w') as file:
            for i in range(len(classes[0])):
                file.write(f"{classes[0][i]} {' '.join(map(lambda x: str(x / 256), boxes[0][i]))} {scores[0][i]}\n")

        return original, enhanced

    