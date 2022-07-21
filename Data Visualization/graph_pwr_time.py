import csv
from math import *

import numpy as np
from matplotlib import pyplot as plt

src_dir = "data/processed/"
src_files = [
    ["Static Panel", "Trial 2/static_96s.csv"],
    # ["Tracking Panel, 500ms Adjustment Time", "Trial 2/tracker_500ms_96s.csv"],
    # ["Tracking Panel, 1000ms Adjustment Time", "Trial 2/tracker_1000ms_96s.csv"],
    # ["Tracking Panel, 2000ms Adjustment Time", "Trial 2/tracker_2000ms_96s.csv"],
    # ["Tracking Panel, 3000ms Adjustment Time", "Trial 2/tracker_3000ms_96s.csv"],
    # ["Tracking Panel, 4000ms Adjustment Time", "Trial 2/tracker_4000ms_96s.csv"],
    # ["Tracking Panel, 6000ms Adjustment Time", "Trial 2/tracker_6000ms_96s.csv"],
    # ["Tracking Panel, 8000ms Adjustment Time", "Trial 2/tracker_8000ms_96s.csv"],
]
dest_graph_dir = "graphs/Power vs. Time/"


def csv_to_ndarray(filename):
    with open(filename, newline="") as csv_file:
        csv_reader = csv.reader(csv_file)

        data = []
        for row in csv_reader:
            data.append(row)
        return np.array(data, dtype=np.float)


for file in src_files:
    data_array = csv_to_ndarray(src_dir + file[1])
    # print(data_array)
    # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(data_array[:, 0],
            [i[0] * i[1] for i in zip(data_array[:, 1], data_array[:, 1])])  # Plot some data on the axes.
    ax.plot(data_array[:, 0],
            [1.5 * cos(pi / 40 * (i - 40)) for i in data_array[:, 0]], c="pink")  # Plot some data on the axes.
    ax.set_xlabel('Time (seconds)')  # Add an x-label to the axes.

    out_name = f"Power vs. Time, {file[0]}"
    ax.set_ylabel('Power (milliwatts)')  # Add a y-label to the axes.
    ax.set_title(out_name)  # Add a title to the axes.
    ax.set_ybound(0, 2.0)
    ax.set_xbound(0, 96.0)
    ax.set_xticks(np.arange(0, 96 + 1, 4.0))  # setting the ticks

    plt.savefig(dest_graph_dir + out_name + ".png")

    # plt.show()
