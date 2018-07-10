
import pygame
import numpy as np

from src import config
from src.ml.environments.game import ColorEnv

from .screen import Screen
from ..widgets import Frame, Label, Image, Button
from ..components import Input, Output, Connection, KNN


class Level(Screen):

    def __init__(self):
        super().__init__('Level', 'MasterState', back_screen='LevelSelector')

        self.component_frame = Frame(0, 220, 300, config.SCREEN_HEIGHT - 220,
                                     True, config.SCHEME2, gridded=True)
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

        self.component_frame.clear_children()
        self.workspace_frame.clear_children()

        self.component_frame.changed = True
        self.workspace_frame.changed = True

        self.playing = False

        self.clear_connections()
        self.add_control_buttons()
        self.title.change_text('Level ' + str(data))
        # self.component_frame.add_child(Input(10, 10, 3))
        # self.component_frame.add_child(Output(10, 300))

        self.load_level(data)

    def on_update(self, elapsed):
        for widget in self.widgets:
            if widget.type != 'connection' or self.playing:
                widget.on_update(elapsed)

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
            if not self.create_connections(pos, True):
                self.clear_hanging_connection()

    def create_connections(self, pos, mouse_up=False):
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
                if widget.in_holder is None and touching_holder.holder_type == 'output':
                    widget.in_holder = touching_holder
                    connected = True
                    break
                elif widget.out_holder is None and touching_holder.holder_type == 'input':
                    widget.out_holder = touching_holder
                    connected = True
                    break

        if not connected and not mouse_up:  # TODO must check type of holder
            if holder.holder_type == 'output':
                self.widgets.append(Connection(holder, None, self.environment.render_data))
            else:
                self.widgets.append(Connection(None, holder, self.environment.render_data))

        return True

    def clear_hanging_connection(self):
        for widget in self.widgets:
            if widget.type == 'connection':
                if widget.in_holder is None or widget.out_holder is None:
                    self.widgets.remove(widget)
                    self.workspace_frame.changed = True
                    break

    def select_floating_component(self, pos):
        for widget in self.component_frame.children:
            if widget.is_clicked and widget.type == 'component':
                widget.add_pos(*self.component_frame.get_pos())
                self.drag_offset = np.subtract(pos, widget.get_pos())
                self.floating_component = widget
                self.floating_component.parent = None
                self.component_frame.children.remove(widget)
                return

        # If not in the component frame
        for widget in self.workspace_frame.children:
            if widget.is_clicked and widget.type == 'component':
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

    def clear_connections(self):
        connections = []
        for widget in self.widgets:
            if widget.type == 'connection':
                connections.append(widget)

        for conn in connections:
            self.widgets.remove(conn)

    def add_control_buttons(self):
        pause_button = Button(config.SCREEN_WIDTH - 90 - 310, 0, 80, 80, "", 72,
                              config.BLACK, config.BLACK, config.SCHEME2, 5,
                              self.pause,
                              img=Image(15, 15, 50, 50, "pause.png"))
        self.workspace_frame.add_child(pause_button)

        play_button = Button(config.SCREEN_WIDTH - 180 - 310, 0, 80, 80, "", 72,
                             config.BLACK, config.BLACK, config.SCHEME2, 5,
                             self.play,
                             img=Image(18, 15, 50, 50, "play.png"))
        self.workspace_frame.add_child(play_button)

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def load_level(self, num):
        if num == 1:
            self.environment = ColorEnv(1, num_samples=5)
        elif num == 2:
            self.environment = ColorEnv(2, target_y=1)
        elif num == 3:
            self.environment = ColorEnv(3, target_y=2)
        else:
            raise NotImplementedError("Can't find level", num)

        self.component_frame.add_child(Input(10, 10, self.environment))
        self.component_frame.add_child(Output(10, 300, self.environment))
        self.component_frame.add_child(KNN(self.environment))
