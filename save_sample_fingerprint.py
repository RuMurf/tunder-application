from utils import *
import json
from sys import argv

def main(footprint, target_start, target_height, target_width):
    print("footprint: "+str(footprint)+", target start: "+str(target_start)+", targer height: "+str(target_height)+", target width: "+str(target_width))
    sample = "C:/Users/Ruairi/IdeaProjects/pythonProject/Recording_2.wav"
    sample_fingerprint = create_fingerprint(sample, footprint_size=footprint, target_start=target_start,
                                            target_height=target_height, target_width=target_width, sample_rate=44100)
    # write hashes for future reading
    with open("edata/client_hashes/hashes [fp=" + str(footprint) + ",ts=" + str(target_start) + ",th=" + str(
            target_height) + ",tw=" + str(target_width) + "].json", "w") as file:
        file.write(json.dumps(sample_fingerprint))
        file.close()
    print("Hashes Generated: " + str(len(sample_fingerprint)))


# take command line arguments if given,
# else use defaults
try:
    main(int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4]))
except:
    exit(1)