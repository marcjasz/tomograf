from skimage import util
import math

class Scanner:
    def __init__(self, image):
        self.image = image

    def to_square_img(self):
        diff = self.image.shape[0] - self.image.shape[1]
        padding = (0,)
        if diff > 0:
            padding = ((0, 0), (diff//2, diff - diff//2))
        elif diff < 0:
            padding = ((-math.ceil(diff/2), - diff + math.ceil(diff/2)), (0, 0))
        self.image = util.pad(self.image, padding, 'constant')
        return self

    def bresenham(self, x1, y1, x2, y2):
        y_diff = y2 - y1
        x_diff = x2 - x1
        result = []
        if x_diff == 0:
            if y2 < y1:
                y1, y2 = y2, y1
            for y in range(y1, y2+1):
                result.append((x1, y))
        else:
            m = float(y_diff) / x_diff
            inc = 1 if m >= 0 else -1
            current = 0
            if m <= 1 and m >= -1:
                step = abs(y_diff) * 2
                thresh = abs(x_diff)
                thresh_step = abs(x_diff) * 2
                y = y1
                if x2 < x1:
                    x1, x2 = x2, x1
                    y = y2
                for x in range(x1, x2+1):
                    result.append((x, y))
                    current += step
                    if current >= thresh:
                        y += inc
                        thresh += thresh_step
            else:
                step = abs(x_diff) * 2
                thresh = abs(y_diff)
                thresh_step = abs(y_diff) * 2
                x = x1
                if y2 < y1:
                    y1, y2 = y2, y1
                    x = x2
                for y in range(y1, y2+1):
                    result.append((x, y))
                    current += step
                    if current >= thresh:
                        x += inc
                        thresh += thresh_step
        return result

