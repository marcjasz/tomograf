from skimage import io, color
from matplotlib import pyplot as plt

if __name__ == '__main__':
    img = io.imread('img/Kropka.jpg')
    img = color.rgb2gray(img)
    plt.imshow(img)
    plt.show()

