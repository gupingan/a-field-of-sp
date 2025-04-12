from math import comb


def bezier_curve(control_points, steps):
    """
    生成贝塞尔曲线路径
    :param control_points: 控制点列表
    :param steps: 生成路径的步数
    :return: 贝塞尔曲线路径
    """
    n = len(control_points) - 1
    path = []
    for i in range(steps + 1):
        t = i / steps
        point = [0, 0]
        for j, (x, y) in enumerate(control_points):
            binomial_coeff = comb(n, j)
            point[0] += binomial_coeff * (t ** j) * ((1 - t) ** (n - j)) * x
            point[1] += binomial_coeff * (t ** j) * ((1 - t) ** (n - j)) * y
        path.append(point[1])
    return path
