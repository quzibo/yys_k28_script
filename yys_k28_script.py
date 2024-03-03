# 对屏幕截图整合为函数的形式  try_3       桌面版的大小不能改变   位置可以改变  也不要遮挡
# 读取模板图像整合为函数的形式  try_4
# 只获取匹配到的第一个位置
# 加入循环执行的逻辑   try_5
#  首先判断是不是在explore界面（其实应该先判断协助邀请界面）  其实在每个界面都要判断有没有协助邀请界面
#  判断有没有fight界面
       # 如果有fight界面，循环判断是否有胜利界面 如果有胜利界面  连续点击屏幕   如果失败也连续点击屏幕
#  如果掉落宝箱点击宝箱
# 初步实现循环逻辑   try_6
# 对大部分函数进一步的封装  参数包括 template_type 间隔时间等 很多地方例如点击次数 位移  点倒数的还是正数的 很多地方不一样 仍采用try_6    try_7
# 制作控制脚本开始或者结束的界面   try_8
# 限制或统计次数
# treasure_box 和 receive_award 互换位置 try_9

import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
import tkinter as tk
from threading import Thread

# 一个方法
# 函数获取当前屏幕的截屏并返回BGR格式的numpy数据
def get_screenshot():
    # 截屏
    screenshot = ImageGrab.grab()
    # 将 PIL 图像转换为 NumPy 数组
    screenshot_np = np.array(screenshot)
    # 将 NumPy 数组转换为 OpenCV 格式的图像
    screenshot_cv2 = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    return screenshot_cv2


# 一个方法
# 函数读取模板图片，并返回BGR格式的numpy图片数据 以及目标那图片的宽和高
# 参数模板的类型： 探索，战斗，宝箱等
def get_template(template_type):
    if template_type == 'test':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/out_warehouse.png', -1)
    if template_type == 'explore':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/explore.png', -1)
    if template_type == 'fight':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/fight.png', -1)
    if template_type == 'boss_fight':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/boss_fight.png', -1)
    if template_type == 'win':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/win.png', -1)
    if template_type == 'treasure_box':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/treasure_box.png', -1)
    if template_type == 'receive_award':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/receive_award.png', -1)
    if template_type == 'catalogue':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/catalogue.png', -1)
    if template_type == '28':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/28.png', -1)
    if template_type == 'big_treasure_box':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/big_treasure_box1.png', -1)
    if template_type == 'big_treasure_end':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/big_treasure_end.png', -1)
    if template_type == 'refuse':
        # 读取模板图片   以bgr的格式
        template = cv2.imread('./image/refuse.png', -1)
    # 获取模板图像的高度和宽度
    w, h = template.shape[:-1][::-1]
    return template, w, h
fight_count = 0
boss_fight_count = 0
current_action = ''
sign1 = False
def start_task():
    # 创建并启动一个新线程执行任务
    t = Thread(target=task)
    t.start()
def task():
    # 模拟一个耗时的任务
    global sign1
    sign1 = True
    while sign1:
        global current_action
        # 判断顺序
        screenshot_cv2 = get_screenshot()

        #  拒绝悬赏封印邀请
        template, w, h = get_template('refuse')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][-1], loc[0][-1]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            # 如果有explore就左键单击   跳出本次循环   执行下一次循环
            print('refuse')
            current_action = 'refuse'
            time.sleep(0.5)
            continue

        #  先前前的大宝箱
        template, w, h = get_template('big_treasure_box')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][-1], loc[0][-1]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            # 如果有explore就左键单击   跳出本次循环   执行下一次循环
            print('big_treasure_box')
            current_action = 'big_treasure_box'
            time.sleep(0.5)
            continue


        #  先前前的大宝箱的结局
        template, w, h = get_template('big_treasure_end')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][-1], loc[0][-1]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            # 如果有explore就左键单击   跳出本次循环   执行下一次循环
            print('big_treasure_end')
            current_action = 'big_treasure_end'
            time.sleep(0.5)
            continue


        #  先前的第一顺位 28   但是会匹配到第26章
        template, w, h = get_template('28')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][-1], loc[0][-1]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            # 如果有explore就左键单击   跳出本次循环   执行下一次循环
            print('28')
            current_action = '28'
            time.sleep(0.5)
            continue


        #  第一顺位判断 explore
        template, w, h = get_template('explore')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >=1 :
            pt = tuple((loc[1][0], loc[0][0]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            # 如果有explore就左键单击   跳出本次循环   执行下一次循环
            print('explore')
            current_action = 'explore'
            time.sleep(0.5)
            continue
        # 如果没有 不会执行if语句  进行接下来的判断


        #  第二顺位判断 boss_fight 先打boss
        template, w, h = get_template('boss_fight')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            global boss_fight_count
            boss_fight_count += 1

            pt = tuple((loc[1][0], loc[0][0]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            print('boss_fight')
            current_action = 'boss_fight'
            time.sleep(7.0)
            continue


        #  第三顺位判断 fight
        template, w, h = get_template('fight')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >=1 :
            global fight_count
            fight_count += 1
            pt = tuple((loc[1][-1], loc[0][-1]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            print('fight')
            current_action = 'fight'
            time.sleep(7.0)# 战斗状态多歇息一会
            continue


        #  第四顺位判断 win
        template, w, h = get_template('win')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][0], loc[0][0]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            time.sleep(0.8)
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            pyautogui.click(pt[0] + w / 2, pt[1] + 2*h, button='left')
            print('win!')
            current_action = 'win!'
            time.sleep(0.5)
            continue

        #  第六顺位判断 receive
        template, w, h = get_template('receive_award')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][0], loc[0][0]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2 + 400, button='left')  # +400表示其他位置   可以用ctrl a微信截图测量
            print('receive_award')
            current_action = 'receive_award'
            time.sleep(0.1)  # 缩减暂停时间
            continue


        #  第五顺位判断 treasure_box
        template, w, h = get_template('treasure_box')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][0], loc[0][0]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2, button='left')
            print('treasure_box')
            current_action = 'treasure_box'
            time.sleep(0.5)
            continue





        # 最后的顺位判断   什么都没有了 向前移动  或者向后移动
        template, w, h = get_template('catalogue')
        # 使用模板匹配算法
        res = cv2.matchTemplate(screenshot_cv2, template, cv2.TM_CCOEFF_NORMED)
        # 设定阈值和获取匹配位置
        threshold = 0.8
        loc = np.where(res >= threshold)  # tuple 里面是两个list
        # 获取第一个出现的 loc
        if len(loc) == 2 and len(loc[0]) >= 1:
            pt = tuple((loc[1][0], loc[0][0]))  # 需要颠倒一下顺序
            pyautogui.click(pt[0] + w / 2, pt[1] + h/2 -200 , button='left') # -200 地面的位置  可以用微信截图测量
            print('catalogue')
            current_action = 'catalogue'
            time.sleep(1.0)# 移动的等待时间长一点
            continue

        print('No operation is performed!')
        current_action = 'No operation is performed!'
def stop_task():
    # 停止任务的方法（暂未实现）
    global sign1
    sign1 = False
    print("Task is stopped.")

# 创建主窗口
root = tk.Tk()
root.title("yys_script_v1.0")
# 设置窗口大小
root.geometry("400x600+10+10")
# 创建开始按钮和停止按钮，并绑定事件处理函数
start_button = tk.Button(root,width=10,height=3, text="Start(F5)", command=start_task)
start_button.pack()
start_button.place(x=50, y=10)

stop_button = tk.Button(root, width=10,height=3,text="Stop(F6)", command=stop_task)
stop_button.pack()
stop_button.place(x=50, y=100)
# 将键盘事件和摁键事件绑定到相同的两个函数当中
# def on_key_press(event):
#     if event.keysym == "F5":
#         start_task()
#     elif event.keysym == "F6":
#         stop_task()
# # # 将键盘事件绑定到窗口
# root.bind("<Key>", on_key_press)
# #root.bind_all("<Key>", on_key_press)
import keyboard
def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'f5':
            start_task()
        elif event.name == 'f6':
            stop_task()
# 开始监听键盘事件
keyboard.on_press(on_key_event)



# root.grab_set_global()
# # 监听全局键盘事件
# from pynput.keyboard import Key, Listener
# with Listener(on_press=on_key_press) as listener:
#     listener.join()
# # 将焦点设置为当前窗口
# root.grab_set_global()
# 创建标签并添加到窗口中
label1 = tk.Label(root, text="战斗执行次数：")
label1.pack()
label1.place(x=50, y=200)

label2 = tk.Label(root, text=f"{fight_count}")
label2.pack()
label2.place(x=180, y=200)

label3 = tk.Label(root, text="副本次数：")
label3.pack()
label3.place(x=50, y=300)

label4 = tk.Label(root, text=f"{boss_fight_count}")
label4.pack()
label4.place(x=180, y=300)

label5 = tk.Label(root, text="是否正在执行脚本：")
label5.pack()
label5.place(x=50, y=400)

label6 = tk.Label(root, text="否")
label6.pack()
label6.place(x=180, y=400)

label7 = tk.Label(root, text="当前在执行的动作：")
label7.pack()
label7.place(x=50, y=450)

label8 = tk.Label(root, text="")
label8.pack()
label8.place(x=180, y=450)

from tooltip import Tooltip
label9 = tk.Label(root, text="脚本开发信息提示框")
label9.pack()
label9.place(x=50, y=500)
# 创建一个提示框，并将其绑定到按钮上
tooltip9 = Tooltip(label9, "基于python-opencv cv2.matchTemplate图片模板匹配，以及pyautogui鼠标模拟，gui界面基于tkinter开发的阴阳师脚本")


label10 = tk.Label(root, text="v1.0版本改进信息提示框")
label10.pack() # pack 打包放起来
label10.place(x=50, y=530)
tooltip10 = Tooltip(label10, "treasure_box和receive_award互换判断顺位，改进big_treasure_box模板匹配图片，加入自动拒绝悬赏邀请,加入阴阳师图标")

label11 = tk.Label(root, text="注意信息提示框")
label11.pack() # pack 打包放起来
label11.place(x=50, y=560)
tooltip11 = Tooltip(label11, "隔离沙箱打开yys桌面版，可避免检测以及避免管理员权限。\n桌面版默认大小在1k分辨率屏幕下，可以移动位置。不能遮挡，需要在屏幕中截图。\n不要开启悬赏的追踪功能，影响战斗图标模板。")

def update_label():
    label2.config(text=f"{fight_count+boss_fight_count}")
    label4.config(text=f"{boss_fight_count}")
    if sign1:
        label6.config(text="是")
    else:
        label6.config(text="否")
    label8.config(text=current_action)
    # 设置下一次更新的时间间隔（毫秒）
    root.after(1000, update_label)
# 初始化时立即调用更新函数开始自动更新
update_label()
root.update()
# 运行主循环
root.mainloop()