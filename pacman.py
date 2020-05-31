import time

import pygame
import random

from icecream import ic
from pygame.locals import *

from utils.generate_maze import *
from pacman_sprites import *


class Pacman(object):
    def __init__(self, xTiles, yTiles):
        print(f"{'-' * 10}游戏初始化{'-' * 10}")
        self.xTiles = xTiles
        self.yTiles = yTiles

        # Setup for sounds
        pygame.mixer.init()
        self.dead_sound = pygame.mixer.Sound('./music/pacman-is-dead.ogg')

        pygame.init()
        pygame.display.set_caption('Pacman')
        # Setup the clock for a decent framerate
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((32 * xTiles, 32 * yTiles))

        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.totalScore = None

        self.__create_sprites()

    def __create_sprites(self):
        man, dots, walls, monsters = generate_maze(self.xTiles, self.yTiles, MONSTER_NUM)
        self.totalScore = len(dots)
        self.man = Man(man[0], man[1])
        # todo: 2 men
        self.man_group = pygame.sprite.Group()
        self.man_group.add(self.man)
        self.dot_group = pygame.sprite.Group()
        self.monster_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.floor_group = pygame.sprite.Group()  # bg
        for dot in dots:
            self.dot_group.add(Dot(dot[0], dot[1]))
        for wall in walls:
            self.wall_group.add(Wall(wall[0], wall[1]))
        for x in range(xTiles):
            for y in range(yTiles):
                self.floor_group.add(Floor(x, y))
        for monster in monsters:
            self.monster_group.add(Monster(monster[0], monster[1]))

    def start_game(self):
        print(f"{'-' * 10}游戏开始{'-' * 10}")
        # 背景音乐
        pygame.mixer.music.load("./music/Purple Passion-Diana Boncheva.ogg")
        # pygame.mixer.music.load("./music/bg.ogg")
        pygame.mixer.music.play(loops=-1)
        while True:
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            self.__display_score()
            pygame.display.update()
            if len(self.dot_group) == 0:
                self.__game_over()
            # FRAME_PER_SEC 越小，pacman 走的越慢
            self.clock.tick(FRAME_PER_SEC)

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in [K_ESCAPE, K_q]:
                    self.__game_over()
                if event.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                    self.man.changeDirection(event.key)
            elif event.type == KEYUP:
                if event.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                    self.man.silent()
            elif event.type == QUIT:
                self.__game_over()

    def __update_sprites(self):
        self.floor_group.draw(self.screen)
        self.wall_group.update()
        self.wall_group.draw(self.screen)
        self.dot_group.update()
        self.dot_group.draw(self.screen)
        self.man_group.update(self.wall_group)
        self.man_group.draw(self.screen)
        self.monster_group.update(self.man, walls=self.wall_group)
        self.monster_group.draw(self.screen)

    def __display_score(self):
        score = self.totalScore - len(self.dot_group)
        text = self.font.render(f"Score: {score}/ {self.totalScore}", True, green)
        self.screen.blit(text, [10, 5])

    def __check_collide(self):
        pygame.sprite.groupcollide(self.man_group, self.dot_group, False, True)
        if pygame.sprite.groupcollide(self.man_group, self.monster_group, False, False):
            self.dead_sound.play()
            time.sleep(2)
            self.__game_over()

    def __game_over(self):
        print(f"{'-' * 10}游戏结束{'-' * 10}")
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
        exit()


if __name__ == '__main__':
    pacman = Pacman(xTiles=xTiles, yTiles=yTiles)
    pacman.start_game()
