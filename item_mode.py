"""Non-blocking item overlay owned by play_mode."""
import os

from pico2d import (draw_rectangle, get_canvas_height, get_canvas_width,
                    load_font, load_image)
from sdl2 import SDL_KEYDOWN, SDLK_i, SDLK_0, SDLK_1, SDLK_2


class ItemWindow:
    def __init__(self, boy):
        self.boy = boy
        self.visible = False
        font_path = os.path.join(os.environ.get('WINDIR', 'C:/Windows'),
                                 'Fonts', 'consola.ttf')
        self.font = load_font(font_path, 16)
        self.images = {size: load_image(f'ball{size}x{size}.png')
                       for size in (21, 41)}

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_i:
            if not getattr(event, 'repeat', False):
                self.visible = not self.visible
            return True
        choices = {SDLK_0: None, SDLK_1: 21, SDLK_2: 41}
        if (self.visible and event.type == SDL_KEYDOWN and
                event.key in choices):
            self.boy.ball_size = choices[event.key]
            return True
        return False

    def draw(self):
        if not self.visible:
            return
        right = get_canvas_width() - 16
        top = get_canvas_height() - 16
        left, bottom = right - 264, top - 224
        draw_rectangle(left, bottom, right, top, 24, 32, 48, filled=True)
        draw_rectangle(left, bottom, right, top, 100, 190, 230)
        self.font.draw(left + 14, top - 24, 'ITEMS       [I] Close',
                       (225, 240, 255))
        for index, (size, label) in enumerate(
                ((None, '0  Clear'), (21, '1  Ball 21x21'),
                 (41, '2  Ball 41x41'))):
            y = top - 64 - index * 52
            if self.boy.ball_size == size:
                draw_rectangle(left + 8, y - 23, right - 8, y + 23,
                               50, 86, 108, filled=True)
                draw_rectangle(left + 8, y - 23, right - 8, y + 23,
                               100, 220, 200)
            self.font.draw(left + 18, y - 5, label, (240, 240, 240))
            if size is not None:
                self.images[size].draw(right - 38, y, size, size)
        self.font.draw(left + 14, bottom + 12, 'Game keeps running',
                       (140, 210, 180))
