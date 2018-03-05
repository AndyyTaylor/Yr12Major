import numpy as np
import csv

DATASET_PATH = "/Users/andytaylor/Google Drive/Major/data/datasets/"


def load_file(file_name):  # Seperate to lead csv text etc based on extension
    with open(DATASET_PATH + file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
