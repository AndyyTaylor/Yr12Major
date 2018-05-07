
import pygame
from ..ui.UIElement import UIElement
from .. import config
from .component import Component


class KNN(Component):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
