def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print("\n\n")

def generate_spectrogram(filepath, sample_rate=44100, frame_size_seconds=0.2):
    from madmom.audio import Signal
    from madmom.audio.signal import FramedSignal
    from madmom.audio.stft import STFT
    from madmom.audio.spectrogram import Spectrogram

    print("Generating Spectrogram...")
    # frame size is in samples, convert from seconds
    frame_size = frame_size_seconds * sample_rate

    signal = Signal(filepath, num_channels=1, sample_rate=sample_rate, stop=204)
    framed_signal = FramedSignal(signal, hop_size=441, frame_size=frame_size)
    stft = STFT(framed_signal)
    spectrogram = Spectrogram(stft)
    # print(spectrogram.shape)
    # print(framed_signal.shape)
    # print(signal.shape)
    # print("Spectrogram Complete")
    return spectrogram

def show_spectrogram(spectrogram):
    from matplotlib import pyplot as plt
    plt.imshow(spectrogram[:, :].T, aspect='auto', origin='lower')
    return plt

def generate_starmap(spectrogram, footprint):
    import numpy as np
    from scipy.ndimage import maximum_filter

    print("Generating Starmap...")
    filtered_spec = maximum_filter(spectrogram, footprint)
    starmap = np.zeros(spectrogram.shape)
    x = []
    y = []

    for i in range(starmap.shape[0]):
        printProgressBar(i, starmap.shape[0], "Starmap: ", printEnd="")
        for j in range(starmap.shape[1]):
            if spectrogram[i][j] == filtered_spec[i][j] and filtered_spec[i][j] != 0:
                starmap[i][j] = 1
                x.append(i)
                y.append(j)
    print("Starmap Generated!")
    show_starmap(starmap)
    return starmap  # , x, y

def show_starmap(starmap):
    from matplotlib import pyplot as plt
    x_points = []
    y_points = []

    for x in range(starmap.shape[0]):
        for y in range(starmap.shape[1]):
            if starmap[x][y] == 1:
                x_points.append(x)
                y_points.append(y)

    plt.scatter(x_points, y_points)
    plt.show()

    return x_points, y_points

def get_hashes(spectrogram=None, starmap=None, gap=0.05, width=1.8, height=4000, track_id=None):
    print("Getting hashes")
    if height is None:
        height = spectrogram.shape[1] // 3
    frequency_bin_size = 5  # THESE COULD CHANGE BASED ON PARAMETERS
    samples_per_second = 100  # THESE COULD CHANGE BASED ON PARAMETERS

    gap = int(samples_per_second*gap)
    width = int(samples_per_second*width)
    height = int(height//frequency_bin_size)

    hashes = []
    for x in range(starmap.shape[0]):
        printProgressBar(x, starmap.shape[0], "Hashes: ", printEnd="")
        for y in range(starmap.shape[1]):
            if starmap[x][y] == 0:
                continue
            else:
                try:
                    for i in range(int(x + gap), int(x + width)):
                        for j in range(int(y - height // 2), int(y + height // 2)):
                            if int(starmap[i][j]) > 0:
                                # hash = {"anchor frequency": y, "target frequency": j, "time difference": i - x, "time from start": x, "track id": track_id}

                                # this loops j around bottom to top but the try catch won't let it loop the other way
                                if j < 0:
                                    j = starmap.shape[1] - j
                                raw_hash = {"hash": str(y)+"-"+str(j)+"-"+str((i - x)), "track_id": track_id,
                                            "time_d": x}
                                #print("anchor: "+str(x)+","+str(y)+", target: "+str(i)+","+str(j))
                                hashes.append(raw_hash)
                except IndexError:
                    continue
    print("Hashes Generated!")
    return hashes

def create_fingerprint(file, track_id=None, sample_rate=44100, frame_size_seconds=0.2, footprint=None, footprint_size=30, target_start=0.05, target_width=1.8, target_height=4000):
    if footprint is None:
        footprint = (footprint_size, footprint_size)

    spectrogram = generate_spectrogram(file, sample_rate, frame_size_seconds)
    starmap = generate_starmap(spectrogram, footprint)
    fingerprint = get_hashes(spectrogram, starmap, target_start, target_width, target_height, track_id)
    return fingerprint

def match_song(clip, db_hashes):
    from matplotlib import pyplot as plt
    spectrogram = generate_spectrogram(clip)
    starmap = generate_starmap(spectrogram, (50, 50))
    clip_hashes = get_hashes(spectrogram, starmap)

    times = {}

    matched_hashes = []
    for clip_hash in clip_hashes:
        for db_hash in db_hashes:
            if clip_hash["hash"] == db_hash["hash"]:
                #matched_hashes.append({"hash": db_hash, "time_d": (db_hash["time_from_start"] - clip_hash["time_from_start"])})
                if db_hash["track_id"] in times:
                    times[db_hash["track_id"]].append((db_hash["time_from_start"] - clip_hash["time_from_start"]))
                else:
                    times[db_hash["track_id"]] = [(db_hash["time_from_start"] - clip_hash["time_from_start"])]

    fig, (fig1, fig2) = plt.subplots(2)
    n1, bins, patches = fig1.hist(1)
    n2, bins, patches = fig2.hist(2)

    plt.show()

def save_hashes(hashes, filename):
    import json

    with open("edata/"+filename+".json", "w") as file:
        file.write(json.dumps(hashes))
        file.close()

def read_hashes(filename):
    import json

    with open("edata/"+filename+".json", "r") as file:
        return json.load(file)