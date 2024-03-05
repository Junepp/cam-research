import cv2
import numpy as np
from Detector import Detector
from Calibrator import Calibrator


def deltaDegreeToDutyRatio(deltaDegree: float):
    7.5 + (deltaDegree / 36)
    ...


DEBUG = True
W = 1920
H = 1080

det_instance = Detector()
cal_instance = Calibrator(file_path='cam_parameters/camera_intrinsics_c922pro.dat')

# camera setting
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

# subo motor setting
import time
import RPI.GPIO as GPIO

# set pin number
pinAzim = 18
pinElev = 19

# pin number rule - GPIO.BCM or GPIO.BOARD
GPIO.setmode(GPIO.BCM)

# set output mode
# GPIO.setup([pinAzim, pinElev], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(pinAzim, GPIO.OUT)
GPIO.setup(pinElev, GPIO.OUT)

# set and initialize PWM
pulseFreq = 50  # based on MG996R datasheet
pulseAzim = GPIO.PWM(pinAzim, pulseFreq)
pulseElev = GPIO.PWM(pinElev, pulseFreq)

pulseAzim.start(7.5)  # 7.5 dutyRatio = 90 degree
pulseElev.start(7.5)

while cam.isOpened():
    status, frame = cam.read()
    print(type(frame))

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

            # generate and send PWM signal
            azimDutyRatio = 7.5 + (azim / 36)
            elevDutyRatio = 7.5 + (elev / 36)

            pulseAzim.ChangeDuty(azimDutyRatio)
            pulseElev.ChangeDuty(elevDutyRatio)

            # TODO. set waiting time
            # TODO. set limit of degree (0 to 180)
            """
            pulse frequency = 50hz
            20ms per each pulse
            1 ms ~ 0 degree (duty ratio = 5%)
            2 ms ~ 180 degree (duty ratio = 10%) 
            """

            if DEBUG:
                cv2.line(hud_frame, (bcx, 0), (bcx, H), color=(0, 0, 255), thickness=1)  # draw vertical line
                cv2.line(hud_frame, (0, bcy), (W, bcy), color=(0, 0, 255), thickness=1)  # draw horizontal line
                cv2.putText(hud_frame, f'azim: {azim:.1f}', (bcx, bcy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        if DEBUG:
            cv2.imshow("DEBUG", hud_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

else:
    print('camera closed')

cam.release()
cv2.destroyAllWindows()

GPIO.cleanup()
