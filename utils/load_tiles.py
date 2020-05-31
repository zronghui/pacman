#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame import image, Rect, Surface

TILE_POSITIONS = [
    ('#', 0, 0),  # wall
    (' ', 0, 1),  # floor
    ('*', 3, 0),  # eater
    ('.', 2, 0)  # dot
]
DEST_POSITIONS = {
    '#': [0, 0],  # wall
    ' ': [1, 0],  # floor
    '*': [2, 0],  # eater
    '.': [3, 0]  # dot
}

SIZE = 32
_image = 'tiles.xpm'


# tiles.xpm (288, 64)
# explo.xpm (32, 256)
# bg.xpm    (64, 288)

def load_tiles():
    tiles = {}
    tile_img = image.load(_image)
    for tile_position in TILE_POSITIONS:
        symbol, x, y = tile_position
        rect = Rect(x * SIZE, y * SIZE, SIZE, SIZE)
        tiles[symbol] = rect
    return tile_img, tiles


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = Surface((SIZE * len(TILE_POSITIONS), SIZE))
    for tile_position in TILE_POSITIONS:
        symbol, x, y = tile_position
        destx, desty = DEST_POSITIONS[symbol]
        m.blit(tile_img, Rect(destx * SIZE, desty * SIZE, SIZE, SIZE), tiles[symbol])
    image.save(m, 'tile_combo.png')


# class Tile:
#     def __init__(self, achar, x, y):
#         self.char = achar
#
#
# t = Tile('#', 0, 0)
# print(t.char)
