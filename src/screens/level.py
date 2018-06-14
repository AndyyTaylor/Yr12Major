
import pygame
from src import config
from .screen import Screen
from ..widgets import Frame, Label
from ..components import ColorInput


class Level(Screen):

    def __init__(self):
        super().__init__('Level', 'MasterState', back_screen='LevelSelector')

        self.component_frame = Frame(0, 220, 300, config.SCREEN_HEIGHT - 220, True, config.SCHEME2)
        self.workspace_frame = Frame(310, 160, config.SCREEN_WIDTH - 315,
                                     config.SCREEN_HEIGHT - 170, True, config.SCHEME4)
        # component_frame.add_child()
        self.widgets.append(self.component_frame)
        self.widgets.append(self.workspace_frame)

        self.widgets.append(Label(0, 160, 300, 60, config.SCHEME2, "Components", 36, config.BLACK))

        self.floating_component = None

    def on_enter(self, data, screen):
        super().on_enter(data, screen)

        print("Entering level", data)

        self.component_frame.add_child(ColorInput(10, 10, 3))

    def on_update(self, elapsed):
        super().on_update(elapsed)

        if self.floating_component is not None:
            self.floating_component.on_update(elapsed)

    def on_render(self, screen):
        super().on_render(screen)

        if self.floating_component is not None:
            self.floating_component.on_render(screen)

    def on_mouse_motion(self, event, pos):
        super().on_mouse_motion(event, pos)

        if self.floating_component is None:
            for widget in self.component_frame.children:
                if widget.is_clicked:
                    self.floating_component = widget
                    print(len(self.component_frame.children))
                    self.component_frame.children.remove(widget)
                    print(len(self.component_frame.children))
                    break

            # If not in the component frame
            for widget in self.workspace_frame.children:
                if widget.is_clicked:
                    self.floating_component = widget
                    self.workspace_frame.children.remove(widget)
                    break

        if self.floating_component is not None:
            self.floating_component.set_pos(*pos)

            for widget in self.widgets:
                widget_rect = pygame.Rect(widget.get_rect())
                floating_rect = pygame.Rect(self.floating_component.get_rect())

                if widget_rect.colliderect(floating_rect):
                    widget.changed = True

    def on_mouse_up(self, event, pos):
        super().on_mouse_up(event, pos)

        if self.floating_component is not None:
            workspace_rect = pygame.Rect(self.workspace_frame.get_rect())
            component_rect = pygame.Rect(self.floating_component.get_rect())

            if workspace_rect.colliderect(component_rect):
                self.floating_component.sub_pos(*self.workspace_frame.get_pos())
                self.workspace_frame.add_child(self.floating_component)
            else:
                self.floating_component.sub_pos(*self.component_frame.get_pos())
                self.component_frame.add_child(self.floating_component)

            self.floating_component.is_clicked = False
            self.floating_component = None
