from skimage import io, color, util
from matplotlib import pyplot as plt
from scanner import Scanner
import math

if __name__ == '__main__':
    img = io.imread('img/CT_ScoutView.jpg')
    img = color.rgb2gray(img)
    scan = Scanner(img).to_square_img()

    plt.imshow(scan.image)
    plt.show()

