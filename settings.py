import os, math , sys
import pygame as pg
### 常數
TITLE = "The Rolling Donuts"
FPS = 100    # 每秒刷新次數
ADD_FIRE_RATE = 200
WIDTH, HEIGHT = 1250, 650   # 畫面大小
SIZE = (WIDTH, HEIGHT)
HW, HH = WIDTH / 2, HEIGHT / 2
AREA = WIDTH * HEIGHT
GHEIGHT = 66    # 地面高度
PSPEED = 1    ### 此為畫面捲動速度，敬請多加利用。

game = "run" ##遊戲結束用

### 定義一些顏色：混合RGB的比例 0-255
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OLIVE = (128, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
CHOCOLATE = (210, 105, 30)
TAN = (210, 180, 140)
GOLDENROD = (218, 165, 32)
ROSYBROWN = (188, 143, 143)
STEELBLUE = (70, 130, 180)
NAVY = (0, 0, 128)
DARKSLATEBLUE = (72, 61, 139)
INDIGO = (75, 0, 130)

### 精靈會用到的屬性
life = 0
life2 = 0
DONUT_W = 75    # 暫定
DONUT_H = 75
DONUT_ACC = 2#1.5             # 加速度，越大可以跑快一點
DONUT_FRICTION = -0.35      # 摩擦力，越小會滑行越遠，最大速度亦會變大。
GRAVITY = 0.75               # 重力
JMP = -20                   # 跳躍力（加速度／絕對值越大越強）

### 波狀飛行物用常數
BSPEED = 2      # 兩者之間的比例
AMPLITUDE = 5   # 與運動軌跡有關
### 影響振幅？

flframe = 0

### firball用常數
FSPEED = 5
fire_list = []
add_fire_rate = 0

### dropdown用常數
drframe = 0
DSPEED = 1

### genemy用常數
gframe = 0

###monster用
leftframe = 0
### Chaser用常數
MAX_SPEED = 1.8
CHASERSIZE = (50, 50)
APPROACH_RADIUS = 55
MAX_FORCE = 5

### 平台（x, y, 寬度, 厚度）
### 因為目前人物寬100，所以平台寬度至少150吧，暫定以５０為單位增加
### 或者寬度也可固定幾種
### 或者位置也可以固定
THICK = 20
PW = 150
PWADD = 50
PLATFORM_LIST = [(0, 450, PW, THICK),
                 (WIDTH / 6 + 100, 400, PW + PWADD, THICK),
                 (2 * WIDTH / 6, 100, PW, THICK),
                 (3 * WIDTH / 6 + 100, 450, PW, THICK),
                 (4 * WIDTH / 6, 100, PW + PWADD, THICK),
                 (5 * WIDTH / 6, 250, PW, THICK)]

GROUND_LIST = [(WIDTH, HEIGHT - GHEIGHT, (2 * WIDTH) - 200, GHEIGHT),
               (WIDTH, HEIGHT - GHEIGHT, (2 * WIDTH) - 200, GHEIGHT),
               (WIDTH, HEIGHT - GHEIGHT, WIDTH + (WIDTH / 2), GHEIGHT),
               (WIDTH, HEIGHT - GHEIGHT, 4 * WIDTH / 3 , GHEIGHT),
               (WIDTH, HEIGHT - GHEIGHT, 4 * WIDTH / 3, GHEIGHT),
               (WIDTH, HEIGHT - GHEIGHT, 9 * WIDTH / 5 , GHEIGHT)]
### 設定assets： 圖片與聲音的存放
### 取得這個檔案的目錄位置
game_folder = os.path.dirname(__file__)
### 將img指定在上面這個目錄下
img_folder = os.path.join(game_folder, "img")

Bstart = 0  # 螢幕初始設定
Direction = 1  # 螢幕捲動方向
frame = 0  # 主角所在動作的index
def clock():
    current_time = pg.time.get_ticks()
    return current_time
nextFrame = clock()

# 鍵盤用
keydict = {"space": pg.K_SPACE, "esc": pg.K_ESCAPE, "up": pg.K_UP, "down": pg.K_DOWN,
           "left": pg.K_LEFT, "right": pg.K_RIGHT, "return": pg.K_RETURN,
           "a": pg.K_a,
           "b": pg.K_b,
           "c": pg.K_c,
           "d": pg.K_d,
           "e": pg.K_e,
           "f": pg.K_f,
           "g": pg.K_g,
           "h": pg.K_h,
           "i": pg.K_i,
           "j": pg.K_j,
           "k": pg.K_k,
           "l": pg.K_l,
           "m": pg.K_m,
           "n": pg.K_n,
           "o": pg.K_o,
           "p": pg.K_p,
           "q": pg.K_q,
           "r": pg.K_r,
           "s": pg.K_s,
           "t": pg.K_t,
           "u": pg.K_u,
           "v": pg.K_v,
           "w": pg.K_w,
           "x": pg.K_x,
           "y": pg.K_y,
           "z": pg.K_z,
           "1": pg.K_1,
           "2": pg.K_2,
           "3": pg.K_3,
           "4": pg.K_4,
           "5": pg.K_5,
           "6": pg.K_6,
           "7": pg.K_7,
           "8": pg.K_8,
           "9": pg.K_9,
           "0": pg.K_0,
           "num0": pg.K_KP0,
           "num1": pg.K_KP1,
           "num2": pg.K_KP2,
           "num3": pg.K_KP3,
           "num4": pg.K_KP4,
           "num5": pg.K_KP5,
           "num6": pg.K_KP6,
           "num7": pg.K_KP7,
           "num8": pg.K_KP8,
           "num9": pg.K_KP9}
