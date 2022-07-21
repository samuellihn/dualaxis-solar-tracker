import csv
import numpy as np
from datetime import datetime

src_dir = "data/raw/"
dest_dir = "data/processed/"
src_files = [
    "Trial 1/static_96s.csv",
    "Trial 1/tracker_1000ms_96s.csv",
    "Trial 1/tracker_2000ms_96s.csv",
    "Trial 1/tracker_3000ms_96s.csv",
    "Trial 1/tracker_4000ms_96s.csv",
    "Trial 1/tracker_500ms_96s.csv",
    "Trial 1/tracker_6000ms_96s.csv",
    "Trial 1/tracker_8000ms_96s.csv",
    "Trial 2/static_96s.csv",
    "Trial 2/tracker_1000ms_96s.csv",
    "Trial 2/tracker_2000ms_96s.csv",
    "Trial 2/tracker_3000ms_96s.csv",
    "Trial 2/tracker_4000ms_96s.csv",
    "Trial 2/tracker_500ms_96s.csv",
    "Trial 2/tracker_6000ms_96s.csv",
    "Trial 2/tracker_8000ms_96s.csv",
]


def process_row(row, zero_ts):
    ts = datetime.fromisoformat(row[0])
    return [(ts - zero_ts).total_seconds()] + list(map(float, row[1:4]))


for src_file in src_files:
    data = []
    with open(src_dir + src_file, newline='') as csv_file_in:
        csv_reader = csv.reader(csv_file_in)

        for row in csv_reader:
            if csv_reader.line_num == 1:
                pass
            elif csv_reader.line_num == 2:
                zero_ts = datetime.fromisoformat(row[0])
                process_row(row, zero_ts)
            else:
                data.append(process_row(row, zero_ts))

    with open(dest_dir + src_file,  "w+", newline="", ) as csv_file_out:
        csv_writer = csv.writer(csv_file_out)
        csv_writer.writerows(data)

