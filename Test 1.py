import sys
import random

import pygame
from pygame.locals import *

pygame.init()

'''IMAGE'''

player_ship = 'plyshp.png'
enemy_ship = 'enemyshp.png'
ufo_ship = 'ufoshp.png'

screen = pygame.display.set_mode((0, 0), FULLSCREEN)
s_width, s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

bacground_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([x,y])
        self.image.fill('white')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1
        self.rect.x += 1
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)

class player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        mouse = pygame.mouse.get_pos()
        self.rect.x = mouse[0]
        self.rect.y = mouse[1]
    
class Enemy(player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-2000, 0)

class Ufo(Enemy):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = -200
        self.rect.y = 200
        self.move = 1

    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 200:
            self.move *= -1
        elif self.rect.x < -200:
            self.move *= -1


class Game:
    def __init__(self):
        self.run_game()

    def create_background(self):
        for i in range(30):
            x = random.randint(1,8)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            bacground_group.add(background_image)
            sprite_group.add(background_image)

    def create_player(self):
        self.player = player(player_ship)
        player_group.add(self.player)
        sprite_group.add(self.player)

    def create_enemy(self):
        for i in range(10):
            self.enemy = Enemy(enemy_ship)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)

    def create_ufo(self):
        for i in range(5):
            self.ufo = Ufo(ufo_ship)
            ufo_group.add(self.ufo)
            sprite_group.add(self.ufo)

    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        self.create_background()
        self.create_player()
        self.create_enemy()
        self.create_ufo()
        while True:
            screen.fill((0, 0, 0))
            self.run_update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()


            pygame.display.update()
            clock.tick(FPS)


def main():
    game = Game()


if __name__ == "__main__":
    main()