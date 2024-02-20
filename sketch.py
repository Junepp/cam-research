import cv2
import numpy as np
from Detector import Detector
from Calibrator import Calibrator

DEBUG = True
W = 1920
H = 1080

det_instance = Detector()
cal_instance = Calibrator(file_path='camera_intrinsics_c922pro.dat')

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

while cam.isOpened():
    status, frame = cam.read()

    if status:
        result = det_instance.predict(frame)

        # get coords and image
        coords = result[0].boxes.xywh.numpy()
        hud_frame = result[0].plot()

        if len(coords) >= 1:  # detect at least one object
            # H/W Control
            bcx, bcy, _, _ = map(int, coords[0])  # on image plane, coords of detection box center
            n2x, n2y = cal_instance.undistort(bcx, bcy)  # project to normalize plane and undistort

            # get azimuth and elevation
            azim = np.arctan(n2x) * 57.2958  # radian to degree
            elev = np.arctan(n2y) * 57.2958  # radian to degree
            print(f'azim: {azim:.1f}, elev: {elev:.1f}')

            # TODO. generate PWM signal
            # TODO. send PWM to each subo-motor

            if DEBUG:  # debug
                cv2.line(hud_frame, (bcx, 0), (bcx, H), color=(0, 0, 255), thickness=1)  # draw vertical line
                cv2.line(hud_frame, (0, bcy), (W, bcy), color=(0, 0, 255), thickness=1)  # draw horizontal line
                cv2.putText(hud_frame, f'azim: {azim:.1f}', (bcx, bcy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        if DEBUG:  # debug
            cv2.imshow("DEBUG", hud_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

else:
    print('camera closed')

cam.release()
cv2.destroyAllWindows()
