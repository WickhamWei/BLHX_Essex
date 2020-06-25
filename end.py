# 1701 魏淳华 171110028
import pygame
import random
import math  # 引入数学模块
import time

version = "1.0.0"

# 界面
pygame.init()
# 载入程序图标
icon = pygame.image.load('image/icon.jpg')
pygame.display.set_icon(icon)
# 导入程序背景
bg_image = pygame.image.load('image/bg.png')
# 载入程序名字
title = '特别演习·埃塞克斯级 v'+version+" By 魏阿华 请勿用于商业用途 图片和音乐版权属于碧蓝航线"
pygame.display.set_caption(title)
# 初始化程序窗口
screen = pygame.display.set_mode((1200, 600))
# 载入背景音乐
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)  # 单曲循环

# 玩家


class Player():
    def __init__(self):
        # 玩家的图标
        self.img = pygame.image.load('image/qy.png')
        # 起始位置
        self.x = 200
        self.y = int((600-100)/2)
        # 起始血量
        self.health = 3
        # 局部变量 用于长按wasd时的持续移动
        self.__y_w = 0
        self.__y_s = 0
        self.__x_a = 0
        self.__x_d = 0
    # 开始移动

    def move_w(self):
        self.__y_w = -0.6

    def move_s(self):
        self.__y_s = 0.6

    def move_a(self):
        self.__x_a = -0.6

    def move_d(self):
        self.__x_d = 0.6
    # 停止移动

    def stop_move_w(self):
        self.__y_w = 0

    def stop_move_s(self):
        self.__y_s = 0

    def stop_move_a(self):
        self.__x_a = 0

    def stop_move_d(self):
        self.__x_d = 0
    # 刷新位置

    def fresh_location(self):
        self.x = self.x+self.__x_a+self.__x_d
        # 设置x的边界
        if self.x >= 600-100:
            self.x = 600-100
        elif self.x <= 0:
            self.x = 0
        self.y = self.y+self.__y_s+self.__y_w
        # 设置的边界
        if self.y >= 600-100:
            self.y = 600-100
        elif self.y <= 33:
            self.y = 33
        # 提交图像
        screen.blit(self.img, (self.x, self.y))

    # 遭到攻击 hurt为伤害数量
    def hit(self, hurt):
        self.health -= hurt
        # 防止生命值为负的
        if self.health <= 0:
            self.health = 0

# 玩家的子弹


class PlayerBullet():
    def __init__(self):
        global player
        self.img = pygame.image.load('image/zd.png')
        # 子弹的初始位置
        self.x = player.x + 100
        self.y = player.y+(100-50)/2
        self.speed = 1  # 子弹移动的速度

    def fresh_location(self):
        global asks
        global player_bullets
        global dyfcs
        # 子弹飘出屏幕
        if self.x > 1200:
            player_bullets.remove(self)
            return
        # 子弹打中埃塞克斯
        if self.distance(self.x+25, self.y+25, asks.x+75, asks.y+75) <= 80:
            player_bullets.remove(self)
            asks.hit(1)
            return
        # 子弹打中地狱俯冲轰炸机（明明是战斗机）
        for dyfc in dyfcs:
            if self.distance(self.x+25, self.y+25, dyfc.x+25, dyfc.y+25) <= 40:
                player_bullets.remove(self)
                dyfc.hit(1)
                return
        self.x += self.speed
        screen.blit(self.img, (self.x, self.y))

    # 用于计算子弹和对象的直线距离
    def distance(self, bx, by, ex, ey):
        a = bx - ex
        b = by - ey
        return math.sqrt(a*a + b*b)

# 地狱俯冲轰炸机的子弹


class DyfcBullet():
    def __init__(self, x, y):
        self.img = pygame.image.load('image/zd2.png')
        self.x = x - 50
        self.y = y
        self.speed = 1  # 子弹移动的速度

    def fresh_location(self):
        global player
        global dyfc_bullets
        global asks
        if self.x < 0:
            dyfc_bullets.remove(self)
            return
        if player.health > 0 and asks.health > 0:
            if self.distance(self.x+25, self.y+25, player.x+50, player.y+50) <= 50:
                dyfc_bullets.remove(self)
                player.hit(1)
                return
        self.x -= self.speed
        screen.blit(self.img, (self.x, self.y))

    def distance(self, bx, by, ex, ey):
        a = bx - ex
        b = by - ey
        return math.sqrt(a*a + b*b)

# 老婆


class Asks_small():
    def __init__(self):
        self.img = pygame.image.load('image/asks.png')
        self.x = 1000
        self.y = random.randint(33+1, 600-150-1)
        # 埃塞克斯的速度乘数
        self.speed_multiplier = 1
        # 埃塞克斯的初始生命值
        self.health = 10

    def fresh_location(self):
        self.y = self.y+0.4*self.speed_multiplier
        if self.y >= 600-150 or self.y <= 33:
            self.speed_multiplier = -self.speed_multiplier
        screen.blit(self.img, (self.x, self.y))

    def hit(self, hurt):
        self.health -= hurt
        if self.health <= 0:
            self.health = 0

# 地狱俯冲轰炸机


class Dyfc():
    def __init__(self):
        global asks
        self.img = pygame.image.load('image/dyfc.png')
        self.x = asks.x-50
        self.y = asks.y+(150-50)/2
        self.__direction_r = random.randint(0, 100)
        self.direction = 1
        if self.__direction_r >= 50:
            self.direction = -self.direction
        self.speed_multiplier_x = 1
        self.speed_multiplier_y = 2*self.direction
        self.health = 1

    def fresh_location(self):
        global asks

        self.y = self.y+0.4*self.speed_multiplier_y
        if self.y >= 600-50 or self.y <= 33:
            self.speed_multiplier_y = -self.speed_multiplier_y

        self.x = self.x+0.4*self.speed_multiplier_x
        if self.x > asks.x-50 or self.x <= 600:
            self.speed_multiplier_x = -self.speed_multiplier_x

        screen.blit(self.img, (self.x, self.y))

    def hit(self, hurt):
        global asks
        global dyfcs
        self.health -= hurt
        if self.health <= 0:
            self.health = 0
            dyfcs.remove(self)


# 事件监听器


def event_listener():
    global running
    global dyfcs
    global asks
    global player_bullets_ticks
    global player
    global dyfc_bullets
    for event in pygame.event.get():
        # 关闭游戏
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            # 控制老婆
            if event.key == pygame.K_d:
                player.move_d()
            elif event.key == pygame.K_a:
                player.move_a()
            elif event.key == pygame.K_w:
                player.move_w()
            elif event.key == pygame.K_s:
                player.move_s()
            # 发射子弹
            elif event.key == pygame.K_SPACE:
                if time.time()-player_bullets_ticks >= 1:
                    player_bullets_ticks = time.time()
                    player_bullets.append(PlayerBullet())
            # 重来
            elif event.key == pygame.K_TAB:
                if player.health == 0 or asks.health == 0:
                    player.health = 3
                    dyfcs.clear()
                    dyfc_bullets.clear()
                    asks.health = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.stop_move_d()
            elif event.key == pygame.K_a:
                player.stop_move_a()
            elif event.key == pygame.K_w:
                player.stop_move_w()
            elif event.key == pygame.K_s:
                player.stop_move_s()


def screen_loader():
    global dyfc_bullets_ticks
    global dyfc_ticks
    show_score()
    # 检查老婆有没有挂
    if asks.health > 0:
        asks.fresh_location()
    # 补充飞机
    if time.time()-dyfc_ticks >= 2:
        dyfc_ticks = time.time()
        if len(dyfcs) < 10 and asks.health > 0:
            dyfcs.append(Dyfc())
    # 刷新飞机
    for dyfc in dyfcs:
        dyfc.fresh_location()
    # 飞机射子弹
    if time.time()-dyfc_bullets_ticks >= 1:
        for dyfc in dyfcs:
            dyfc_bullets.append(DyfcBullet(dyfc.x, dyfc.y))
        dyfc_bullets_ticks = time.time()
    # 检查自己有没有挂
    if player.health > 0:
        player.fresh_location()
    for bullet in player_bullets:
        bullet.fresh_location()
    for bullet in dyfc_bullets:
        bullet.fresh_location()
    check_is_win()
    check_is_over()
    pygame.display.update()


font = pygame.font.SysFont('simsunnsimsun', 32)  # 宋体

# nhml


def check_is_over():
    global player
    if player.health <= 0:
        font = pygame.font.SysFont('simsunnsimsun', 100)
        text = "前辈，就这？"
        score_render = font.render(text, True, (255, 0, 0))
        screen.blit(score_render, (200, 250))
        font = pygame.font.SysFont('simsunnsimsun', 50)
        text = "按TAB重试"
        score_render = font.render(text, True, (255, 0, 0))
        screen.blit(score_render, (200, 450))

# 你赢了


def check_is_win():
    global asks
    if asks.health <= 0:
        font = pygame.font.SysFont('simsunnsimsun', 70)
        text = "前辈！你真棒！"
        score_render = font.render(text, True, (0, 255, 0))
        screen.blit(score_render, (200, 250))

# 计分板


def show_score():
    global font
    text = f"埃塞克斯还有: "+str(asks.health)+"血     WASD移动、空格发射"
    score_render = font.render(text, True, (255, 0, 0))
    screen.blit(score_render, (900, 10))
    text = f"企业还有: "+str(player.health)+"血"
    score_render = font.render(text, True, (0, 255, 0))
    screen.blit(score_render, (10, 10))


# 主程序
# 我自己
player = Player()
# 埃塞克斯
asks = Asks_small()
# 我发射的子弹
player_bullets = []
# 地狱俯冲轰炸机
dyfcs = []
# 地狱俯冲轰炸机的子弹
dyfc_bullets = []
# 游戏是否被关闭
running = True
# 用于间隔时间放飞机
dyfc_ticks = time.time()
# 用于间隔时间发射子弹
player_bullets_ticks = time.time()
# 用于间隔时间飞机发射子弹
dyfc_bullets_ticks = time.time()
while running:
    # 背景图
    screen.blit(bg_image, (0, 0))
    event_listener()
    screen_loader()
