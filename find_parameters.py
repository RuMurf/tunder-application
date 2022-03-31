from os import path, listdir
from matplotlib import pyplot as plt
import numpy as np

db_hashes = {}
client_hashes = {}

# read hashes from files
for filename in listdir("edata/client_hashes"):
    file = path.join("edata/client_hashes")
    client_hashes[filename] = open(file, "r")

for filename in listdir("edata/db_hashes"):
    file = path.join("edata/db_hashes")
    db_hashes[filename] = open(file, "r")

for db_hash in db_hashes:
    for client_hash in client_hashes:

        match_times = {1: [], 2: []}
        for sample_hash in client_hash:
            for db_h in db_hash:
                if db_hash["hash"] == sample_hash["hash"]:
                    if db_hash["track_id"] in match_times:
                        match_times[db_hash["track_id"]].append(db_hash["time_d"] - sample_hash["time_d"])
                    else:
                        match_times[db_hash["track_id"]] = [db_hash["time_d"] - sample_hash["time_d"]]

        fig, (fig1, fig2) = plt.subplots(2)
        n1, bins, patches = fig1.hist(match_times[1])
        n2, bins, patches = fig2.hist(match_times[2])

        # process resulting data
        scores = [np.max(n1), np.max(n2)]
        plt.savefig("edata/statistics/Invaders-Children histogram [db=" + str(db_hash[8:-5]) + ", client=" + str(client_hash[8:-5])+"].png")
        score_file = open("edata/statistics/Invaders-Children scores.csv", "a")
        score_file.write("[db=" + str(db_hash[8:-5]) + ", client=" + str(client_hash[8:-5])+"],")
        for score in scores:
            score_file.write(score + ",")
        score_file.write("\n")
        score_file.close()
        print(scores)
        print(match_times)
        plt.show()
