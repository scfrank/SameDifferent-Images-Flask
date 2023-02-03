import csv
import datetime
import glob
import os
from pathlib import Path
import random
import time

# Change file paths to your local paths
PAIRS_CSV = "pairs.csv"

BIRDIMAGES = "static/Images/"

# Writes a new row of data into csv file
# data is: (bird_img1, bird_img2, same?=T/F)
def write_new_row(data, session_id):
    fieldnames = ["session_id", "image1", "image2", "same?"]  # , "different"]
    file_exists = os.path.isfile(PAIRS_CSV)
    with open(PAIRS_CSV, "a", newline="") as csvfile:
        dataWriter = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            restval=0,
            lineterminator="\n",
        )
        if not file_exists:
            dataWriter.writeheader()  # file doesn't exist yet, write a header
        # 'same?' is a boolean column
        row_data = {}
        row_data["session_id"] = session_id
        # either 'same' or 'different' will be in data, depending on buttonpress
        row_data["same?"] = "same" in data.keys()
        if not row_data["same?"]:
            print("row_data", row_data)
            print("data", data)
            assert data["different"] == "Different"
        row_data["image1"] = Path(data["image1"]).name
        row_data["image2"] = Path(data["image2"]).name
        dataWriter.writerow(row_data)


# Checks if a pair of images already exists in CSV file
# (regardless of order)
# UNUSED: each session gets a new random set of images,
# ie. don't worry about duplicates.
def is_pair_labelled(filename1, filename2, CSVPATH):
    with open(CSVPATH, newline="") as csvfile:
        my_content = csv.reader(csvfile, delimiter=",")
        is_labelled = False

        for row in my_content:
            if (filename1 == row[0] and filename2 == row[1]) or (
                filename2 == row[0] and filename1 == row[1]
            ):
                is_labelled = True
                return True
        if not is_labelled:
            return False


# Gets list of image pairs to be labelled (random pairing)
def get_images_labelling_list(N=100):
    """
    Return N pairs of images, chosen at random from static/birds/*jpgs.
    """
    pairs_to_label = set()
    csv_exists = os.path.isfile(PAIRS_CSV)
    images_glob = set(glob.glob(BIRDIMAGES + "/*.jpg"))
    # print("images", len(images_glob))
    # If CSV File Exists
    for i in range(N):
        (f1, f2) = random.sample(images_glob, 2)
        if f1 == f2:
            continue
        if f2 < f1:  # unique pairs by enforcing ordering
            f1, f2 = f2, f1
        if False:  #  if csv_exists:  # don't worry about duplicates anymore
            if not is_pair_labelled(f1, f2, PAIRS_CSV):
                pairs_to_label.add((f1, f2))
        else:
            pairs_to_label.add((f1, f2))
    return list(pairs_to_label)
