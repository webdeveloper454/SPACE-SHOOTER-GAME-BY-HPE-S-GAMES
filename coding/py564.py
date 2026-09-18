import pygame
import random
import math
from pathlib import Path

pygame.init()
WIDTH, HEIGHT = 500, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space shooters by HPE's GAMES")

BLACK = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 220, 255)
red = (255, 70, 70)
purple = (190, 70, 255)
clock = pygame.time.Clock()
FPS = 30
font = pygame.font.SysFont("arial", 30)

picture_dir = Path(r"C:\Users\athyr\Desktop\pictures")
enemy_images = []
player_sprite_image = None
background_image = None

enemy_file = picture_dir / "enemy ship.jpeg"
player_file = picture_dir / "spaceship (player).jpeg"
background_file = picture_dir / "space shooter background.jpeg"

def remove_white_background(surface):
    width, height = surface.get_size()
    transparent = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        for x in range(width):
            r, g, b, a = surface.get_at((x, y))
            is_near_white = (
                max(r, g, b) > 220 and
                abs(r - g) < 25 and
                abs(g - b) < 25
            )
            if is_near_white:
                transparent.set_at((x, y), (0, 0, 0, 0))
            else:
                transparent.set_at((x, y), (r, g, b, a))
    return transparent


if enemy_file.exists():
    enemy_img = pygame.image.load(str(enemy_file)).convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (44, 40))
    enemy_img = remove_white_background(enemy_img)
    enemy_images.append(enemy_img)

if player_file.exists():
    player_sprite_image = pygame.image.load(str(player_file)).convert_alpha()
    player_sprite_image = pygame.transform.scale(player_sprite_image, (64, 52))
    player_sprite_image = remove_white_background(player_sprite_image)

if background_file.exists():
    background_image = pygame.image.load(str(background_file)).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


def make_spaceship():
    if player_sprite_image is not None:
        return player_sprite_image
    image = pygame.Surface((64, 52), pygame.SRCALPHA)
    pygame.draw.polygon(image, cyan, [(32, 2), (8, 44), (24, 38), (32, 50), (40, 38), (56, 44)])
    pygame.draw.polygon(image, blue, [(32, 10), (24, 35), (40, 35)])
    pygame.draw.rect(image, white, (29, 17, 6, 12), border_radius=3)
    pygame.draw.line(image, yellow, (16, 44), (10, 51), 3)
    pygame.draw.line(image, yellow, (48, 44), (54, 51), 3)
    return image


def make_enemy(style):
    if enemy_images:
        return enemy_images[style % len(enemy_images)]
    image = pygame.Surface((44, 40), pygame.SRCALPHA)
    color = [red, purple, yellow][style % 3]
    pygame.draw.ellipse(image, color, (4, 5, 36, 27))
    pygame.draw.polygon(image, color, [(4, 18), (0, 34), (14, 27), (30, 27), (44, 34), (40, 18)])
    pygame.draw.circle(image, BLACK, (16, 17), 4)
    pygame.draw.circle(image, BLACK, (28, 17), 4)
    pygame.draw.circle(image, white, (16, 16), 1)
    pygame.draw.circle(image, white, (28, 16), 1)
    return image

class player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = make_spaceship()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH //2
        self.rect.bottom = HEIGHT - 30
        self.speed = 6

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if key[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if key[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed       

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet) 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = make_enemy(random.randrange(9))
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(3, 6)

    def update(self):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx)) + 90
        self.image = pygame.transform.rotate(self.base_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(3, 6)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 18), pygame.SRCALPHA)
        pygame.draw.rect(self.image, yellow, (1, 0, 4, 18), border_radius=2)
        pygame.draw.circle(self.image, white, (3, 3), 2)
        self.rect = self.image.get_rect()  
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class HeartSystem:
    def __init__(self, max_hearts):
        self.max_hearts = max_hearts
        self.hearts = max_hearts
        self.heart_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.heart_image, (255, 0, 0), (12, 13), 10)
        pygame.draw.circle(self.heart_image, (255, 0, 0), (28, 13), 10)
        pygame.draw.polygon(
            self.heart_image,
            (255, 0, 0),
            [(3, 16), (37, 16), (20, 38)],
        )

    def lose_heart(self):
        self.hearts -= 1
        if self.hearts < 0:
            self.hearts = 0

    def add_heart(self):
        if self.hearts < self.max_hearts:
            self.hearts += 1

    def is_dead(self):
        return self.hearts <= 0

    def draw(self, screen):
        for i in range(self.hearts):
            x = 10 + (i * 45)
            y = 40
            screen.blit(self.heart_image, (x, y))


all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = player()
all_sprites.add(player)
heart_system = HeartSystem(2)

for i in range(9):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)
score = 0
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 1
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    for enemy in pygame.sprite.spritecollide(player, enemies, False):
        heart_system.lose_heart()
        enemy.rect.x = random.randint(0, WIDTH - enemy.rect.width)
        enemy.rect.y = random.randint(-100, -40)
        if heart_system.is_dead():
            running = False

    if background_image is not None:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BLACK)
    all_sprites.draw(screen)
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 10))
    heart_system.draw(screen)
    pygame.display.flip()
pygame.quit()    