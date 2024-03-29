import numpy as np
from ultralytics import YOLO


class Detector:
    def __init__(self, conf_threshold=0.8):
        self.model = YOLO('yolov8n.pt')
        self.model_input_size = 640
        self.conf_threshold = conf_threshold

    def predict(self, img: np.array):
        return self.model.predict(img, imgsz=self.model_input_size, conf=self.conf_threshold, verbose=False)


# DEBUG
if __name__ == '__main__':
    import cv2

    img = cv2.imread('sample_data/sample_1.png')

    det_instance = Detector()

    retval = det_instance.predict(img)
    hud_frame = retval[0].plot()

    cv2.imshow('temp', hud_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
