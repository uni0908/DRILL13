"""Integration checks using a real pico2d canvas and synthetic key events."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pico2d
from sdl2 import (SDL_QUIT, SDL_KEYDOWN, SDL_KEYUP, SDLK_i, SDLK_0, SDLK_1,
                  SDLK_2, SDLK_RIGHT, SDLK_SPACE, SDLK_p, SDLK_ESCAPE)

import game_framework
import game_world
import pause_mode
import play_mode
import title_mode
from ball import Ball


class ItemModeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pico2d.open_canvas()

    @classmethod
    def tearDownClass(cls):
        pico2d.close_canvas()

    def setUp(self):
        game_framework.stack = [play_mode]
        play_mode.init()

    def tearDown(self):
        while game_framework.stack:
            game_framework.stack.pop().finish()

    def key(self, key, event_type=SDL_KEYDOWN, repeat=False):
        event = SimpleNamespace(type=event_type, key=key, repeat=repeat)
        mode = game_framework.stack[-1]
        with patch.object(mode, 'get_events', return_value=[event]):
            mode.handle_events()

    def balls(self):
        return [o for layer in game_world.world for o in layer
                if isinstance(o, Ball)]

    def test_selection_and_live_world(self):
        boy = play_mode.boy
        self.assertEqual(boy.ball_size, 21)
        self.key(SDLK_2)
        self.assertEqual(boy.ball_size, 21)
        self.key(SDLK_SPACE)
        small = self.balls()[0]
        self.key(SDLK_i)
        self.key(SDLK_i, repeat=True)
        self.assertTrue(play_mode.item_window.visible)
        self.key(SDLK_2)
        self.assertFalse(play_mode.item_window.visible)
        self.key(SDLK_SPACE)
        self.assertEqual([b.size for b in self.balls()], [21, 41])
        self.assertIsNot(self.balls()[0].image, self.balls()[1].image)
        x, ball_x, frame = boy.x, small.x, boy.frame
        self.key(SDLK_i)
        self.key(SDLK_RIGHT)
        play_mode.update()
        self.assertGreater(boy.x, x)
        self.assertGreater(small.x, ball_x)
        self.assertNotEqual(boy.frame, frame)
        self.key(SDLK_RIGHT, SDL_KEYUP)
        self.key(SDLK_0)
        self.assertFalse(play_mode.item_window.visible)
        self.key(SDLK_SPACE)
        self.assertEqual(len(self.balls()), 2)
        self.key(SDLK_i)
        self.key(SDLK_i)
        self.assertIsNone(boy.ball_size)
        boy.idle_started_at = pico2d.get_time() - 6
        play_mode.update()
        self.assertEqual(boy.state, 'SLEEP')
        self.key(SDLK_SPACE)
        self.assertEqual(boy.state, 'IDLE')
        self.assertEqual(len(self.balls()), 2)
        self.key(SDLK_1)
        self.assertFalse(play_mode.item_window.visible)
        self.assertEqual(boy.ball_size, 21)
        self.key(SDLK_i)
        self.key(SDLK_2)
        self.key(SDLK_i)
        play_mode.render()
        small.x = pico2d.get_canvas_width() + 1
        play_mode.update()
        self.assertNotIn(small, self.balls())

    def test_pause_and_new_game(self):
        self.key(SDLK_i)
        self.key(SDLK_2)
        self.key(SDLK_i)
        self.key(SDLK_p)
        self.assertIs(game_framework.stack[-1], pause_mode)
        pause_mode.render()
        self.key(SDLK_p)
        self.assertIs(game_framework.stack[-1], play_mode)
        self.assertTrue(play_mode.item_window.visible)
        self.assertEqual(play_mode.boy.ball_size, 41)
        self.key(SDLK_ESCAPE)
        self.assertIs(game_framework.stack[-1], title_mode)
        self.key(SDLK_SPACE)
        self.assertEqual(play_mode.boy.ball_size, 21)
        self.assertFalse(play_mode.item_window.visible)

    def test_quit_with_window_open(self):
        self.key(SDLK_i)
        game_framework.running = True
        with patch.object(play_mode, 'get_events',
                          return_value=[SimpleNamespace(type=SDL_QUIT)]):
            play_mode.handle_events()
        self.assertFalse(game_framework.running)


if __name__ == '__main__':
    unittest.main()
