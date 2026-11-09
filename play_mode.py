from pico2d import *
import game_framework
import game_world
import title_mode
import pause_mode
from boy import Boy
from grass import Grass
from item_mode import ItemWindow


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not getattr(event, 'repeat', False):
                game_framework.push_mode(pause_mode)
                return
        else:
            if not item_window.handle_event(event):
                boy.handle_event(event)



def init():
    global boy, item_window


    boy = Boy()
    item_window = ItemWindow(boy)
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)



def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    item_window.draw()
    update_canvas()

def finish():
    game_world.clear()


def pause():
    global pause_started_at
    pause_started_at = get_time()


def resume():
    # Exclude paused time from the boy's idle timer.
    boy.idle_started_at += get_time() - pause_started_at
    # Movement keys may have been released while paused.
    boy.pressed_keys.clear()
    if boy.state == 'RUN':
        boy.dir = 0
        boy.stop_run()



