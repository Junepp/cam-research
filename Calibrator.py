class Calibrator:
    """
    p: image plane
    n: normalized plane
    d: distorted
    u: undistorted
    """
    def __init__(self, file_path: str):
        self.fx = 0
        self.fy = 0
        self.cx = 0
        self.cy = 0
        self.skew = 0
        self.k1 = 0
        self.k2 = 0
        self.k3 = 0

        self._load_parameters(file_path)

    def _load_parameters(self, file_path):
        with open(file_path, 'r') as f:
            data = f.readlines()
        
        focal_x, skew_coefficient, principal_x = map(float, data[1].split())
        _, focal_y, principal_y = map(float, data[2].split())
        distortion_coefficients = list(map(float, data[5].split()))

        self.fx = focal_x
        self.fy = focal_y
        self.cx = principal_x
        self.cy = principal_y
        self.skew = skew_coefficient
        self.k1, self.k2, self.p1, self.p2, self.k3 = distortion_coefficients

    def _normalize(self, px: float, py: float):
        ny = (py - self.cy) / self.fy
        nx = (px - self.cx) / self.fx - self.skew * ny

        return nx, ny

    def _distort_normal(self, x: float, y: float):
        r2 = x**2 + y**2
        radial_d = 1 + (r2 ** 1) * self.k1 + (r2 ** 2) * self.k2 + (r2 ** 3) * self.k3
        x_d = radial_d * x + 2 * self.p1 * x * y + self.p2 * (r2 + 2 * x * x)
        y_d = radial_d * y + 2 * self.p2 * x * y + self.p1 * (r2 + 2 * y * y)

        return x_d, y_d

    def undistort(self, pdx: float, pdy: float):
        """
        normalize and undistort
        :param pdx: image plane coords x
        :param pdy: image plane coords y
        :return: normalized and undistorted coords set (x, y)
        """

        ndx, ndy = self._normalize(pdx, pdy)
        nux = ndx
        nuy = ndy

        for _ in range(3):
            temp_x, temp_y = self._distort_normal(nux, nuy)
            err_x = temp_x - ndx
            err_y = temp_y - ndy

            nux -= err_x
            nuy -= err_y

        return nux, nuy
