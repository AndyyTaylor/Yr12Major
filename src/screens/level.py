
import pygame
import numpy as np

from src import config
from src.ml.environments.game import ColorEnv, DonutEnv, XOREnv

from .screen import Screen
from ..widgets import Frame, Label, Image, Button, Message
from ..components import Input, Output, Connection, KNN, NBayes, LogisticRegression, NeuralNetwork
from ..components import Trash


class Level(Screen):

    def __init__(self):
        super().__init__('Level', 'MasterState', back_screen='LevelSelector')

        self.setup_frames()
        self.setup_score_frame()

        self.widgets.append(Label(0, 160, 300, 60, config.SCHEME2, "Components", 36, config.BLACK))

        self.floating_component = None
        self.drag_offset = (0, 0)

    def on_enter(self, data, screen):
        super().on_enter(data, screen)

        self.component_frame.clear_children()
        self.workspace_frame.clear_children()

        self.component_frame.changed = True
        self.workspace_frame.changed = True
        self.title_frame.changed = True
        self.score_frame.clear_children()
        self.setup_score_frame()

        self.playing = False
        self.play_time = 0

        self.clear_connections()
        self.add_control_buttons()
        self.title.change_text('Level ' + str(data))

        self.load_level(data)
        self.show_level_blurb()

    def on_update(self, elapsed):
        for widget in self.widgets:  # FIX, this will allow components to process while game paused
            if widget.type != 'connection' or self.playing:
                widget.on_update(elapsed)

        if self.floating_component is not None:
            self.floating_component.on_update(elapsed)

        if self.playing:
            if self.is_game_over():
                self.resolve_game()
            else:
                self.update_scores(elapsed)

    def on_render(self, screen):
        super().on_render(screen)

        if self.floating_component is not None:
            self.floating_component.on_render(screen)

    def update_scores(self, elapsed):
        self.play_time += elapsed / 1000
        self.time_label.change_text(int(self.play_time))
        if self.play_time <= self.max_time:
            self.time_label.change_color(config.GREEN)
        else:
            self.time_label.change_color(config.RED)

        self.acc_label.change_text(self.output.get_percentage())
        if self.output.get_raw_percentage() >= self.req_accuracy:
            self.acc_label.change_color(config.GREEN)
        else:
            self.acc_label.change_color(config.RED)

    def is_game_over(self):
        for child in self.workspace_frame.children:
            if isinstance(child, Button) or child.title == 'Trash':
                continue

            # child is a component
            total_data = 0
            for holder in child.inputs + child.outputs:
                total_data += len(holder.samples)

            if total_data > 0:
                return False  # If it's not empty, the game is not over

        if self.floating_component is not None:  # Must also check the floating
            total_data = 0                       # component, if it exists
            for holder in self.floating_component.inputs + self.floating_component.outputs:
                total_data += len(holder.samples)

            if total_data > 0:
                return False

        for widget in self.widgets:  # Connections should also be empty
            if widget.type == 'connection':
                if len(widget.samples) > 0:
                    return False

        return True

    def resolve_game(self):
        won = self.has_won()

        if self.end_frame.hidden:
            width = 250
            height = 450
            x = int(config.SCREEN_WIDTH / 2 - width / 2)
            y = self.workspace_frame.y + self.workspace_frame.h / 2 - height / 2
            self.end_frame = Frame(x, y, width, height,
                                   back_color=config.SCHEME2)

            if won:
                title = 'YOU WON!'
                file = 'trophy.png'
                desc = 'Click anywhere to continue'
            else:
                title = 'YOU LOST'
                file = 'spoon.png'
                desc = 'Click anywhere to retry'

            self.end_frame.add_child(Label(10, 10, width - 20, 70, config.BLACK, title, 48,
                                           config.WHITE))

            self.end_frame.add_child(Image(10, 90, width - 20, height - 50 - 90, file))

            self.end_frame.add_child(Label(10, height - 40, width - 20, 30, config.BLACK,
                                           desc, 16, config.WHITE))

            self.widgets.append(self.end_frame)

    def has_won(self):
        if self.output.get_percentage() == '--%':
            return False

        if self.play_time < self.max_time and self.output.get_raw_percentage() >= self.req_accuracy:
            return True

        return False

    def on_mouse_down(self, event, pos):
        super().on_mouse_down(event, pos)

        if not self.blurb_frame.hidden:  # Should hide the level blurb
            self.blurb_frame.hide()
            self.workspace_frame.changed = True
            self.title_frame.changed = True
        elif not self.end_frame.hidden:  # Should hide the win/loss frame blurb
            self.end_frame.hide()
            self.workspace_frame.changed = True
            self.title_frame.changed = True
            self.widgets.remove(self.end_frame)

            if self.has_won():
                if self.current_level == config.MAX_LEVEL:  # First time completed
                    config.MONEY += 500
                else:
                    config.MONEY += 250

                self.parent.change_state('Level', self.current_level + 1)  # Next level
            else:
                self.stop()  # Restart current level
        elif event.button == 3:
            for widget in self.workspace_frame.children:
                if widget.type == 'component':
                    for holder in widget.inputs + widget.outputs:
                        if holder.hover:
                            self.remove_linked_connections(holder)
                            break

        elif not self.create_connections(pos) and self.floating_component is None:
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

        if self.floating_component:
            self.floating_component.on_mouse_up(pos)

        if self.floating_component is not None:
            self.drop_floating_component()
        else:
            if not self.create_connections(pos, True):
                self.clear_hanging_connection()

    def remove_linked_connections(self, holder):
        to_remove = []
        for widget in self.widgets:
            if widget.type == 'connection':
                if widget.in_holder == holder or widget.out_holder == holder:
                    to_remove.append(widget)

        for widget in to_remove:
            self.widgets.remove(widget)

    def setup_frames(self):
        self.component_frame = Frame(0, 220, 300, config.SCREEN_HEIGHT - 220,
                                     True, config.SCHEME2, grid_type='stack')
        self.workspace_frame = Frame(310, 160, config.SCREEN_WIDTH - 305,
                                     config.SCREEN_HEIGHT - 160, False, config.SCHEME5)
        self.end_frame = Frame(0, self.workspace_frame.y, 200, 200, back_color=config.SCHEME2)
        self.end_frame.hide()

        border1 = Frame(0, 150, config.SCREEN_WIDTH, 10, back_color=config.SCHEME5)
        border2 = Frame(300, 160, 10, config.SCREEN_HEIGHT - 160, back_color=config.SCHEME5)

        self.widgets.append(self.component_frame)
        self.widgets.append(self.workspace_frame)

        self.widgets.append(border1)
        self.widgets.append(border2)

    def setup_score_frame(self):
        self.score_frame = Frame(config.SCREEN_WIDTH - 340, 0, 340, 150, back_color=config.SCHEME4)
        self.score_frame.add_child(Label(0, 0, 340, 50, None, "Score", 36, config.BLACK))

        self.score_frame.add_child(Label(5, 50, 100, 40, None, "Accuracy", 30,
                                         config.BLACK, align='lc'))
        self.score_frame.add_child(Label(5, 90, 100, 40, None, "Time", 30,
                                         config.BLACK, align='lc'))

        self.acc_label = Label(160, 50, 80, 40, config.SCHEME4, "--%", 30, config.BLACK, align='lc')
        self.time_label = Label(160, 90, 80, 40, config.SCHEME4, '0', 30, config.BLACK, align='lc')

        self.score_frame.add_child(self.acc_label)
        self.score_frame.add_child(self.time_label)

        self.score_frame.add_child(Label(240, 50, 60, 40, config.SCHEME4, '/', 30, config.BLACK,
                                         align='lc'))
        self.score_frame.add_child(Label(240, 90, 60, 40, config.SCHEME4, '/', 30, config.BLACK,
                                         align='lc'))

        self.req_acc_label = Label(270, 50, 60, 40, config.SCHEME4, '--%', 30, config.BLACK,
                                   align='lc')
        self.max_time_label = Label(270, 90, 60, 40, config.SCHEME4, '--', 30, config.BLACK,
                                    align='lc')

        self.score_frame.add_child(self.req_acc_label)
        self.score_frame.add_child(self.max_time_label)

        self.title_frame.add_child(self.score_frame)

    def show_level_blurb(self):
        width = 600
        height = 600
        x = int(config.SCREEN_WIDTH / 2 - width / 2)
        y = self.workspace_frame.y + self.workspace_frame.h / 2 - height / 2
        blurb_frame = Frame(x, y, width, height, back_color=config.SCHEME2)

        blurb_frame.add_child(Label(10, 10, width - 20, 70, config.BLACK, self.level_title, 48,
                                    config.WHITE))
        blurb_frame.add_child(Message(10, 80, width - 20, height - 90, config.BLACK,
                                      self.level_description, 24, config.WHITE, align='ll'))
        blurb_frame.add_child(Label(10, 560, width - 20, 30, config.BLACK,
                                    'Click anywhere to continue...', 16, config.WHITE))

        self.blurb_frame = blurb_frame
        self.widgets.append(blurb_frame)

    def create_connections(self, pos, mouse_up=False):
        holders = []
        for widget in self.workspace_frame.children:  # Get all the holders
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
        for widget in self.widgets:  # See connection can be connected to holder
            if widget.type == 'connection':
                if widget.in_holder is None and touching_holder.holder_type == 'output':
                    widget.in_holder = touching_holder
                    connected = True
                    break
                elif widget.out_holder is None and touching_holder.holder_type == 'input':
                    widget.out_holder = touching_holder
                    connected = True
                    break

        if not connected and not mouse_up:  # Place floating connection
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
        # First check the component frame
        for widget in self.component_frame.children:
            if widget.is_clicked and widget.type == 'component':
                widget.add_pos(*self.component_frame.get_pos())
                widget.add_pos(*self.component_frame.get_scroll())
                self.drag_offset = np.subtract(pos, widget.get_pos())
                self.floating_component = widget
                self.floating_component.parent = None
                self.component_frame.children.remove(widget)
                return

        # If not in the component frame
        for widget in self.workspace_frame.children:
            if widget.is_clicked and widget.type == 'component':
                widget.add_pos(*self.workspace_frame.get_pos())
                widget.add_pos(*self.workspace_frame.get_scroll())
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

        if c_frame_intersect.size + w_frame_intersect.size == 0:  # doesn't intersect
            pass
        elif c_frame_intersect.size > w_frame_intersect.size:  # Mostly over component frame
            self.floating_component.sub_pos(*self.component_frame.get_pos())
            self.floating_component.sub_pos(*self.component_frame.get_scroll())
            self.component_frame.add_child(self.floating_component)
        else:  # Mostly over workspace_frame
            self.floating_component.sub_pos(*self.workspace_frame.get_pos())
            self.floating_component.sub_pos(*self.workspace_frame.get_scroll())
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
        stop_button = Button(config.SCREEN_WIDTH - 90 - 310, 0, 80, 80, "", 72,
                             config.BLACK, config.BLACK, config.SCHEME2, 5,
                             self.stop,
                             img=Image(15, 15, 50, 50, "stop.png"))
        self.workspace_frame.add_child(stop_button)

        pause_button = Button(config.SCREEN_WIDTH - 180 - 310, 0, 80, 80, "", 72,
                              config.BLACK, config.BLACK, config.SCHEME2, 5,
                              self.pause,
                              img=Image(15, 15, 50, 50, "pause.png"))
        self.workspace_frame.add_child(pause_button)

        play_button = Button(config.SCREEN_WIDTH - 270 - 310, 0, 80, 80, "", 72,
                             config.BLACK, config.BLACK, config.SCHEME2, 5,
                             self.play,
                             img=Image(15, 15, 50, 50, "play.png"))
        self.workspace_frame.add_child(play_button)

    def play(self):
        self.playing = True
        for widget in self.workspace_frame.children + self.component_frame.children:
            if widget.type == 'component':
                widget.train(self.environment.trainX, self.environment.trainy)

    def pause(self):
        self.playing = False

    def stop(self):
        self.playing = False
        self.play_time = 0

        self.output.reset_stats()
        self.clear_components()
        self.update_scores(0)

    def clear_components(self):
        for widget in self.workspace_frame.children + self.widgets:
            if widget.type == 'component':
                widget.clear_holders()
            elif widget.type == 'connection':
                widget.clear_samples()

    def load_level(self, num):
        config.MAX_LEVEL = max(config.MAX_LEVEL, num)
        self.current_level = num
        self.level_title = ''
        self.level_description = ''

        with open("data/assets/level_text.txt") as f:
            while self.level_title == '' or self.level_description == '':
                line = f.readline().strip()
                if int(line) == num:
                    self.level_title = f.readline().strip()
                    self.level_description = f.readline().strip()
                    self.req_accuracy = int(f.readline().strip())
                    self.max_time = int(f.readline().strip())

                    break
                else:
                    # Skip over the current title, desc etc
                    for i in range(4):
                        f.readline()

        if num == 1:
            self.environment = ColorEnv(1, num_samples=3)  # Can't easily load these from file
        elif num == 2:
            self.environment = ColorEnv(2, target_y=0, num_samples=10)
            if 'Naive Bayes' not in config.PURCHASES:
                config.PURCHASES.append('Naive Bayes')
        elif num == 3:
            self.environment = ColorEnv(2, target_y=1, num_samples=30)
        elif num == 4:
            self.environment = ColorEnv(2, target_y=1, num_samples=50)
        elif num == 5:
            self.environment = ColorEnv(3, target_y=2, num_samples=25)
        elif num == 6:
            self.environment = DonutEnv(num_samples=25)
        elif num == 7:
            self.environment = XOREnv(num_samples=25)
        elif num == 7:
            """
            Handwritten Digit Recognition (Easy)
            Slightly modified MNIST dataset
            """
        elif num == 7:
            """
            - Fashion MNIST
            - World cup man of the match
            - Fruit recognition
            - Soccer match prediction with post-game stats (excluding scores)
            - Soccer match prediction with post-game stats (excluding scores & attempts)
            - Soccer match prediction without post-game stats
            """
        else:
            raise NotImplementedError("Can't find level", num)

        self.req_acc_label.change_text(str(self.req_accuracy) + '%')
        self.max_time_label.change_text(self.max_time)

        self.component_frame.add_child(Input(10, 10, self.environment))

        self.output = Output(10, 300, self.environment)
        self.component_frame.add_child(self.output)
        self.component_frame.add_child(Trash(10, 10, self.output))

        # Add unlocked algorithms
        algorithms = {
            'Logistic Regression': LogisticRegression(self.environment),
            'Neural Network': NeuralNetwork(self.environment),
            'KNN': KNN(self.environment),
            'Naive Bayes': NBayes(self.environment)
        }

        for name, algo in algorithms.items():
            if name in config.PURCHASES:
                self.component_frame.add_child(algo)
