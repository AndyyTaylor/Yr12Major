" Main Menu "

import pygame
from .screen import Screen
from ..elements import *
from ..screen_components import *
from src import config


class MainMenu(Screen):
    " A "

    def __init__(self):
        super().__init__("MainMenu", "MasterState")

        self.total_time = 0
        w = 400
        h = 100
        # self.elements = [
        #     RoundedButton(50, 470, w, h, 3, config.BLACK, config.SCHEME2, lambda: self.parent.change_state("LevelSelector")),
        #     Textbox(50, 470, w, h, "Resume", config.BLACK, 62),
        #     RoundedButton(50, 590, w, h, 3, config.BLACK, config.SCHEME2, lambda: print("Not Implemented")),
        #     Textbox(50, 590, w, h, "Load", config.BLACK, 62),
        #     RoundedButton(50, 710, w, h, 3, config.BLACK, config.SCHEME2, lambda: print("Not Implemented")),
        #     Textbox(50, 710, w, h, "About", config.BLACK, 62)
        # ]

        play_button = Button.create_rounded_button(
                        50, 470, w, h, config.BLACK, config.SCHEME2, 3,
                        "Play", config.BLACK, 62,
                        lambda: self.parent.change_state("LevelSelector")
                      )

        load_button = Button.create_rounded_button(
                        50, 590, w, h, config.BLACK, config.SCHEME2, 3,
                        "Load", config.BLACK, 62,
                        lambda: print("Not Implemented")
                      )

        about_button = Button.create_rounded_button(
                        50, 710, w, h, config.BLACK, config.SCHEME2, 3,
                        "About", config.BLACK, 62,
                        lambda: print("Not Implemented")
                       )

        self.components = [
            play_button,
            load_button,
            about_button
        ]

        self.fps = Textbox(1300, 10, 140, 80, "00", config.BLACK, 72)

    def on_init(self):
        print("Application started.")

    def on_shutdown(self):
        print("Application closed.")

    def on_enter(self, _, screen):
        pygame.draw.rect(screen, config.SCHEME5, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        for comp in self.components + [self.fps]:
            comp.changed = True

    def on_exit(self):
        print("Intro state exited")

    def on_update(self, elapsed):
        for comp in self.components + [self.fps]:
            comp.on_update(elapsed)

        self.fps.set_text(str(int(1000 / elapsed)))

    def on_render(self, screen):
        changed_rectangles = []
        for comp in self.components + [self.fps]:
            if comp.has_changed():
                changed_rectangles.append(comp.get_rect())

        for rect in changed_rectangles:
            pygame.draw.rect(screen, config.SCHEME5, rect)

        for comp in self.components + [self.fps]:
            if comp.has_changed():
                comp.on_render(screen)

        # self.fps.on_render(screen)

    def on_mouse_down(self, event, pos):
        for comp in self.components:
            if isinstance(comp, Button) and pygame.Rect(comp.get_rect()).collidepoint(pos):
                comp.on_click()
                return

    def on_mouse_up(self, event, pos):
        pass

    def on_mouse_motion(self, event, pos):
        for comp in self.components:
            comp.on_mouse_motion(pos)
