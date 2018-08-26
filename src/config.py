import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__)).replace("src", "")
DATASET_PATH = DIR_PATH + "data/datasets/"

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

SCHEME1 = (222, 66, 82)  # RED
SCHEME2 = (246, 241, 215)  # CREAME
SCHEME3 = (183, 224, 228)  # V L BLUE
SCHEME4 = (129, 155, 180)  # BLUE PURPLE
SCHEME5 = (69, 67, 67)  # BLACK

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 860

MAX_LEVEL = 5
COOLDOWN_MODIFIER = 500000

SCROLL_SPEED = 30

DISABLED_ALPHA = 50

TRAIN_PERC = 0.7
TEST_PERC = 1 - TRAIN_PERC

PREDICT_MULTIPLIER = 500
TRAIN_MULTIPLIER = 10

PURCHASES = ['KNN']
MONEY = 0
