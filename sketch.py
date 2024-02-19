import cv2
import numpy as np
from Detector import Detector
from Calibrator import Calibrator

det_instance = Detector()
cal_instance = Calibrator(file_path='camera_intrinsics.dat')

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while cam.isOpened():
    status, frame = cam.read()

    if status:
        result = det_instance.predict(frame)
        hud_frame = result[0].plot()

        # get coords
        coords = result[0].boxes.xywh.numpy()
        if len(coords) >= 1:
            bcx, bcy, _, _ = map(int, coords[0])

            cv2.line(hud_frame, (bcx, 0), (bcx, 720), color=(0, 0, 255), thickness=1)  # draw line
            cv2.line(hud_frame, (0, bcy), (1280, bcy), color=(0, 0, 255), thickness=1)  # draw line

            n2x, n2y = cal_instance.undistort(bcx, bcy)

            ang2 = np.arctan(n2x / 1)  # calculate azimuth
            ang2 *= 57.2958  # radian to degree
            print(n2x, ang2)

        cv2.imshow("test", hud_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

else:
    print('camera closed')

cam.release()
cv2.destroyAllWindows()
