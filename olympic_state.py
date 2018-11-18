from pico2d import *
import game_framework
import main_state

from Tile import Bigtile

Title = None

def enter():
    global Title, Player
    if Title == None:
        Title = load_image(".\\icons\\dest1.png")

def exit():
    pass


def pause():
    pass


def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            event.y = main_state.WINDOW_HEIGHT - event.y + 1
            set_dst(event)
        else:
            pass

def update():
    game_framework.stack[0].update()

def draw():
    Title.draw(400, 300)
    game_framework.stack[0].draw()


def set_dst(event):
    global Player
    dst = 14
    for tile in main_state.MAP:
        if type(tile) != Bigtile and tile.isclicked(event.x, event.y) == 1:
            dst = main_state.MAP.index(tile)
            break

    if dst != 14:
        Player.move = dst - Player.index
        if Player.move < 0:
            Player.move = 28 + Player.move
        game_framework.pop_state()