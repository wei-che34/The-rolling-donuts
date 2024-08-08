import os, time, math, random, sys
import pygame as pg
from pygame.locals import *
from settings import *
from players import *
from platforms import *
from enemies import *

class Game2:
    def __init__(self):
        # 初始化遊戲
        pg.init()           # 起手式
        pg.mixer.init()     # 有用聲音的起手式
        self.screen = pg.display.set_mode(SIZE) #, pg.FULLSCREEN)  # 設定介面大小
        pg.display.set_caption(TITLE)
        self.bkgd = pg.image.load("img/bk.png").convert() #
        self.bkgd = pg.transform.scale(self.bkgd, (1550, 1150))
        # self.background = pg.Surface(SIZE)  # ??跟screen有何不同
        # self.background.fill(( 0 , 0 , 120 ))  # 塗滿(之後可調整)
        self.clock = pg.time.Clock()
        self.running = True
        self.hurt_sound = pg.mixer.Sound("bgm/hurt.wav")

    def new(self):
        # 重新開始一個遊戲
        self.FPS = 60
        self.all_sprites = pg.sprite.Group()    # 初始化全部精靈群組
        self.grounds = pg.sprite.Group()    # 初始化地面群組
        self.holes = pg.sprite.Group()    # 初始化洞群組
        self.platforms = pg.sprite.Group()    # 初始化平台群組
        self.enemies = pg.sprite.Group()   # 初始化敵人群組
        self.weapon = pg.sprite.Group()  # 初始化道具群組
        self.superdonut = pg.sprite.Group()  # 初始化donut群組
        self.p1 = pg.sprite.Group()



        ### 送自己回去Superdonut，才能夠與這裡的platform群組檢查
        self.donut = Superdonut(self, "img/don.png", 4)
        self.donutp2 = Superdonut2(self, "img/don2.png", 4)   # !!!!!!!!!!!!!!!!
        self.all_sprites.add(self.donut)
        self.superdonut.add(self.donut)
        self.p1.add(self.donut)
        self.blood = Blood("img/p1blood.png", 6, 0)
        self.all_sprites.add(self.blood)

        ### 讀入地板
        self.gnd = Ground(0, HEIGHT - GHEIGHT, WIDTH, GHEIGHT)     # 地板單獨設定
        self.all_sprites.add(self.gnd)
        self.grounds.add(self.gnd)

        # ### 讀入洞
        self.holeedges = Holeedge()
        self.all_sprites.add(self.holeedges)
        self.hole = Hole()
        self.all_sprites.add(self.hole)
        self.holes.add(self.hole)

        ### 讀入其他平台
        for plat in PLATFORM_LIST:
            p = Platform(plat[0], plat[1], plat[2], plat[3])
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.high_p1 = Highplatform1()
        self.high_p2 = Highplatform2()
        self.mid_p1 = Midplatform1()
        self.mid_p2 = Midplatform2()
        self.lo_p1 = Lowplatform1()
        self.lo_p2 = Lowplatform2()

        ### 待初始走遠後
        self.all_sprites.add(self.high_p1)
        self.platforms.add(self.high_p1)
        self.all_sprites.add(self.high_p2)
        self.platforms.add(self.high_p2)

        self.all_sprites.add(self.mid_p1)
        self.platforms.add(self.mid_p1)
        self.all_sprites.add(self.mid_p2)
        self.platforms.add(self.mid_p2)

        self.all_sprites.add(self.lo_p1)
        self.platforms.add(self.lo_p1)
        self.all_sprites.add(self.lo_p2)
        self.platforms.add(self.lo_p2)

        self.sbomb = Strangebomb("img/flyenemy.png",8)
        self.all_sprites.add(self.sbomb)
        self.enemies.add(self.sbomb)

        self.fball = Fireball()
        self.all_sprites.add(self.fball)
        self.enemies.add(self.fball)

        self.genemy = GEnemy("img/genemy.png",8)
        self.all_sprites.add(self.genemy)
        self.enemies.add(self.genemy)

        self.reverse = Reverse()
        self.all_sprites.add(self.reverse)
        self.weapon.add(self.reverse)
        
        self.monster = Strangebomb2("img/leftenemy.png",6)
        self.all_sprites.add(self.monster)
        self.enemies.add(self.monster)


        ### 執行遊戲
        self.run()

    def run(self):
        # 遊戲迴圈：
        self.playing = True
        while self.playing:      # 每回畫面更新都要做的事情
            global frame, nextFrame
            self.frame = frame
            if clock() > nextFrame:
                if frame < 3:
                    self.frame += 1
                    frame += 1
                else:
                    frame = 0
                nextFrame += 40
            self.clock.tick(self.FPS)
            self.events()
            self.update()
            self.draw()
            self.change()
            self.check_gameover()

    def bgm(self):
        bgm = pg.mixer.music.load("bgm/one.ogg")
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(1.0)  #調整音量大小(0.0-1.0)

    def update(self):
        # 更新背景
        global Bstart
        global Direction
        global life
        global life2
        global gframe
        global drframe
        global flframe
        global leftframe
        global game
        self.rel_x = Direction * Bstart % self.bkgd.get_rect().width
        self.screen.blit(self.bkgd, (self.rel_x - self.bkgd.get_rect().width, \
                                     -300)) # 捲動螢幕
        if self.rel_x < WIDTH:
            self.screen.blit(self.bkgd, (self.rel_x, -300))
        Bstart -= PSPEED

        # 更新群組內每一個每個精靈的動作
        self.all_sprites.update()
        # 檢查「落下」碰撞（放入一個list）
        oops = pg.sprite.spritecollide(self.donut, self.holes, False)
        if not oops:
            if self.donut.vel.y > 0:    # 檢查落下（y>0）時的碰撞
                hits = pg.sprite.spritecollide(self.donut, self.platforms, \
                       False)
                hitsground = pg.sprite.spritecollide(self.donut, self.grounds, \
                             False)
                if hits:
                ### 撞到的話就讓他的位置維持在那個平台上，速度歸零。
                    self.donut.pos.y = hits[0].rect.top + 1
                    self.donut.vel.y = 0
                elif hitsground:
                ### 撞到的話就讓他的位置維持在地板上，速度歸零。
                    self.donut.pos.y = hitsground[0].rect.top + 1
                    self.donut.vel.y = 0
            if self.donut.vel.y < 0:    # 檢查向上碰撞
                hits = pg.sprite.spritecollide(self.donut, self.platforms, \
                       False)
                if hits:
                ### 撞到的話就瞬間降低一個主角的高度，並且速度歸零。
                    self.donut.pos.y = hits[0].rect.bottom + DONUT_W
                    self.donut.vel.y = 0

        ###判斷是否吃到倒轉武器
        getweapon = pg.sprite.spritecollide(self.reverse, self.superdonut, \
                    False)
        if getweapon:
            self.reverse.rect.right = 4000 #重置倒轉武器位置
            #Direction *= -1  # 背景倒轉
            self.FPS += 60

        ###donut撞enemies

        crash = pg.sprite.spritecollide(self.donut, self.enemies, \
                False, pg.sprite.collide_circle)
        sbcrash = pg.sprite.spritecollide(self.sbomb, self.superdonut, \
                  False, pg.sprite.collide_circle)
        fbcrash = pg.sprite.spritecollide(self.fball, self.superdonut, \
                  False, pg.sprite.collide_circle)
        grcrash = pg.sprite.spritecollide(self.genemy, self.superdonut, \
                  False, pg.sprite.collide_circle)
        mocrash = pg.sprite.spritecollide(self.monster, self.superdonut,
                  False, pg.sprite.collide_circle)
        if crash and sbcrash:
            self.sbomb.rect.right = 2000
            life += 1
            if life >= 5:
                game = "gameover"
            changeSpriteImage(self.blood, life)
            self.hurt_sound.play()
        if crash and fbcrash:
            self.fball.rect.right = 2000
            life += 1
            if life >= 5:
                game = "gameover"
            changeSpriteImage(self.blood, life)
            self.hurt_sound.play()
        if crash and grcrash:
            self.genemy.rect.right = 3000
            life += 1
            if life >= 5:
                game = "gameover"
            changeSpriteImage(self.blood, life)
            self.hurt_sound.play()
        if crash and mocrash:
            self.monster.rect.right = -500
            life += 1
            if life >= 5:
                game = "gameover"
            changeSpriteImage(self.blood, life)
            self.hurt_sound.play()

        if gframe < 7:
            gframe += 0.05
            changeSpriteImage(self.genemy, int(gframe))
        else:
            gframe = 0
            changeSpriteImage(self.genemy, int(gframe))
        if flframe < 7:
            flframe += 0.05
            changeSpriteImage(self.sbomb, int(flframe))
        else:
            flframe = 0
            changeSpriteImage(self.sbomb, int(flframe))
        if leftframe < 5:
            leftframe += 0.05
            changeSpriteImage(self.monster, int(leftframe))
        else:
            leftframe = 0
            changeSpriteImage(self.monster, int(leftframe))
        

    def events(self):
        for event in pg.event.get():
            # 遊戲結束
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and \
                                         event.key == pg.K_ESCAPE):
                if self.playing:    # 不玩了
                    self.playing = False
                self.running = False    # 不執行了

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.donut.jump()
                if event.key == pg.K_w:
                    self.donutp2.jump()


    def change(self):
        if keyPressed("right"):
            changeSpriteImage(self.donut, frame)
        elif keyPressed("left"):
            changeSpriteImage(self.donut, frame)
        else:
            changeSpriteImage(self.donut, 0)
        pg.display.update()

    def draw(self):
        self.all_sprites.draw(self.screen)
        ### 每次畫好畫滿所有的東西之後，就要flip。
        pg.display.flip()   # 把畫好的東西翻到正面的

    def check_gameover(self):
        global game
        global life
        if self.donut.pos.y > HEIGHT:
            self.show_go_screen()
            self.playing = False
        if game == "gameover":
            game = "run"
            self.show_go_screen()
            self.playing = False
    def rule_explain(self):
        # 開始畫面
        self.screen.fill(BLACK)
        self.start_img = pg.image.load('img/rule_new.png')
        self.start_img = pg.transform.scale(self.start_img, (1250, 650))
        self.start_img_rect = self.start_img.get_rect()
        self.start_img_rect.center = (WIDTH/2, HEIGHT/2)
        self.screen.blit(self.start_img, self.start_img_rect)

        go = True
        while go:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()      # 結束在這裏
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()      # 還有這裏
                    else:
                        go = False      # 停止迴圈
            pg.display.update()
    def choose_game(self):
        # 開始畫面
        def player1(self):
            self.screen.fill(BLACK)
            self.start_img = pg.image.load('img/startp1.png')
            self.start_img = pg.transform.scale(self.start_img, (1250, 650))
            self.start_img_rect = self.start_img.get_rect()
            self.start_img_rect.center = (WIDTH/2, HEIGHT/2)
            self.screen.blit(self.start_img, self.start_img_rect)
        def player2(self):
            self.screen.fill(BLACK)
            self.start_img = pg.image.load('img/startp2.png')
            self.start_img = pg.transform.scale(self.start_img, (1250, 650))
            self.start_img_rect = self.start_img.get_rect()
            self.start_img_rect.center = (WIDTH/2, HEIGHT/2)
            self.screen.blit(self.start_img, self.start_img_rect)
        startimg = player1(self)
        go = True
        while go:
            startimg
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()      # 結束在這裏
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()      # 還有這裏
                    elif event.key == pg.K_DOWN:
                        startimg = player2(self)
                        g = Game()
                    elif event.key == pg.K_UP:
                        startimg = player1(self)
                        g = Game2()
                    else:
                        go = False      # 停止迴圈
    def show_go_screen(self):
        # 遊戲結束／再來一場？的畫面
        global life
        life = 0
        self.screen.fill(BLACK)
        self.start_img = pg.image.load('img/LOSE.png')
        self.start_img = pg.transform.scale(self.start_img, (1250, 650))
        self.start_img_rect = self.start_img.get_rect()
        self.start_img_rect.center = (WIDTH/2, HEIGHT/2)
        self.screen.blit(self.start_img, self.start_img_rect)

        go = True
        while go:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()      # 結束在這裏
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()      # 還有這裏
                    else:
                        go = False      # 停止迴圈
            pg.display.update()
