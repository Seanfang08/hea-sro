from import_to_pickle import *
from visualize_3D_mini import *

# csv_names = ["data/R5081_01402-800C1hWQ tip1/R5081_01402-v02.CSV",
#              "data/R5081_01403-800C1hWQ tip2/R5081_01403-v02.CSV",
csv_names = ["data/R5081_01406-600C3hWQ tip1/R5081_01406-v01.CSV",
             "data/R5081_01407-600C3hWQ tip2/R5081_01407-v01.CSV"]
# csv_names = ["data/data.csv"]

selection_id_template = "{}-{}-{}"
pickle_name_template = "pickles/{}.pickle"
ratio_experiment_template = "ratio-{}"
dist_experiment_template = "dist-{}"
image_addr_template = "images/{}.png"

z_choices = [(10, 20), (20, 30), (30, 40)]


def save_ratio(ps, ratio_experiment_id):
    stat = []
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

    plt.title('{}, z_limit_min={}, z_limit_max={}'.format(pickle_name, z_limit_min, z_limit_max))
    cr_ratio, = plt.plot([i[0] for i in stat], [i[1] for i in stat], '-o', label='Cr ratio')
    co_ratio, = plt.plot([i[0] for i in stat], [i[2] for i in stat], '-o', label='Co ratio')
    ni_ratio, = plt.plot([i[0] for i in stat], [i[3] for i in stat], '-o', label='Ni ratio')
    plt.legend(['Cr ratio', 'Co ratio', 'Ni ratio'])
    plt.savefig(image_addr_template.format(ratio_experiment_id), dpi=300)
    plt.clf()


def save_dist(ps, dist_experiment_id):
    stat = []
    for n_limit in range(1, 20):
        sum_cr = sum_co = sum_ni = count = 0
        for p in (ps['Cr']):
            for np in p.nearest_cr[:n_limit]:
                sum_cr += p.dist(np)
            for np in p.nearest_co[:n_limit]:
                sum_co += p.dist(np)
            for np in p.nearest_ni[:n_limit]:
                sum_ni += p.dist(np)
            count += 1
        stat.append([n_limit, sum_cr / count / n_limit, sum_co / count / n_limit, sum_ni / count / n_limit])

    plt.title('{}, z_limit_min={}, z_limit_max={}'.format(pickle_name, z_limit_min, z_limit_max))
    cr_dist, = plt.plot([i[0] for i in stat], [i[1] for i in stat], '-o', label='Cr avg dist')
    co_dist, = plt.plot([i[0] for i in stat], [i[2] for i in stat], '-o', label='Co avg dist')
    ni_dist, = plt.plot([i[0] for i in stat], [i[3] for i in stat], '-o', label='Ni avg dist')
    plt.legend(['Cr avg dist', 'Co avg dist', 'Ni avg dist'])
    plt.savefig(image_addr_template.format(dist_experiment_id), dpi=300)
    plt.clf()


if __name__ == "__main__":
    for csv_name in csv_names:
        # data_id = csv_name.split('/')[1].split('_')[1].split('-')[0]
        data_id = csv_name.split('/')[1].split('.')[0]

        for z_limit_min, z_limit_max in z_choices:
            selection_id = selection_id_template.format(data_id, z_limit_min, z_limit_max)
            print(selection_id)
            pickle_name = pickle_name_template.format(selection_id)
            blocks = import_data(z_limit_min, z_limit_max)
            ps = get_points_to_draw(blocks, z_limit_min, z_limit_max)

            ratio_experiment_id = ratio_experiment_template.format(selection_id)
            save_ratio(ps, ratio_experiment_id)

            dist_experiment_id = dist_experiment_template.format(selection_id)
            save_dist(ps, dist_experiment_id)

