import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
from bresenham import bresenham


def bresenham1(x1, y1, x2, y2):
    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)

    tuples = []

    y = y1
    for x in range(x1, x2 + 1):

        print("(", x, ",", y, ")\n")
        tuples.append((x, y))

        # Add slope to increment angle formed
        slope_error_new = slope_error_new + m_new

        # Slope error reached limit, time to
        # increment y and update slope error.
        if (slope_error_new >= 0):
            y = y + 1
            slope_error_new = slope_error_new - 2 * (x2 - x1)

        # driver function
    return tuples


if __name__ == '__main__':
    x1 = 15
    y1 = 15
    x2 = 5
    y2 = 5
    points = bresenham(x1, y1, x2, y2)

    # print(list(points))


    x = np.linspace(0, 10, 30)
    y = np.sin(x)

    plt.scatter(*zip(*points))

    plt.show()