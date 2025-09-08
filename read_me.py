"""
Please adjust configs in this file.
Run "python3 visualize_3D_mini.py" to see 3D plots.
"""


from constants import *


# Choose where to read from and where to save to
csv_name = "data/R5081_01402-800C1hWQ tip1/R5081_01402-v02.CSV"
pickle_name = "data01402n.pickle"


# Choose which part to load to the pickle file
z_limit = 40

z_limit_min = 30
z_limit_max = 40


# Choose which part to display
x_range = (-24, 25)  # x_range should be within (-24, 25)
y_range = (-27, 22)  # y_range should be within (-27, 22)
z_range = (2, 8)  # z_range should be within (2, 8)


# Choose the number of nearest atoms to connect to.
# Lower Bound (Exclusive), Upper Bound (Inclusive) -- When selecting, lb + 1 is the rank of neighbor with index lb.
n_nearest_low = 0
n_nearest_high = 20


# Choose the main element type to analyze (can be 'Cr', 'Co', 'Ni', or 'all_three')
p_type = all_three


# Choose the element type of neighbors to connect to (can be 'Cr', 'Co', 'Ni', or 'all_three')
np_type = either_one


# Choose the threshold for being classified as an island
i_thres = 0.7


# Choose the threshold for being classified as a cluster
c_thres = 1
