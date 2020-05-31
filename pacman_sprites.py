#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import pretty_errors
import pygame

from pygame.locals import *

pretty_errors.activate()

xTiles = 10
yTiles = xTiles
FRAME_PER_SEC = 5
MONSTER_NUM = 1

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y, speed=32):
        super().__init__()
        self.image = pygame.image.load(image_name).convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.image.get_rect(left=32 * x, top=32 * y)
        self.speed = speed
        self.direction = None

    def next(self, direction):
        newx = newy = oldx = oldy = 0
        if direction == 'right':
            oldx = self.rect.x
            newx = self.rect.x + self.speed
            oldy = newy = self.rect.y
        if direction == 'left':
            oldx = self.rect.x
            newx = self.rect.x - self.speed
            oldy = newy = self.rect.y
        if direction == 'down':
            oldy = self.rect.y
            newy = self.rect.y + self.speed
            oldx = newx = self.rect.x
        if direction == 'up':
            oldy = self.rect.y
            newy = self.rect.y - self.speed
            oldx = newx = self.rect.x
        return newx, newy, oldx, oldy

    def update(self, walls=None):
        if not self.direction:
            return
        if self.connect(walls, self.direction):
            newx, newy, _, _ = self.next(self.direction)
            self.rect.x = newx
            self.rect.y = newy

    def connect(self, walls, direction):
        newx, newy, oldx, oldy = self.next(direction)
        self.rect.x = newx
        self.rect.y = newy
        collide_walls = pygame.sprite.spritecollide(self, walls, False)
        self.rect.x = oldx
        self.rect.y = oldy
        return not bool(collide_walls)


class Floor(GameSprite):
    def __init__(self, x, y):
        super().__init__("./img/floor.png", x, y)

    def update(self, pressed_keys=None):
        super().update()


class Man(GameSprite):
    def __init__(self, x, y):
        super().__init__("./img/right.png", x, y)
        self.right = self.surf = pygame.image.load("./img/right.png").convert()
        self.left = self.surf = pygame.image.load("./img/left.png").convert()
        self.down = self.surf = pygame.image.load("./img/down.png").convert()
        self.up = self.surf = pygame.image.load("./img/up.png").convert()
        self.prev_x = x
        self.prev_y = y

    def update(self, walls=None):
        super().update(walls)

    def changeDirection(self, event_key):
        if event_key == K_UP:
            self.image = self.up
            self.direction = 'up'
        if event_key == K_LEFT:
            self.image = self.left
            self.direction = 'left'
        if event_key == K_DOWN:
            self.image = self.down
            self.direction = 'down'
        if event_key == K_RIGHT:
            self.image = self.right
            self.direction = 'right'

    def silent(self):
        self.direction = None


class Dot(GameSprite):
    def __init__(self, x, y):
        super().__init__("./img/dot.png", x, y)

    def update(self, walls=None):
        super().update()


class Wall(GameSprite):
    def __init__(self, x, y):
        super().__init__("./img/wall.png", x, y)

    def update(self, walls=None):
        super().update()


class Monster(GameSprite):
    def __init__(self, x, y):
        super().__init__("./img/monster.png", x, y)

    def update(self, man, walls=None):
        directions = ['right', 'left', 'up', 'down']
        # 增大朝着 pacman 方向的权重
        for i in range(1):
            if man.rect.left > self.rect.left:
                directions.append('right')
            elif man.rect.left < self.rect.left:
                directions.append('left')
            if man.rect.top < self.rect.top:
                directions.append('up')
            elif man.rect.top > self.rect.top:
                directions.append('down')
        self.direction = random.choice(list(filter(lambda direction: self.connect(walls, direction), directions)))
        super().update(walls)
