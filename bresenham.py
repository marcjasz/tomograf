class Bresenham:
    @staticmethod
    def get_line(x1, y1, x2, y2):
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
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


    @classmethod
    def get_circle(cls, xc, yc, r):
        x = 0
        y = r
        d = 3 - 2*r
        result = cls.__new_points(xc, yc, x, y)
        while y >= x:
            x += 1
            if d > 0:
                y -= 1
                d = d + 4*(x - y) + 10
            else:
                d = d + 4*x + 6
            result += cls.__new_points(xc, yc, x, y)
        return result

    @staticmethod
    def __new_points(xc, yc, x, y):
        return [(xc+x, yc+y), (xc-x, yc+y),
                (xc+x, yc-y), (xc-x, yc-y),
                (xc+y, yc+x), (xc-y, yc+x),
                (xc+y, yc-x), (xc-y, yc-x)]
