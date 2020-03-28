from skimage import io, color, util
from matplotlib import pyplot as plt
from scanner import Scanner, normalize_photo
from bresenham import Bresenham
import numpy as np
import math
import time


if __name__ == '__main__':
    start = time.time()

    img = io.imread('img/Head.jpg')
    img = color.rgb2gray(img)
    scan = Scanner(img, Bresenham).to_square_img()
    scan.set_sampling_params(step=0.08, detectors_number=300, angle=math.pi)

    output = scan.inverse_radon_transform(scan.generate_sinogram())
    plt.imshow(scan.generate_sinogram())
    plt.show()

    plt.imshow(normalize_photo(output))
    plt.show()

    print(time.time() - start)
