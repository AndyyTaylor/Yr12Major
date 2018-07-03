
import pygame
import numpy as np
from src import config
from .screen import Screen
from ..widgets import Frame, Label
from ..components import ColorInput, Output, Connection


class Level(Screen):

    def __init__(self):
        super().__init__('Level', 'MasterState', back_screen='LevelSelector')

        self.component_frame = Frame(0, 220, 300, config.SCREEN_HEIGHT - 220, True, config.SCHEME2)
        self.workspace_frame = Frame(310, 160, config.SCREEN_WIDTH - 305,
                                     config.SCREEN_HEIGHT - 160, True, config.SCHEME5)

        border1 = Frame(0, 150, config.SCREEN_WIDTH, 10, back_color=config.SCHEME5)
        border2 = Frame(300, 160, 10, config.SCREEN_HEIGHT - 160, back_color=config.SCHEME5)

        self.widgets.append(border1)
        self.widgets.append(border2)

        self.widgets.append(self.component_frame)
        self.widgets.append(self.workspace_frame)

        self.widgets.append(Label(0, 160, 300, 60, config.SCHEME2, "Components", 36, config.BLACK))

        self.floating_component = None
        self.drag_offset = (0, 0)

    def on_enter(self, data, screen):
        super().on_enter(data, screen)

        print("Entering level", data)

        self.component_frame.clear_children()
        self.component_frame.add_child(ColorInput(10, 10, 3))
        self.component_frame.add_child(Output(10, 300))

    def on_update(self, elapsed):
        super().on_update(elapsed)

        if self.floating_component is not None:
            self.floating_component.on_update(elapsed)

    def on_render(self, screen):
        super().on_render(screen)

        if self.floating_component is not None:
            self.floating_component.on_render(screen)

    def on_mouse_down(self, event, pos):
        super().on_mouse_down(event, pos)

        if not self.create_connections(pos) and self.floating_component is None:
            self.select_floating_component(pos)

    def on_mouse_motion(self, event, pos):
        super().on_mouse_motion(event, pos)

        if self.floating_component is not None:
            self.floating_component.set_pos(*np.subtract(pos, self.drag_offset))

            for widget in self.widgets:
                widget_rect = pygame.Rect(widget.get_rect())
                floating_rect = pygame.Rect(self.floating_component.get_prev_rect())

                if widget_rect.colliderect(floating_rect):
                    widget.changed = True

    def on_mouse_up(self, event, pos):
        super().on_mouse_up(event, pos)

        if self.floating_component is not None:
            self.drop_floating_component()
        else:
            self.create_connections(pos)

    def create_connections(self, pos):
        holders = []
        for widget in self.workspace_frame.children:
            if widget.type == 'component':
                for child in widget.children:
                    if child.type == 'holder':
                        holders.append(child)

        touching_holder = None
        for holder in holders:
            if pygame.Rect(holder.get_global_rect()).collidepoint(pos):
                touching_holder = holder
                break

        if touching_holder is None:
            return False

        connected = False
        for widget in self.widgets:
            if widget.type == 'connection':
                if widget.in_holder is None:
                    widget.in_holder = touching_holder
                    connected = True
                    break
                elif widget.out_holder is None:
                    widget.out_holder = touching_holder
                    connected = True
                    break

        if not connected:
            self.widgets.append(Connection(holder, None))

        return True

    def select_floating_component(self, pos):
        for widget in self.component_frame.children:
            if widget.is_clicked:
                widget.add_pos(*self.component_frame.get_pos())
                self.drag_offset = np.subtract(pos, widget.get_pos())
                self.floating_component = widget
                self.floating_component.parent = None
                self.component_frame.children.remove(widget)
                return

        # If not in the component frame
        for widget in self.workspace_frame.children:
            if widget.is_clicked:
                widget.add_pos(*self.workspace_frame.get_pos())
                self.drag_offset = np.subtract(pos, widget.get_pos())
                self.floating_component = widget
                self.floating_component.parent = None
                self.workspace_frame.children.remove(widget)
                return

    def drop_floating_component(self):
        workspace_rect = pygame.Rect(self.workspace_frame.get_rect())
        component_rect = pygame.Rect(self.floating_component.get_rect())
        component_frame_rect = pygame.Rect(self.component_frame.get_rect())

        c_frame_intersect = component_frame_rect.clip(component_rect)
        w_frame_intersect = workspace_rect.clip(component_rect)

        self.update_components(pygame.Rect(self.floating_component.get_global_rect()))

        if c_frame_intersect.size + w_frame_intersect.size == 0:
            pass
        elif c_frame_intersect.size > w_frame_intersect.size:
            self.floating_component.sub_pos(*self.component_frame.get_pos())
            self.component_frame.add_child(self.floating_component)
        else:
            self.floating_component.sub_pos(*self.workspace_frame.get_pos())
            self.workspace_frame.add_child(self.floating_component)

        self.floating_component.is_clicked = False
        self.floating_component = None
