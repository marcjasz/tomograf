from skimage import io, color, util
from matplotlib import pyplot as plt
from scanner import Scanner
import numpy as np
import math

if __name__ == '__main__':
    img = io.imread('img/Kropka.jpg')
    img = color.rgb2gray(img)
    scan = Scanner(img).to_square_img()
    scan.radius = scan.width//2 - 1

    circle = scan.circle_bresenham(scan.width//2, scan.width//2, scan.radius)
    indexes = np.array(circle).transpose()
    scan.image[indexes[0], indexes[1]] = 1
    line = scan.line_bresenham(0, 0, scan.width-1, scan.width-1)
    line_indexes = np.array(line).transpose()
    scan.image[line_indexes[0], line_indexes[1]] = 1

    plt.imshow(scan.image)
    plt.show()
