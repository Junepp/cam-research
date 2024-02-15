import cv2
import numpy as np
from Detector import Detector

det_instance = Detector()
cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

fps = cam.get(cv2.CAP_PROP_FPS)
print(f'cam fps: {fps}')

while cam.isOpened():
    status, frame = cam.read()

    if status:
        result = det_instance.img2img(frame)

        #.1 trial
        temp_vertical_x = 1200  # sample coords
        cv2.line(result, (temp_vertical_x, 0), (temp_vertical_x, 720), color=(0, 0, 254), thickness=1)  # draw line
        normalized_temp_vertical_x = (temp_vertical_x - 636.187782) / 1002.30343  # projection (to normalized plane)

        ang = np.arctan(normalized_temp_vertical_x/1)  # calculate azimuth
        ang *= 57.2958  # radian to degree

        print(normalized_temp_vertical_x, ang)
        #.1

        cv2.imshow("test", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

else:
    print('camera closed')

cam.release()
cv2.destroyAllWindows()
