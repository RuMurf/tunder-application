from utils import *
from sys import argv
import matplotlib.pyplot as plt
import numpy

footprint = 200
if argv[1] is not None:
    footprint = argv[1]
    print("Using Footprint "+str(argv[1]))

sample = "C:/Users/Ruairi/IdeaProjects/pythonProject/Recording_2.wav"  # argv[1]
db_hashes = read_hashes("hashes")
sample_fingerprint = create_fingerprint(sample, footprint_size=200, target_height=4000, target_start=1, target_width=6, sample_rate=44100)

match_times = {}
match_times[1] = []
match_times[2] = []
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

scores = [numpy.max(n1), numpy.max(n2)]
print(scores)
plt.savefig("Invaders-Children results "+str(footprint)+".png")
plt.show()

print(match_times)








            #if track id exists as key in match_times
                #append db_hash["time_d"] - sample_hash["time_d"] to match_times[db_hash["id"]]
            #else
                #add key db_hash["id"] to match_times
                #