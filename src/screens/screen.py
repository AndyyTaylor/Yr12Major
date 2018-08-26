
import pygame

from src import config
from ..widgets import Frame, Label, Button, Image
from src.framework.StateRegistry import StateRegistry


class Screen():

    def __init__(self, name, parent, back_color=config.SCHEME5, **kwargs):
        self.name = name
        self.back_color = back_color
        self.parent = StateRegistry.instance().register(self, parent)

        defaults = {
            'back_button': True,
            'show_title': True,
            'back_screen': 'MainMenu'
        }

        for key, val in defaults.items():
            setattr(self, key, kwargs.get(key, val))

        self.widgets = []

        if self.show_title:
            self.title_frame = Frame(0, 0, config.SCREEN_WIDTH, 150, False, config.SCHEME2)
            self.widgets.append(self.title_frame)

            self.title = Label(300, 0, config.SCREEN_WIDTH - 600, 150,
                               config.SCHEME2, self.name, 118, config.BLACK)
            self.title_frame.add_child(self.title)

            if self.back_button:
                back_button = Button(0, 0, 150, 150, "", 72,
                                     config.BLACK, config.SCHEME2, config.SCHEME2, 0,
                                     lambda: self.parent.change_state(self.back_screen),
                                     shape='rect', img=Image(25, 25, 100, 100, "back_arrow.png"))

                self.title_frame.add_child(back_button)

    def on_init(self):
        for widget in self.widgets:
            widget.on_init()

    def on_shutdown(self):
        for widget in self.widgets:
            widget.on_shutdown()

    def on_enter(self, data, screen):
        pygame.draw.rect(screen, self.back_color, screen.get_rect())

        for widget in self.widgets:
            widget.reset_animation()
            widget.on_render(screen)

    def on_exit(self):
        for widget in self.widgets:
            widget.on_exit()

    def on_update(self, elapsed):
        for widget in self.widgets:
            widget.on_update(elapsed)

    def on_render(self, screen):
        moving_rects = []
        for widget in self.widgets:
            if widget.type == 'connection' and widget.has_changed():
                moving_rects.append(pygame.Rect(widget.get_global_rect()))

        self.update_components(moving_rects)

        for widget in self.widgets:
            if widget.has_changed():
                widget.on_render(screen, self.back_color)

    def update_components(self, update_rects):
        if not isinstance(update_rects, list):
            update_rects = [update_rects]

        for widget in self.widgets:
            widget_rect = pygame.Rect(widget.get_global_rect())

            for update_rect in update_rects:
                if widget_rect.colliderect(update_rect):
                    widget.changed = True
                    break

    def on_key_down(self, key):
        for widget in self.widgets:
            widget.on_key_down(key)

    def on_mouse_event(self, event):
        for widget in self.widgets:
            widget.on_mouse_event(event)

    def on_mouse_motion(self, event, pos):
        for widget in self.widgets:
            widget.on_mouse_motion(pos)

    def on_mouse_down(self, event, pos):
        for widget in self.widgets:
            if widget.type == 'frame':
                widget.on_mouse_down(pos)
            elif pygame.Rect(widget.get_rect()).collidepoint(pos):
                if widget.on_click(pos):
                    True

    def on_mouse_up(self, event, pos):
        for widget in self.widgets:
            widget.on_mouse_up(pos)

    def on_scroll(self, is_down, pos):
        for widget in self.widgets:
            if pygame.Rect(widget.get_rect()).collidepoint(pos):
                widget.on_scroll(is_down)
