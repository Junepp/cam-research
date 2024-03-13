"""
reference: https://github.com/tsutsuji815/pixel_convert
"""

import numpy as np

n8 = np.array([[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]],
              np.uint8)

n4 = np.array([[0, 1, 0],
               [1, 1, 1],
               [0, 1, 0]],
              np.uint8)


def make_dot(img, k=3, scale=2, color=True, blur=0, erode=0, saturation=1):
    """
    :param img:
    :param k: num of colors [1:]
    :param scale: dot size [1:4]
    :param color:
    :param blur: 0
    :param erode: 0 (disable) / 1, 2
    :param saturation: 1 (disable) / 1.5, 2.0
    :return: Tuple, (image: np.ndarray, color_info: )
    """
    h, w, c = img.shape

    d_h = int(h / scale)
    d_w = int(w / scale)

    if erode == 1:
        img = cv2.erode(img, n4, iterations=1)

    elif erode == 2:
        img = cv2.erode(img, n8, iterations=1)

    if blur:
        img = cv2.bilateralFilter(img, 15, blur, 20)

    img = cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)

    if color:
        img_cp = img.reshape(-1, c)

    else:
        img_cp = img.reshape(-1)

    img_cp = img_cp.astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(img_cp, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    center = center.astype(np.uint8)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    result = cv2.resize(result, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)

    # increase saturation
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    colors = []

    for res_c in center:
        color_code = '#{0:02x}{1:02x}{2:02x}'.format(res_c[2], res_c[1], res_c[0])
        colors.append(color_code)

    return result, colors


if __name__ == '__main__':
    import cv2
    import numpy as np

    DEBUG = True
    W = 1920
    H = 1080
    R = 0.3
    mode = 0

    cam = cv2.VideoCapture(0)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # temp
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)

    while cam.isOpened():
        status, frame = cam.read()

        if status:
            frame = cv2.resize(frame, (int(W*R), int(H*R)))

            if mode == 1:
                frame, color_info = make_dot(frame, k=8, scale=4, color=True, blur=0, erode=0, saturation=1.5)

            cv2.imshow("pixelart", frame)

        k = cv2.waitKey(1)

        if k & 0xFF == ord('q'):
            break

        elif k & 0xFF == ord('c'):
            mode = 1 - mode

    else:
        print('camera closed')

    cam.release()
    cv2.destroyAllWindows()
