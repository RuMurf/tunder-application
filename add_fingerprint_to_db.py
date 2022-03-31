from utils import *
from sys import argv
import json

# reference
SAMPLE_RATE = 44100
FOOTPRINT_SIZE = 30
POINT_EFFICIENCY = 0.8
TARGET_START = 0.05
TARGET_T = 1.8
TARGET_F = 4000
FFT_WINDOW_SIZE = 0.2

# defaults
default_footprint = 100
default_target_start = 1
default_target_height = 4000
default_target_width = 6

def main(footprint, target_start, target_height, target_width):
    # temporary hard-coded parameters for testing
    directory = "The Number Of The Beast/"
    files = ["01 Invaders.wav", "02 Children Of The Damned.wav"]
    id = 1

    hashes = []
    for file in files:
        hashes += create_fingerprint(directory+file, footprint_size=footprint, target_height=target_height, target_start=target_start, target_width=target_width, sample_rate=44100)
        id += 1

    # write hashes for future reading
    with open("edata/db_hashes/hashes [fp="+str(footprint)+",ts="+str(target_start)+",th="+str(target_height)+",tw="+str(target_width)+"].json", "w") as file:
        file.write(json.dumps(hashes))
        file.close()
    print("Hashes Generated: "+str(len(hashes)))

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

if __name__ == "__main__":
    main(int(footprint), int(target_start), int(target_height), int(target_width))
