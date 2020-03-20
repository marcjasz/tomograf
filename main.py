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

    rotation = math.pi*1.8
    detectors = scan.get_detectors(math.pi/5, rotation, 25)
    emitter = scan.get_emitter(rotation)

    for detector in detectors:
        line = scan.line_bresenham(int(emitter[0]), int(emitter[1]), int(detector[0]), int(detector[1]))
        line_indexes = [scan.to_plot_coords(coords) for coords in line]
        line_indexes = np.array(line_indexes).transpose()
        scan.image[line_indexes[0], line_indexes[1]] = 1

    circle = scan.circle_bresenham(0, 0, scan.radius)
    indexes = [scan.to_plot_coords(coords) for coords in circle]
    indexes = np.array(indexes).transpose()
    scan.image[indexes[0], indexes[1]] = 1

    plt.imshow(scan.image)
    plt.show()
