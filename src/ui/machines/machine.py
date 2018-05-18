
import pygame
from ..components.component import Component
from src import config


class Holder(Component):

    def __init__(self, x, y, w, h, machine):
        super().__init__(x, y, w, h)

        self.machine = machine
        self.clicked = False
        self.hover = False
        self.alphaCover = pygame.Surface((self.w, self.h))
        self.alphaCover.set_alpha(128)
        self.alphaCover.fill(config.WHITE)

        self.data = []

        self.prev_hash = None

    def on_update(self, elapsed):
        new_hash = hash((self.hover))

        if new_hash != self.prev_hash:
            self.changed = True

            self.prev_hash = new_hash

    def add_data(self, data):
        if isinstance(data, list):
            self.data += data
        else:
            self.data.append(data)

    def take_data(self):
        return self.data.pop()

    def has_data(self):
        return len(self.data) > 0

    def on_mouse_down(self, pos):
        self.clicked = pygame.Rect(self.get_rect()).collidepoint(pos)
        return self.clicked

    def on_mouse_up(self, pos):
        ret = self.clicked or pygame.Rect(self.get_rect()).collidepoint(pos)

        self.clicked = False

        return ret

    def _on_mouse_motion(self, pos):
        self.hover = pygame.Rect(self.get_rect()).collidepoint(pos)

    def on_render(self, screen):
        pygame.draw.rect(screen, config.SCHEME3, self.get_rect())

        if self.hover or self.clicked:
            screen.blit(self.alphaCover, (self.x, self.y))

        self.changed = False


class Machine(Component):

    def __init__(self, x, y, w, h, cloneable=True):
        super().__init__(x, y, w, h)

        self.cloneable = cloneable
        self.clicked = False
        self.isalgorithm = False

        self.slot_width = 40
        self.slot_height = 30

        self.inputs = []
        self.input_pos = []
        self.input_labels = []
        self.outputs = []
        self.output_pos = []
        self.output_labels = []

        self.mouse_offset_x = None
        self.mouse_offset_y = None

        self.text = None

    def on_update(self, elapsed):
        for holder in self.inputs + self.outputs:
            holder.on_update(elapsed)

    def on_render(self, screen, **kwargs):
        self.draw_rounded_rect(screen, self.get_rect(), config.SCHEME4)

        for i, input in enumerate(self.inputs):
            input.on_render(screen)
            if i < len(self.input_labels):
                self.render_data(screen, input.x + input.w/2, input.y + input.h/2, self.input_labels[i], 10)

        for i, output in enumerate(self.outputs):
            output.on_render(screen)
            if i < len(self.output_labels):
                self.render_data(screen, output.x + output.w/2, output.y + output.h/2, self.output_labels[i], 10)

        self.changed = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y

        self.text.x = x
        self.text.y = y

        for o in range(len(self.outputs)):
            out = self.outputs[o]

            out.x = x + self.output_pos[o][0]
            out.y = y + self.output_pos[o][1]

        for i in range(len(self.inputs)):
            inp = self.inputs[i]

            inp.x = x + self.input_pos[i][0]
            inp.y = y + self.input_pos[i][1]

    def setup_inputs_and_outputs(self):
        for out in self.output_pos:
            self.outputs.append(Holder(*out, self.slot_width, self.slot_height, self))

        for inp in self.input_pos:
            self.inputs.append(Holder(*inp, self.slot_width, self.slot_height, self))

    def on_mouse_down(self, pos):
        clicked_holder = False
        for holder in self.inputs + self.outputs:
            clicked_holder = holder.on_mouse_down(pos)
            if clicked_holder:
                return

        if not clicked_holder and pygame.Rect(self.get_rect()).collidepoint(pos):
            self.clicked = True
            self.mouse_offset_x = pos[0] - self.x
            self.mouse_offset_y = pos[1] - self.y

    def on_mouse_up(self, pos):
        self.clicked = False

        input = None  # is this necessary
        output = None
        for holder in self.inputs:
            if holder.on_mouse_up(pos):
                input = holder

        for holder in self.outputs:
            if holder.on_mouse_up(pos):
                output = holder

        return input, output

    def _on_mouse_motion(self, pos):
        if self.clicked and not self.cloneable:
            self.set_pos(pos[0] - self.mouse_offset_x, pos[1] - self.mouse_offset_y)

        for holder in self.inputs + self.outputs:
            holder._on_mouse_motion(pos)

    def clone(self, mpos, labels, render_data):
        if self.isalgorithm:
            new_comp = self.__class__(labels, render_data)
        else:
            new_comp = self.__class__()

        new_comp.clicked = True
        new_comp.cloneable = False
        new_comp.set_pos(*self.get_pos())
        new_comp.mouse_offset_x = mpos[0] - new_comp.x
        new_comp.mouse_offset_y = mpos[1] - new_comp.y

        return new_comp

    def has_changed(self):
        holder_changed = False
        for holder in self.inputs + self.outputs:
            holder_changed = holder.has_changed()

            if holder_changed:
                break

        return self.changed or holder_changed

    def has_data(self):
        for holder in self.inputs + self.outputs:
            if holder.has_data():
                return True

        return False

    def train(self, trainX, trainy):
        pass

    def draw_rounded_rect(self, surface, rect, color, radius=0.1):
        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)

        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """
        pos = (rect[0], rect[1])

        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*radius)]*2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        return surface.blit(rectangle, pos)
