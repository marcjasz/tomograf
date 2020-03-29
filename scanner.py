from skimage import util
import numpy as np
import math
import functools

def normalize(num, bot, top):
    if num > top:
        return 1
    if num < bot:
        return 0
    
    return (num - bot)/(top - bot)


def normalize_photo(photo):
    bot, top = np.percentile(photo, (40, 98))
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
        self.xc = self.width/2 - 1
        self.yc = self.width/2 - 1
        self.r = self.width/2 - 2

    def set_sampling_params(self, step=None, angle=None, detectors_number=None):
        self.step = step
        self.angle = angle
        self.emitters_number = int(2 / step) - 1
        self.detectors_number = detectors_number

    @property
    @functools.lru_cache()
    def positions(self):
        positions = []
        for rotation in np.linspace(0, math.pi*(2-self.step), self.emitters_number):
            positions.append({ 'rotation': rotation,
                               'samples': self.get_parallel_samples(rotation) })
        return positions

    def get_parallel_samples(self, rotation):
        samples = []
        detector_coords = self.get_detector_coords(rotation)[::-1]
        emitter_coords = self.get_detector_coords(rotation+math.pi)
        for i in range(len(detector_coords)):
            line = self.geometry.get_line(*detector_coords[i], *emitter_coords[i])
            samples.append({ 'emitter': emitter_coords[0],
                             'detector': detector_coords[1],
                             'line': np.array([self.to_plot_coords(coords) for coords in line]),
                             'value': None })
        return samples


    def get_fan_samples(self, rotation):
        samples = []
        emitter_coords = self.get_emitter(rotation)
        for detector_coords in self.get_detector_coords(rotation):
            line = self.geometry.get_line(*emitter_coords, *detector_coords)
            samples.append({ 'emitter': emitter_coords,
                             'detector': detector_coords,
                             'line': np.array([self.to_plot_coords(coords) for coords in line]),
                             'value': None })
        return samples

    def lines(self):
        lines = []
        for position in self.positions:
            lines.extend([self.geometry.get_line(*position['emitter'], *detector) for detector in position['detectors']])
        return lines

    # relative to the center, so angle is twice as big as at the edge
    def get_detector_coords(self, rotation):
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

    @functools.lru_cache()
    def generate_sinogram(self):
        res = []

        # dla każdego położenia tomografu
        for position in self.positions:
            row = []
            # dla każdego detektora w obecnym położeniu tomografu
            for sample in position['samples']:
                # zbierz koordynaty punktów należących do linii między emiterem a detektorem
                # weź ich wartości i dodaj do listy ich średnią
                values = [self.image[coordsx[0], coordsx[1]] for coordsx in sample['line']]
                sample['value'] = np.mean(values)
                row.append(sample['value'])
            res.append(row)
        return np.array(res)

    def inverse_radon_transform(self):
        # przygotuj sobie tablicę samych zer
        res = [[0 for _ in i] for i in self.image]
        
        # wszystko tak samo, tylko dodaj ładnie na każdej linii średnią zamiast zapisywać ją do tablicy 
        # dla każdego położenia tomografu
        for position in self.positions:
            # dla każdego detektora w obecnym położeniu tomografu
            for sample in position['samples']:
                # zbierz koordynaty punktów należących do linii między emiterem a detektorem
                for coordsx in sample['line']:
                    res[coordsx[0]][coordsx[1]] += sample['value']
        return res
