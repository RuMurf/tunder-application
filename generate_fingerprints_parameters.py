import save_sample_fingerprint
import add_fingerprint_to_db

parameters = {
    "footprint": [500, 300, 100, 50],
    "target_start": [1, 0.5, 0.05],
    "target_height": [1000, 2000, 3000, 4000],
    "target_width": [1.8, 2, 4, 6]
}

for footprint in parameters["footprint"]:
    for target_start in parameters["target_start"]:
        for target_height in parameters["target_height"]:
            for target_width in parameters["target_width"]:
                save_sample_fingerprint.main(footprint, target_start, target_height, target_width)
                add_fingerprint_to_db.main(footprint, target_start, target_height, target_width)
