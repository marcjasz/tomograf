from skimage import io, color, util
from matplotlib import pyplot as plt
from scanner import Scanner, normalize_photo
from bresenham import Bresenham
import numpy as np
import math


if __name__ == '__main__':
    img = io.imread('img/Head.jpg')
    img = color.rgb2gray(img)
    scan = Scanner(img, Bresenham).to_square_img()

    detectors = 100
    step = 0.01
    angle_spread = math.pi/4

    output = scan.inverse_radon_transform(scan.generate_sinogram(angle_spread, detectors, step), math.pi, detectors, step)

    plt.imshow(normalize_photo(output))
    plt.show()
