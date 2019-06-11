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


class Team(object):

    def __init__(self):
        self.game_window = None
        # 窗口位置
        self.window_pos_x = 0
        self.window_pos_y = 0
        # 窗口大小，除去边框部分，纯游戏窗口。
        self.window_width = 0
        self.window_height = 0
        # 模板与取样的差值
        self.ready_flag = 100
        self.finish_flag = 100
        # 组队开始按钮位置
        self.ready_pos_x = 0
        self.ready_pos_y = 0
        # 组队开始按钮大小
        self.ready_rect_x = 0
        self.ready_rect_y = 0
        # 单人开始按钮位置
        self.ready_single_pos_x = 0
        self.ready_single_pos_y = 0
        # 单人开始按钮大小
        self.ready_single_rect_x = 0
        self.ready_single_rect_y = 0
        # 判断完成副本的模板位置
        self.finish_template_pos_x = 0
        self.finish_template_pos_y = 0
        # 判断完成副本的模板大小
        self.finish_template_rect_x = 0
        self.finish_template_rect_y = 0
        # 完成副本后的点击位置
        self.finish_click_pos_x = 0
        self.finish_click_pos_y = 0
        # 完成副本后的点击范围
        self.finish_click_rect_x = 0
        self.finish_click_rect_y = 0
        # 窗口相较于 原始窗口的缩放比例
        self.resize_ratio = 1
        # 传递给前端的一些信息
        self.ready_info = "N/A"
        self.finish_info = "N/A"

    def get_game_info(self):
        """
        获取游戏窗口信息，包括窗口位置，窗口大小，窗口相对于标准窗口（1420，800）的缩放比例，以及该比例下各个特征的位置和大小
        以下的坐标位置是在 Photoshop 中逐像素确认的 应该问题不大
        :return:
        """
        # 去除窗口的边框和状态栏 回归纯甄游戏。。。
        self.window_pos_x = self.game_window.topleft[0] + 10
        self.window_pos_y = self.game_window.topleft[1] + 39
        self.window_width = self.game_window.size[0] - 20
        self.window_height = self.game_window.size[1] - 49

        self.resize_ratio = self.window_width / 1420

        self.ready_pos_x = self.window_pos_x + int(1065 * self.resize_ratio)
        self.ready_pos_y = self.window_pos_y + int(639 * self.resize_ratio)

        self.ready_rect_x = int(186 * self.resize_ratio)
        self.ready_rect_y = int(56 * self.resize_ratio)

        self.ready_single_pos_x = self.window_pos_x + int(990 * self.resize_ratio)
        self.ready_single_pos_y = self.window_pos_y + int(523 * self.resize_ratio)

        self.ready_single_rect_x = int(136 * self.resize_ratio)
        self.ready_single_rect_y = int(57 * self.resize_ratio)

        self.finish_template_pos_x = self.window_pos_x + int(67 * self.resize_ratio)
        self.finish_template_pos_y = self.window_pos_y + int(52 * self.resize_ratio)

        self.finish_template_rect_x = int(40 * self.resize_ratio)
        self.finish_template_rect_y = int(36 * self.resize_ratio)

        self.finish_click_pos_x = self.window_pos_x + int(1270 * self.resize_ratio)
        self.finish_click_pos_y = self.window_pos_y + int(125 * self.resize_ratio)

        self.finish_click_rect_x = int(110 * self.resize_ratio)
        self.finish_click_rect_y = int(90 * self.resize_ratio)

    def click_mouse_ready(self):
        """
        组队模式下 移动到开始按钮并点击
        :return:
        """
        self.get_game_info()
        pyautogui.moveTo(random.randint(self.ready_pos_x, self.ready_pos_x + self.ready_rect_x),
                         random.randint(self.ready_pos_y, self.ready_pos_y + self.ready_rect_y),
                         0.2 + random.random() / 5, pyautogui.easeOutQuad)
        pyautogui.click(clicks=3, interval=random.random() / 3 + 0.1)

    def click_mouse_finish(self):
        """
        组队模式下 结束战斗获取战利品 这个函数的各项interval经过长时间的实践检验切实可行（大概）。
        :return:
        """
        self.get_game_info()
        time.sleep(0.8)
        pyautogui.moveTo(random.randint(self.finish_click_pos_x, self.finish_click_pos_x + self.finish_click_rect_x),
                         random.randint(self.finish_click_pos_y, self.finish_click_pos_y + self.finish_click_rect_y),
                         0.6 + random.random() / 10, pyautogui.easeOutQuad)
        pyautogui.click(clicks=3, interval=random.random() / 10 + 0.2)
        time.sleep(2.1 + (random.random() / 8))
        pyautogui.click(clicks=4, interval=random.random() / 20 + 0.33)
        pyautogui.moveTo(random.randint(self.finish_click_pos_x, self.finish_click_pos_x + 50),
                         random.randint(self.finish_click_pos_y, self.finish_click_pos_y + 50),
                         0.2 + random.random() / 10, pyautogui.easeOutQuad)

    def start(self):
        """
        脚本开始后的一些基本操作
        :return:
        """
        self.game_window = pygetwindow.getWindowsWithTitle('阴阳师-网易游戏')[0]  # 这里返回一个数列，所以多开是可以实现的

        self.game_window.restore()
        self.game_window.focus()  # 置于顶层

        time.sleep(0.4)
        self.get_game_info()
        # 默认移动到右侧中央 不需要的话请注释掉
        self.game_window.moveTo(SCREEN_WIDTH - self.window_width - 20, int(SCREEN_HEIGHT/2 - self.window_height/2))

    def capture(self):
        """
        截取样本的函数 截取 开始战斗 和 结束战斗后的数据分析 两个位置
        :return:
        """
        self.get_game_info()
        # 截取游戏
        # pyautogui.screenshot("background.png", region=(self.window_pos_x, self.window_pos_y,
        #                                                self.window_width, self.window_height))
        pyautogui.screenshot("sample_1.png", region=(self.ready_pos_x, self.ready_pos_y,
                                                     self.ready_rect_x, self.ready_rect_y))
        pyautogui.screenshot("sample_2.png", region=(self.finish_template_pos_x, self.finish_template_pos_y,
                                                     self.finish_template_rect_x, self.finish_template_rect_y))

    def capture_template(self):
        # 制作模板的函数 截取对应三个位置 手动移动到source文件夹
        self.get_game_info()
        pyautogui.screenshot("battle_ready_1_tmp.png", region=(self.ready_pos_x, self.ready_pos_y,
                                                               self.ready_rect_x, self.ready_rect_y))
        pyautogui.screenshot("battle_ready_2_tmp.png", region=(self.ready_single_pos_x, self.ready_single_pos_y,
                                                               self.ready_single_rect_x, self.ready_single_rect_y))
        pyautogui.screenshot("battle_finished_tmp.png", region=(self.finish_template_pos_x, self.finish_template_pos_y,
                                                                self.finish_template_rect_x, self.finish_template_rect_y))

    def judge(self):
        """
        简单的判断 直接图片相减 快到不可思议
        :return:
        """
        ready_sample = cv2.imread("sample_1.png")
        ready_template = cv2.imread("./source/battle_ready_1.png")

        finish_sample = cv2.imread("sample_2.png")
        finish_template = cv2.imread("./source/battle_finished.png")

        try:
            self.ready_flag = numpy.mean(ready_sample - ready_template)
            self.finish_flag = numpy.mean(finish_sample - finish_template)
            self.ready_info = "准备:{}".format(self.ready_flag)
            self.finish_info = "结束:{}".format(self.finish_flag)
        except ValueError:
            # 出现这个错误说明取样图片和模板图片不匹配
            self.ready_flag = 100
            self.finish_flag = 100
            self.ready_info = "模板图片大小不匹"
            self.finish_info = "配,请重新制作模板。"

    def handle(self):
        """
        简单的响应函数 开始和结束
        :return:
        """
        if self.ready_flag < 30:
            self.click_mouse_ready()
        if self.finish_flag < 30:
            self.click_mouse_finish()


class Solo(Team):

    def __init__(self):
        super().__init__()

    def get_game_info(self):
        super().get_game_info()
        # 继承父类的大部分参数 但是结束战斗后的点击位置有些许不同
        self.finish_click_rect_x = int(135 * self.resize_ratio)
        self.finish_click_rect_y = int(230 * self.resize_ratio)

    def click_mouse_ready(self):
        """
        单刷的挑战按钮位置有些许不同 所以这个函数要重写
        :return:
        """
        self.get_game_info()
        pyautogui.moveTo(random.randint(self.ready_single_pos_x, self.ready_single_pos_x + self.ready_single_rect_x),
                         random.randint(self.ready_single_pos_y, self.ready_single_pos_y + self.ready_single_rect_y),
                         0.2 + random.random() / 5, pyautogui.easeOutQuad)
        pyautogui.click(clicks=3, interval=random.random() / 3 + 0.1)

    def capture(self):
        """
        截取样本的位置发生变化 重写一下
        :return:
        """
        self.get_game_info()
        # 截取游戏
        pyautogui.screenshot("sample_1.png", region=(self.ready_single_pos_x, self.ready_single_pos_y,
                                                     self.ready_single_rect_x, self.ready_single_rect_y))
        pyautogui.screenshot("sample_2.png", region=(self.finish_template_pos_x, self.finish_template_pos_y,
                                                     self.finish_template_rect_x, self.finish_template_rect_y))

    def judge(self):
        ready_sample = cv2.imread("sample_1.png")
        ready_template = cv2.imread("./source/battle_ready_2.png")

        finish_sample = cv2.imread("sample_2.png")
        finish_template = cv2.imread("./source/battle_finished.png")

        try:
            self.ready_flag = numpy.mean(ready_sample - ready_template)
            self.finish_flag = numpy.mean(finish_sample - finish_template)
            self.ready_info = "准备:{}".format(self.ready_flag)
            self.finish_info = "结束:{}".format(self.finish_flag)
        except ValueError:
            self.ready_flag = 100
            self.finish_flag = 100
            self.ready_info = "模板图片大小不匹"
            self.finish_info = "配,请重新制作模板。"


class ToPo(Team):

    # TODO： 结界突破：///蛇到位了再实现吧///。 等红林到位了再说吧。

    pass


if __name__ == "__main__":
    print("本文件提供了两个类")

