# -*- coding: utf-8 -*-
# @Time : 2019/5/8 11:42
# @Author : EricNiu
# @FileName: Akuma.py
# @Software: PyCharm

import pyautogui
import pygetwindow
import random
import time
import cv2
import numpy


SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
BATTLE_READY_B = cv2.imread("./source/battle_ready_1.png")
BATTLE_READY_Y = cv2.imread("./source/battle_ready_2.png")
BATTLE_FINISHED = cv2.imread("./source/battle_finished.png")


class BaQiDaShe(object):

    def __init__(self):
        self.stop_flag = 0
        self.game_window = None
        self.window_x = 0
        self.window_y = 0
        self.ready_flag = 100
        self.finish_flag = 100
        self.ready_info = "N/A"
        self.finish_info = "N/A"

    def click_mouse_ready(self):
        x = self.window_x + 875
        y = self.window_y + 557
        pyautogui.moveTo(random.randint(x, x + 140), random.randint(y, y + 50),
                         0.2 + random.random() / 5, pyautogui.easeOutQuad)
        pyautogui.click(clicks=2, interval=random.random() / 3 + 0.1)
        pyautogui.moveTo(random.randint(self.window_x, SCREEN_WIDTH), random.randint(1200, SCREEN_HEIGHT - 60),
                         0.5 + random.random()/5, pyautogui.easeOutQuad)

    def click_mouse_finish(self):
        time.sleep(0.5)
        x = self.window_x + 1038
        y = self.window_y + 141
        pyautogui.moveTo(random.randint(x, x + 57), random.randint(y, y + 68),
                         0.6 + random.random() / 10, pyautogui.easeOutQuad)
        pyautogui.click(clicks=3, interval=random.random() / 10 + 0.2)
        time.sleep(2.1 + (random.random() / 8))
        pyautogui.click(clicks=4, interval=random.random() / 20 + 0.33)
        pyautogui.moveTo(random.randint(x, x + 100), random.randint(y, y + 100),
                         0.2 + random.random() / 10, pyautogui.easeOutQuad)

    def start(self):
        self.game_window = pygetwindow.getWindowsWithTitle('阴阳师-网易游戏')[0]
        self.game_window.restore()
        self.game_window.focus()
        time.sleep(0.4)
        self.game_window.resizeTo(1175, 700)
        time.sleep(0.4)
        self.game_window.moveTo(SCREEN_WIDTH - 1200, int(SCREEN_HEIGHT/2 - 350))
        self.window_x, self.window_y = self.game_window.topleft

    def capture(self):
        pyautogui.screenshot("background.png", region=(self.window_x, self.window_y, 1175, 700))

    def capture_template(self):
        pyautogui.screenshot("battle_ready_1_tmp.png", region=(self.window_x + 878, self.window_y + 560, 148, 43))
        pyautogui.screenshot("battle_ready_2_tmp.png", region=(self.window_x + 826, self.window_y + 472, 89, 34))
        pyautogui.screenshot("battle_finished_tmp.png", region=(self.window_x + 67, self.window_y + 83, 23, 29))

    def judge(self):
        src_img = cv2.imread("background.png")
        self.ready_flag = numpy.mean(src_img[560:603, 878:1026, :] - BATTLE_READY_B)
        self.finish_flag = numpy.mean(src_img[83:112, 67:90, :] - BATTLE_FINISHED)
        self.ready_info = "准备:{}".format(self.ready_flag)
        self.finish_info = "结束:{}".format(self.finish_flag)

    def handle(self):
        if self.ready_flag < 50:
            self.click_mouse_ready()
        if self.finish_flag < 50:
            self.click_mouse_finish()


class YeYuanHuo(BaQiDaShe):

    def click_mouse_ready(self):
        x = self.window_x + 815
        y = self.window_y + 465
        pyautogui.moveTo(random.randint(x, x + 100), random.randint(y, y + 45),
                         0.5 + random.random() / 2, pyautogui.easeOutQuad)
        pyautogui.click(clicks=3, interval=random.random() / 3 + 0.1)
        pyautogui.moveTo(random.randint(self.window_x, SCREEN_WIDTH), random.randint(1200, SCREEN_HEIGHT - 60),
                         2 + random.random(), pyautogui.easeOutQuad)

    def click_mouse_finish(self):
        time.sleep(0.5)
        x = self.window_x + 1022
        y = self.window_y + 128
        pyautogui.moveTo(random.randint(x, x + 112), random.randint(y, y + 315),
                         0.6 + random.random() / 10, pyautogui.easeOutQuad)
        pyautogui.click(clicks=3, interval=random.random() / 10 + 0.2)
        time.sleep(2.1 + (random.random() / 8))
        pyautogui.click(clicks=4, interval=random.random() / 20 + 0.33)
        pyautogui.moveTo(random.randint(x, x + 112), random.randint(y, y + 315),
                         0.2 + random.random() / 10, pyautogui.easeOutQuad)

    def judge(self):
        src_img = cv2.imread("background.png")
        self.ready_flag = numpy.mean(src_img[472:506, 826:915, :] - BATTLE_READY_Y)
        self.finish_flag = numpy.mean(src_img[83:112, 67:90, :] - BATTLE_FINISHED)
        self.ready_info = "准备:{}".format(self.ready_flag)
        self.finish_info = "结束:{}".format(self.finish_flag)


class ToPo(BaQiDaShe):

    # TODO： 结界突破：双蛇到位了再实现吧。

    pass


if __name__ == "__main__":
    print("あれは誰だ 誰だ 誰だ")
    print("あれはデビル デビルマン デビルマン")
