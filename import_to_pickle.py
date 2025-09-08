import csv
from math import floor, sqrt
import pickle
from read_me import *


class Point:
    def __init__(self, x, y, z, n):
        self.x = x
        self.y = y
        self.z = z
        self.n = n
        self.nearest_cr = None
        self.nearest_co = None
        self.nearest_ni = None
        self.nearest = None

    def dist(self, p2):
        return sqrt((p2.x - self.x) ** 2 + (p2.y - self.y) ** 2 + (p2.z - self.z) ** 2)

    def island_score(self):
        tot = len(self.nearest)
        alien = sum(1 for p in self.nearest if p.n != self.n)
        return alien / tot

    def is_island(self):
        return self.island_score() >= i_thres


def choose_name(mass):
    if 25.8280 < mass < 26.1700 \
            or 24.9140 < mass < 25.0900 \
            or 26.3630 < mass < 26.6230 \
            or 26.8970 < mass < 27.0640 \
            or 51.8520 < mass < 52.1600:
        return Cr

    if 28.8471 < mass < 29.1820 \
            or 29.8650 < mass < 30.1570 \
            or 30.3930 < mass < 30.5900 \
            or 30.8570 < mass < 31.1100 \
            or 31.8770 < mass < 32.0740 \
            or 57.8350 < mass < 58.0540 \
            or 59.8740 < mass < 60.0210:
        return Ni

    if 29.3290 < mass < 29.6880 \
            or 58.8580 < mass < 59.0410:
        return Co

    return False


def import_data(z_limit_min, z_limit_max):
    blocks = {}
    for i in range(x_min * 2, x_max * 2):
        for j in range(y_min * 2, y_max * 2):
            for k in range(z_limit_min * 2, z_limit_max * 2):
                blocks[(i, j, k)] = []

    size = 0
    with open(csv_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            x, y, z = float(row['Xnm']), float(row['Ynm']), float(row['Znm'])
            n = choose_name(float(row['Mass']))
            if n and z_limit_min < z < z_limit_max:
                blocks[(floor(x * 2), floor(y * 2), floor(z * 2))].append(Point(x, y, z, n))
    return blocks


if __name__ == "__main__":
    with open(pickle_name, 'wb') as f:
        data = import_data(z_limit_min, z_limit_max)
        pickle.dump(data, f)
