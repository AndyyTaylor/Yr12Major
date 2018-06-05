
import pygame
import numpy as np

from src import config
from .widget import Widget


class Holder(Widget):

    def __init__(self, x, y, w, h):
        