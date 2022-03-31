from utils import *
from sys import argv
import matplotlib.pyplot as plt
import numpy

# reference
SAMPLE_RATE = 44100
FOOTPRINT_SIZE = 30
TARGET_START = 0.05
TARGET_T = 1.8
TARGET_F = 4000
FFT_WINDOW_SIZE = 0.2
POINT_EFFICIENCY = 0.8

# defaults
default_footprint = 100
default_target_start = 1
default_target_height = 4000
default_target_width = 6


def main(footprint, target_start, target_width, target_height):

    sample = "C:/Users/Ruairi/IdeaProjects/pythonProject/Recording_2.wav"  # argv[1]
    db_hashes = read_hashes("hashes [footprint=" + str(footprint) + "]")
    sample_fingerprint = create_fingerprint(sample, footprint_size=footprint, target_start=target_start, target_height=target_height, target_width=target_width, sample_rate=44100)

    match_times = {1: [], 2: []}
    for sample_hash in sample_fingerprint:
        for db_hash in db_hashes:
            if db_hash["hash"] == sample_hash["hash"]:
                if db_hash["track_id"] in match_times:
                    match_times[db_hash["track_id"]].append(db_hash["time_d"] - sample_hash["time_d"])
                else:
                    match_times[db_hash["track_id"]] = [db_hash["time_d"] - sample_hash["time_d"]]

    fig, (fig1, fig2) = plt.subplots(2)
    n1, bins, patches = fig1.hist(match_times[1])
    n2, bins, patches = fig2.hist(match_times[2])

    #process resulting data
    scores = [numpy.max(n1), numpy.max(n2)]
    plt.savefig("edata/statistics/Invaders-Children histogram [footprint=" + str(footprint) + "].png")
    score_file = open("edata/statistics/Invaders-Children scores.csv", "a")
    score_file.write("Footprint: " + str(footprint) + ",")
    for score in scores:
        score_file.write(score + ",")
    score_file.write("\n")
    score_file.close()
    print(scores)
    print(match_times)
    plt.show()
    #-------------------------

# take command line arguments if given,
# else use defaults
try:
    footprint = argv[1]
except:
    footprint = default_footprint
try:
    target_start = argv[2]
except:
    target_start = default_target_start
try:
    target_height = argv[3]
except:
    target_height = default_target_height
try:
    target_width = argv[4]
except:
    target_width = default_target_width

main(footprint, target_start, target_height, target_width)
