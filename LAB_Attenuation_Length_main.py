# 画图包
import matplotlib.pyplot as plt
# 数据分析包
import numpy as np
# GUI包
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
# 音乐包
import pygame 
from pygame import mixer
# 路径包
from pathlib import Path
from os.path import abspath
# 导入自己的辅助函数
import LAB_Attenuation_Length_support
# 拟合函数包
from scipy.optimize import curve_fit
# 数据转化包
import pandas as pd


# 获取路径函数
def LAB_Attenuation_Length_pathin():
    path_string_in = filedialog.askopenfilename()
    path_sv_in.set(path_string_in)

# 保存路径函数
def LAB_Attenuation_Length_pathout():
    path_string_out = filedialog.askdirectory()
    path_sv_out.set(path_string_out)

# 路径地址转真实路径
def path_turn(entry):
    path_str = str(entry.get())
    authentic_path = Path(path_str)
    return authentic_path

# 音乐播放函数
def music():
    mixer.music.load('D:\\STUDY_think\\Data\\LAB-AL-EX-data\\python_control\\audiomass-output.WAV')
    mixer.music.play()

# 绘图函数
def LAB_Attenuation_Length_fig():
    x_L_L, y_ADC, mean_sigma, y_erroy_bar = [],[],[],[]
    pedestal = 0
    path_initial = path_turn(input_e)
    path_mean = path_turn(output_e)
    LAB_Attenuation_Length_support.LAB_Attenuation_Length_getmeandata(path_initial, path_mean)
    LAB_Attenuation_Length_support.LAB_Attenuation_Length_write_meandata(path_mean, x_L_L, y_ADC, mean_sigma, y_erroy_bar)
    print(x_L_L, y_ADC, mean_sigma, y_erroy_bar)
    LAB_Attenuation_Length_support.LAB_Attenuation_Length_figplot(x_L_L, y_ADC, mean_sigma, y_erroy_bar, path_initial, pedestal)
    del x_L_L, y_ADC, mean_sigma, y_erroy_bar, pedestal

# 创建一个空的弹出窗口
main_window = tk.Tk()
main_window.title('LAB光衰减长度拟合')
main_window.geometry('800x500')

# 添加背景图片
BG_photo = Image.open('D:\\STUDY_think\\Data\\LAB-AL-EX-data\\python_control\\EVA.png')
photo = ImageTk.PhotoImage(BG_photo)
canvas = tk.Canvas(main_window, width = 800, height = 600, bd = 0, highlightthickness = 0)
canvas.create_image(400, 250, image = photo)
canvas.place(x = 0, y = 0)

# 添加说明图标
input_lable = tk.Label(main_window, text = '选择输入文件', font = ('Arial',12), bg = 'lime', fg = 'blue', width = 15, height = 1)
input_lable.place(x = 50, y = 50)
# 输入路径定义 # 选取路径按钮 # 音频初始化
mixer.init()
path_sv_in = StringVar()
input_b1 = tk.Button(main_window, text = '点此选择文件路径', font = ('Arial',12), width = 15, height = 1, command = lambda:[LAB_Attenuation_Length_pathin(), music()])
input_b1.place(x = 200, y = 50)
# 输入路径显示框
input_e = tk.Entry(main_window, textvariable = path_sv_in, width = 100)
input_e.place(x = 50, y = 20)

# 添加输出说明图标
output_lable = tk.Label(main_window, text = '选择输出路径', font = ('Arial',12), bg = 'lime', fg = 'blue', width = 15, height = 1)
output_lable.place(x = 50, y = 450)
# 选择数据保存地址
path_sv_out = StringVar()
input_b1 = tk.Button(main_window, text = '点此选择文件路径', font = ('Arial',12), width = 15, height = 1, command = LAB_Attenuation_Length_pathout)
input_b1.place(x = 200, y = 450)
# 保存路径显示框
output_e = tk.Entry(main_window, textvariable = path_sv_out, width = 100)
output_e.place(x = 50, y = 400)

# 添加单张图片绘制按钮
output_b = tk.Button(main_window, text = '点此拟合', font = ('Arial',12), width = 15, height = 1, bg = 'cornflowerblue', fg = 'white',command = LAB_Attenuation_Length_fig)
output_b.place(x = 470, y = 330)

# 刷新窗口
main_window.mainloop()