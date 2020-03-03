from skimage import io, color, util
from matplotlib import pyplot as plt
import math

def to_square(image):
    diff = image.shape[0] - image.shape[1]
    padding = (0,)
    if diff > 0:
        padding = ((0, 0), (diff//2, diff - diff//2))
    elif diff < 0:
        padding = ((-math.ceil(diff/2), - diff + math.ceil(diff/2)), (0, 0))
    return util.pad(image, padding, 'constant')


if __name__ == '__main__':
    img = io.imread('img/CT_ScoutView-large.jpg')
    img = color.rgb2gray(img)
    img = to_square(img)

    plt.imshow(img)
    plt.show()

