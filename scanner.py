from skimage import util
import numpy as np
import math

def normalize(num, bot, top):
    if num > top:
        return 1
    if num < bot:
        return 0
    
    return (num - bot)/(top - bot)


def normalize_photo(photo):
    bot, top = np.percentile(photo, (2, 90))
    print(bot, top)
    res = [[normalize(num, bot, top) for num in x] for x in photo]
    return res


class Scanner:
    def __init__(self, image, geometry_strategy):
        self.image = np.array(image)
        self.geometry = geometry_strategy
        self.set_dimensions()

    # center and radius of the inscribed circle
    def set_dimensions(self):
        self.width = self.image.shape[0]
        self.xc = self.width / 2
        self.yc = self.width / 2
        self.r = self.width / 2

    def set_sampling_params(self, step=None, angle=None, detectors_number=None):
        self.step = step
        self.angle = angle
        self.emitters_number = int(2 / step) - 1
        self.detectors_number = detectors_number

    # relative to the center, so angle is twice as big as at the edge
    def get_detectors(self, rotation):
        angle = self.angle / 2
        rotation += math.pi
        angles = np.linspace(-angle + rotation, angle + rotation, self.detectors_number)
        return [(self.r*math.sin(x), self.r*math.cos(x)) for x in angles]

    # relative to the center
    def get_emitter(self, rotation):
        return (self.r*math.sin(rotation), self.r*math.cos(rotation))

    def to_square_img(self):
        diff = self.image.shape[0] - self.image.shape[1]
        padding = (0,)
        if diff > 0:
            padding = ((0, 0), (diff//2, diff - diff//2))
        elif diff < 0:
            padding = ((-math.ceil(diff/2), - diff + math.ceil(diff/2)), (0, 0))
        self.image = util.pad(self.image, padding, 'constant')
        self.set_dimensions()
        return self

    def to_plot_coords(self, coords):
        return (int(-coords[1]+self.r-1), int(coords[0]+self.r-1))

    def generate_sinogram(self):
        res = []

        # dla każdego położenia tomografu
        for i, x in enumerate(np.linspace(0, 2 - self.step, self.emitters_number)):
            res.append([])
            rotation = math.pi * x
            detectors = self.get_detectors(rotation)
            emitter = self.get_emitter(rotation)
            
            # dla każdego detektora w obecnym położeniu tomografu
            for detector in detectors:
                
                # zbierz koordynaty punktów należących do linii między emiterem a detektorem
                line = self.geometry.get_line(int(emitter[0]), int(emitter[1]), int(detector[0]), int(detector[1]))
                line_coords = [self.to_plot_coords(coords) for coords in line]
                line_coords = np.array(line_coords)
                
                # weź ich wartości i dodaj do listy ich średnią
                values = [self.image[coordsx[0], coordsx[1]] for coordsx in line_coords]
                res[i].append(np.mean(values))

        return np.array(res)

    
    def inverse_radon_transform(self, sinogram):
        
        # przygotuj sobie tablicę samych zer
        res = [[0 for _ in i] for i in self.image]
        
        # wszystko tak samo, tylko dodaj ładnie na każdej linii średnią zamiast zapisywać ją do tablicy 

        # dla każdego położenia tomografu
        for i, x in enumerate(np.linspace(0, 2 - self.step, self.emitters_number)):
            rotation = math.pi * x
            detectors = self.get_detectors(rotation)
            emitter = self.get_emitter(rotation)
            
            # dla każdego detektora w obecnym położeniu tomografu
            for j, detector in enumerate(detectors):
                
                # zbierz koordynaty punktów należących do linii między emiterem a detektorem
                line = self.geometry.get_line(int(emitter[0]), int(emitter[1]), int(detector[0]), int(detector[1]))
                line_coords = [self.to_plot_coords(coords) for coords in line]
                line_coords = np.array(line_coords)
                
                for coordsx in line_coords:
                    try:
                        res[coordsx[0]][coordsx[1]] += sinogram[i, j]
                    except IndexError:
                        print(coordsx[0])
                        print(coordsx[1])
                        print(i, j)
                        print("Sinogram: ", np.shape(sinogram))
                        print("Res: ", np.shape(res))

                        exit(-1)
        return res
