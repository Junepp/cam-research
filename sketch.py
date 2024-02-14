import cv2
from Detector import Detector

det_instance = Detector()
cam = cv2.VideoCapture(0)

fps = cam.get(cv2.CAP_PROP_FPS)
print(f'cam fps: {fps}')

while cam.isOpened():
    status, frame = cam.read()

    if status:
        result = det_instance.img2img(frame)
        cv2.imshow("test", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

else:
    print('camera closed')

cam.release()
cv2.destroyAllWindows()
