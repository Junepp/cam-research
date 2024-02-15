class Calibrator:
    def __init__(self):
        self.parameters = self._load_parameters()

    def _load_parameters(self):
        file_path = 'camera_intrinsics.dat'
        with open(file_path, 'r') as f:
            data = f.readlines()

        focal_x, skew_coefficient, principal_x = map(float, data[1].split())
        _, focal_y, principal_y = map(float, data[2].split())
        distortion_coefficients = list(map(float, data[5].split()))

        camera_parameters = dict()

        camera_parameters['fx'] = focal_x
        camera_parameters['fy'] = focal_y
        camera_parameters['cx'] = principal_x
        camera_parameters['cy'] = principal_y
        camera_parameters['skew'] = skew_coefficient
        camera_parameters['dis_coef'] = distortion_coefficients

        return camera_parameters


if __name__ == '__main__':
    cal_instance = Calibrator()
    for k, v in cal_instance.parameters.items():
        print(f'{k}: {v}')
