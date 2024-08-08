from random import randint, uniform
import pygame as pg
from settings import *
from players import *

vec = pg.math.Vector2
# 火球（正面飛行物）
class Fireball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # super().__init__() 這跟上面一行是一樣的作用，下面的都刪了
        self.image = pg.image.load(os.path.join(img_folder, "fireball.png"))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.6 / 2)
        self.rect.right =  10 * WIDTH
        self.rect.top = random.randint(50, HEIGHT - GHEIGHT - 50)

    def update(self):
        # screen.blit(self.fireball, self.fireball_rect) 不需要
        if self.rect.left > -400:
            self.rect.left -= FSPEED
        else:
            self.rect.right = 5 * WIDTH + WIDTH
            self.rect.top = randint(50, HEIGHT - GHEIGHT - 50)

# 上面掉落物
class Dropdown(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "icecream.png"))
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.7 / 2)
        self.rect.right = random.randint(50, (WIDTH - 50))
        self.rect.top = -300    # 從螢幕外掉進來

    def update(self):
        # screen.blit(self.dropdown , self.dropdown_rect) 這行不需要
        if self.rect.top < HEIGHT:
            self.rect.top += DSPEED
        else:
            self.rect.right = random.randint(50, (WIDTH - 50))
            self.rect.top = -300

"""
class Dropdown(pg.sprite.Sprite):

    def __init__(self, filename, frames=1):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename, img_W=280, img_H=70)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pg.Surface.copy(self.images[0])
        self.currentImage = 0
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
        self.rect = self.image.get_rect()
        self.rect.right = randint(50, (WIDTH - 50))
        self.rect.top = -500    # 從螢幕外掉進來

    def update(self):
        if self.rect.top < HEIGHT:
            self.rect.top += DSPEED
        else:
            self.rect.right = random.randint(50, (WIDTH - 50))
            self.rect.top = -500

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pg.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pg.mask.from_surface(self.image)
"""
# 波狀飛行物
"""
class Strangebomb(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "apple.png"))
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.right = WIDTH + 100
        self.rect.top = random.randint(150, HEIGHT - 150)

    def update(self):
        # screen.blit(self.strangebomb , self.strangebomb_rect) 這行不需要
        theta = pg.time.get_ticks()/170
        self.speed_x = BSPEED
        self.speed_y = WAVE * AMPLITUDE * math.sin(theta)
        if self.rect.left >= -30:
            self.rect.left -= self.speed_x
        else:
            self.rect.left = WIDTH + 100
            self.rect.top = random.randint(150, HEIGHT - 150)

        self.rect.top -= self.speed_y
"""
class Strangebomb(pg.sprite.Sprite):

    def __init__(self, filename, frames=1):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename, img_W=560, img_H=70)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pg.Surface.copy(self.images[0])
        self.currentImage = 0
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.7 / 2)
        self.rect.right = WIDTH + 100
        self.rect.top = randint(150, HEIGHT - 150)

    def update(self):
        # screen.blit(self.strangebomb , self.strangebomb_rect) 這行不需要
        theta = pg.time.get_ticks()/170
        self.speed_x = BSPEED
        self.speed_y = AMPLITUDE * math.sin(theta)
        if self.rect.left >= -30:
            self.rect.left -= self.speed_x
        else:
            self.rect.left = WIDTH + 100
            self.rect.top = randint(150, HEIGHT - 150)

        self.rect.top -= self.speed_y

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pg.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pg.mask.from_surface(self.image)

#地板怪物
class GEnemy(pg.sprite.Sprite):

    def __init__(self, filename, frames=1):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename, img_W=560, img_H=70)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pg.Surface.copy(self.images[0])
        self.currentImage = 0
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.7 / 2)
        self.rect.right = WIDTH + 500
        self.rect.top = 519

    def update(self):
        self.speed = PSPEED
        if self.rect.right >= - 700:
            self.rect.right -= self.speed
        else:
            self.rect.right = WIDTH + 80

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pg.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pg.mask.from_surface(self.image)


class Chase(pg.sprite.Sprite):
    def __init__(self, game, filename, frames=1):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename, img_W=280, img_H=70)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pg.Surface.copy(self.images[0])
        self.currentImage = 0
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
        self.rect = self.image.get_rect()
        # for test
        self.radius = int(self.rect.width * 0.6 / 2)
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.pos = vec( 5 * WIDTH,  3 * HEIGHT)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.game = game

    def seek_with_approach(self, target):
        # 讓他越靠近目標時，會稍微減速
        self.desired = (target - self.game.chaser.pos)
        dist = self.desired.length()
        ### 正常化初始速度（太慢了暫時取消
        # desired.normalize_ip()

        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED

        steer = (self.desired - self.game.chaser.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)

        return steer

    def update(self):
        # 取得兩位玩家的位置
        p1pos = self.game.chasetar_pos1
        p2pos = self.game.chasetar_pos2
        # 總之先決定要追一位
        chase_pos = p1pos
        if not self.game.chase4p1:
            chase_pos = p2pos
        self.game.chaser.acc = self.seek_with_approach(chase_pos)
        # 運動方式
        self.game.chaser.vel += self.game.chaser.acc
        if self.game.chaser.vel.length() > MAX_SPEED:
            self.game.chaser.vel.scale_to_length(MAX_SPEED)
            self.game.chaser.pos += self.game.chaser.vel

        self.game.chaser.rect.center = self.game.chaser.pos
    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pg.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pg.mask.from_surface(self.image)

class Strangebomb2(pg.sprite.Sprite):

    def __init__(self, filename, frames=1):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename, img_W=420, img_H=70)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pg.Surface.copy(self.images[0])
        self.currentImage = 0
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.7 / 2)
        self.rect.right = WIDTH + 100
        self.rect.top = randint(150, HEIGHT - 150)

    def update(self):
        # screen.blit(self.strangebomb , self.strangebomb_rect) 這行不需要
        theta = pg.time.get_ticks()/170
        self.speed_x = BSPEED
        self.speed_y = AMPLITUDE * math.sin(theta)
        if self.rect.left <= 1300:
            self.rect.left += self.speed_x
        else:
            self.rect.left =  -500
            self.rect.top = randint(150, HEIGHT - 150)

        self.rect.top -= self.speed_y

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pg.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pg.mask.from_surface(self.image)