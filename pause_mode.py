import os

from pico2d import *
import game_framework
import game_world


font = None


def init():
    global font
    font = load_font(os.path.join(os.environ.get('WINDIR', 'C:/Windows'),
                                  'Fonts', 'consola.ttf'), 48)


def finish():
    global font
    font = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not getattr(event, 'repeat', False):
                game_framework.pop_mode()
                return


def update():
    pass


def render():
    clear_canvas()
    game_world.render()
    # Consolas is monospaced; five letters at 48px occupy about 144px.
    font.draw(get_canvas_width() / 2 - 72,
              get_canvas_height() / 2, 'pause', (255, 0, 0))
    update_canvas()
