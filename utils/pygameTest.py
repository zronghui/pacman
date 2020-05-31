#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_errors
from pygame import image
from pygame.rect import Rect
from pygame.surface import Surface

pretty_errors.activate()


def xpmToPng(filename):
    img = image.load(f'{filename}.xpm')
    m = Surface((img.get_width(), img.get_height()))
    m.blit(img, Rect(0, 0, img.get_width(), img.get_height()))
    image.save(m, f'{filename}.png')


def subPic(src, dest, x, y):
    img = image.load(src)
    m = Surface((32, 32))
    m.blit(img, Rect(0, 0, 32, 32), Rect(32 * x, 32 * y, 32, 32))
    image.save(m, dest)


if __name__ == '__main__':
    # xpmToPng('tiles')
    subPic('img/tiles.png', 'img/wall.png', 0, 0)
    subPic('img/tiles.png', 'img/floor.png', 0, 1)
    subPic('img/tiles.png', 'img/dot.png', 2, 0)
    subPic('img/tiles.png', 'img/right.png', 3, 0)
    subPic('img/tiles.png', 'img/left.png', 4, 0)
    subPic('img/tiles.png', 'img/down.png', 3, 1)
    subPic('img/tiles.png', 'img/up.png', 4, 1)
    subPic('img/tiles.png', 'img/monster.png', 5, 0)
    subPic('img/tiles.png', 'img/close.png', 5, 1)
