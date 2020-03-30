from skimage import io, color, util, filters
from matplotlib import pyplot as plt
from scanner import Scanner, normalize_photo
from bresenham import Bresenham
from sklearn.metrics import mean_squared_error
import numpy as np
import math
import time

def kernel_function(x):
    if x == 0:
        return 1
    elif x % 2 == 0:
        return 0
    else:
        return (-4/math.pi**2)/(x**2)

if __name__ == '__main__':
    start = time.time()

    img = io.imread('img/Head.jpg')
    img = color.rgb2gray(img)

    scan = Scanner(img, Bresenham).to_square_img()
    scan.set_sampling_params(step=0.01, detectors_number=200, angle=math.pi)
    sinogram = scan.generate_sinogram()
    plt.imshow(sinogram)
    plt.show()

    output = scan.inverse_radon_transform()
    output = np.array(normalize_photo(output))

    # kernel = list(map(kernel_function, range(-20, 21)))
    # kernel = np.convolve(scipy.signal.windows.hamming(10), kernel)
    # scan.filter_samples(kernel)
    # plt.imshow(output)
    # plt.show()

    output = filters.gaussian(output, 6)

    RMSE = mean_squared_error(output, scan.image)**0.5
    plt.imshow(output)
    plt.title('RMSE: ' + str(RMSE))
    plt.show()
    print(time.time() - start)
