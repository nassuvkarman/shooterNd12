from typing import Any
import pygame
from random import randint

HEIGHT = 700
WIDTH = 1200
SIZE = (WIDTH, HEIGHT)
FPS = 60
lost = 0
score = 0
monsters_num = 0
window = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
background = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"),
    SIZE)
pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()
pygame.font.init()
fire_sfx = pygame.mixer.Sound("fire.ogg")
font_big = pygame.font.Font(None, 70)
font_medium = pygame.font.Font(None, 35)
font_small = pygame.font.Font(None, 15)
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, coords: tuple[int,int], speed:int, size:tuple[int,int]):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image),
            size
        )
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.speed = speed
    def reset(self):
         window.blit(self.image, self.rect.topleft)
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.rect.x < WIDTH:
                self.rect.x += self.speed
            else:
                self.rect.x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
            else:
                self.rect.x = WIDTH
    def fire(self):
            new_bullet = Bullet("bullet.png",(self.rect.centerx, self.rect.top), 
                                5, 
                                (5,10))
            bullets.add(new_bullet)
            fire_sfx.play()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom >= HEIGHT:
            self.rect.y = 0
            global lost
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.bottom <= 0:
            self.kill()

player = Player("rocket.png", (WIDTH/2, HEIGHT-50), 5, (75,100))
test_enemy = Enemy("ufo.png", (randint(50, WIDTH-50), 0), 5, (75,50))
monsters = pygame.sprite.Group()

for i in range(monsters_num):
    new_enemy = Enemy("ufo.png", (randint(50,WIDTH-50),0), randint(2,8), (75,50))
    monsters.add(new_enemy)
bullets = pygame.sprite.Group()
game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()
    if not finish:
        window.blit(background, (0,0))
        player.update()
        player.reset()
        test_enemy.update()
        test_enemy.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        text_lost = font_medium.render("Пропущено: " + str(lost),
                                       True,
                                       (255,255,255)
                                       )
        text_score = font_medium.render("Рахунок: " + str(score),
                                       True,
                                       (255,255,255)
                                       )
        window.blit(text_score, (0,0))
        window.blit(text_lost, (0, 40))


    pygame.display.update()
    clock.tick(FPS)
