fp = 'camera_intrinsics.dat'

with open(fp, 'r') as f:
    data = f.readlines()

for idx, each in enumerate(data):
    if idx == 0 or idx == 4:
        print(each.strip())
        continue

    exponential_values = each.strip().split()

    a = list(map(float, exponential_values))

    for v in a:
        print(v, end=' ')

    else:
        print()
