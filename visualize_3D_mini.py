from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sqrt
import pickle
import numpy as np
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

    def cluster_score(self):
        tot = len(self.nearest)
        eigen = sum(1 for p in self.nearest if p.n == self.n)
        return eigen / tot

    def is_island(self):
        return self.island_score() >= i_thres

    def in_cluster(self):
        return self.cluster_score() >= c_thres

    def adj_score(self):
        cr_s = sum(self.weight_func(p) for p in self.nearest if p.n == Cr)
        co_s = sum(self.weight_func(p) for p in self.nearest if p.n == Co)
        ni_s = sum(self.weight_func(p) for p in self.nearest if p.n == Ni)
        return np.array([cr_s, co_s, ni_s])

    def weight_func(self, p):
        # Update afterwards
        coeff = 1 if p.n != self.n else 0.5
        return coeff


def name_to_str(name):
    if name == Cr:
        return "Cr"
    elif name == Co:
        return "Co"
    elif name == Ni:
        return "Ni"
    return ""


def str_to_name(nstr):
    if nstr == "Cr":
        return Cr
    elif nstr == "Co":
        return Co
    elif nstr == "Ni":
        return Ni
    return -1


def plot_line(p, np, ax):
    if p.n == Cr:
        color = color_cr_cr if np.n == Cr else color_cr_co if np.n == Co else color_cr_ni
    elif p.n == Co:
        color = color_cr_co if np.n == Cr else color_co_co if np.n == Co else color_co_ni
    else:
        color = color_cr_ni if np.n == Cr else color_co_ni if np.n == Co else color_ni_ni
    ax.plot([p.x, np.x], [p.y, np.y], [p.z, np.z], color=color)


def plot_lines(t1, t2, ax, ps):
    for p in ps[name_to_str(t1)]:
        np_list = p.nearest_cr if t2 == Cr else p.nearest_co if t2 == Co else p.nearest_ni if t2 == Ni else p.nearest
        for np in np_list:
            plot_line(p, np, ax)


def plot_points(ax, ps):
    ax.scatter([p.x for p in ps["Cr"]], [p.y for p in ps["Cr"]], [p.z for p in ps["Cr"]], color=color_cr)
    ax.scatter([p.x for p in ps["Co"]], [p.y for p in ps["Co"]], [p.z for p in ps["Co"]], color=color_co)
    ax.scatter([p.x for p in ps["Ni"]], [p.y for p in ps["Ni"]], [p.z for p in ps["Ni"]], color=color_ni)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')


def get_points_to_draw(blocks, z_limit_min, z_limit_max):
    ps = {"Cr": [], "Co": [], "Ni": []}
    size = 0
    for i in range(x_min * 2 + 2, x_max * 2 - 2):
        for j in range(y_min * 2 + 2, y_max * 2 - 2):
            for k in range(z_limit_min * 2 + 2, z_limit_max * 2 - 2):
                # if x_range[0] * 2 <= i < x_range[1] * 2 \
                #         and y_range[0] * 2 <= j < y_range[1] * 2 \
                #         and z_range[0] * 2 <= k < z_range[1] * 2:
                    block_points = blocks[(i, j, k)]
                    block_neighbors = []
                    for di in range(-2, 3):
                        for dj in range(-2, 3):
                            for dk in range(-2, 3):
                                block_neighbors += blocks[(i + di, j + dj, k + dk)]
                    for p in block_points:
                        nps = {"Cr": [], "Co": [], "Ni": []}
                        for np in block_neighbors:
                            nps[name_to_str(np.n)].append((p.dist(np), np))
                        i_cr = 1 if p.n == Cr else 0
                        i_co = 1 if p.n == Co else 0
                        i_ni = 1 if p.n == Ni else 0
                        p.nearest_cr = [d[1] for d in sorted(nps["Cr"], key=lambda d: d[0])
                        [i_cr+n_nearest_low:i_cr + n_nearest_high]]
                        p.nearest_co = [d[1] for d in sorted(nps["Co"], key=lambda d: d[0])
                        [i_co+n_nearest_low:i_co + n_nearest_high]]
                        p.nearest_ni = [d[1] for d in sorted(nps["Ni"], key=lambda d: d[0])
                        [i_ni+n_nearest_low:i_ni + n_nearest_high]]
                        p.nearest = [d[1] for d in sorted(nps["Cr"] + nps["Co"] + nps["Ni"], key=lambda d: d[0])
                        [1+n_nearest_low:1+n_nearest_high]]
                        ps[name_to_str(p.n)].append(p)
                        size += 1
                        if size % 10000 == 0:
                            print(size)
    return ps


def get_islands_percentage(ps):
    elements = ps.keys()
    ipc = {}
    for e in elements:
        es = ps[e]
        tout = len(es)
        ipc[e] = sum(1 for e in es if e.is_island()) / tout if tout else 0.0
    return ipc


def get_cluster_percentage(ps):
    elements = ps.keys()
    cpc = {}
    for e in elements:
        es = ps[e]
        tout = len(es)
        cpc[e] = sum(1 for e in es if e.in_cluster()) / tout
    return cpc


def get_adjacency_score(ps):
    elements = ps.keys()
    adjs = {}
    for e in elements:
        es = ps[e]
        adj_i = sum(e.adj_score() for e in es)
        adjs[e] = adj_i / sum(adj_i)
    return adjs


def alien_link_num(islands, ps):
    b = []
    for e in ["Cr", "Co", "Ni"]:
        b.append(len(ps[e]) * (n_nearest_high - n_nearest_low) * islands[e])
    A = np.array([[1, 1, 0],
                  [0, 1, 1],
                  [1, 0, 1]])
    b = np.array(b)
    # CrNi, CrCo, CoNi
    links = np.linalg.solve(A, b)
    return links


def rotate(ax):
    def tourner(angle):
        ax.view_init(azim=angle)
    return tourner


def ps_bond_visualize(ps, anim=False):
    fig = plt.figure(figsize=(8, 8), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    if p_type == all_three:
        if np_type == all_three:
            for i in elements:
                for j in elements:
                    plot_lines(i, j, ax, ps)
        else:
            for i in elements:
                plot_lines(i, np_type, ax, ps)
    elif np_type == all_three:
        for j in elements:
            plot_lines(p_type, j, ax, ps)
    else:
        plot_lines(p_type, np_type, ax, ps)
    plot_points(ax, ps)
    plt.show()
    if anim:
        print("Making animation")
        rot_animation = animation.FuncAnimation(fig, rotate(ax), frames=np.arange(0, 362, 2), interval=100)
        rot_animation.save('rotation_n:{0}_p:{1}_np:{2}.gif'.format((n_nearest_low, n_nearest_high), p_type, np_type),
                           dpi=80, writer='imagemagick')


if __name__ == "__main__":
    with open(pickle_name, 'rb') as f:
        blocks = pickle.load(f)

    ps = get_points_to_draw(blocks, z_limit_min, z_limit_max)
    stat = []
    # print("n_nearest,count,r_cr,r_co,r_ni")
    for n_limit in range(1, 20):
        sum_cr = sum_co = sum_ni = count = 0
        for p in (ps['Cr']):
            for np in p.nearest[:n_limit]:
                if np.n == Cr:
                    sum_cr += 1
                elif np.n == Co:
                    sum_co += 1
                elif np.n == Ni:
                    sum_ni += 1
            count += 1
        stat.append([n_limit, sum_cr / count / n_limit, sum_co / count / n_limit, sum_ni / count / n_limit])
        # print("{},{},{},{},{}".format(n_limit, count, sum_cr / count / n_limit,
        #                               sum_co / count / n_limit, sum_ni / count / n_limit))

    plt.title('{}, z_limit_min={}, z_limit_max={}'.format(pickle_name, z_limit_min, z_limit_max))
    cr_ratio, = plt.plot([i[0] for i in stat], [i[1] for i in stat], '-o', label='Cr ratio')
    co_ratio, = plt.plot([i[0] for i in stat], [i[2] for i in stat], '-o', label='Co ratio')
    ni_ratio, = plt.plot([i[0] for i in stat], [i[3] for i in stat], '-o', label='Ni ratio')
    plt.legend(['Cr ratio', 'Co ratio', 'Ni ratio'])
    plt.savefig('ratio-{}-{}-{}'.format(pickle_name, z_limit_min, z_limit_max) + '.png')


    # # for i, j in [(0, 4), (4, 12), (0, 12), (12, 18), (18, 42)]:
    # for j in range(50):
    #     n_nearest_high = j + 1
    #     ps = get_points_to_draw(blocks)
    #     islands = get_islands_percentage(ps)
    #     # clusters = get_cluster_percentage(ps)
    #     # adjs = get_adjacency_score(ps)
    #     # print("low={}, high={}".format(n_neast_low, n_nearest_high))
    #     # print("islands score: ", islands)
    #     # print("cluster score: ", clusters)
    #     # print("adjacency score: ", adjs)
    #     print("{},{},{},{}".format(j + 1, islands["Cr"], islands["Co"], islands["Ni"]))
