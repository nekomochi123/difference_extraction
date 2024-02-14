import cv2
import numpy as np
from PIL import Image
import os
import tkinter as tk
import re
import glob
import sys
from tkinter import filedialog
from tkinter import messagebox
from matplotlib import pyplot as plt
import tkinter.filedialog
import time


def main():
    root = tk.Tk()
    root.withdraw()
    iDir = os.path.abspath(os.path.dirname(__file__))
    temp_path = templates_path(iDir) 
    img_path = images_path(iDir)  
    img_gray = images_import(img_path)
    tmp_gray = templates_import(temp_path)
    matching_points = templates_matching(img_gray, tmp_gray)
    img_trim = images_trimming(matching_points, img_gray)


def templates_path(iDir):
    temp_folder_path = os.path.abspath(os.path.join(iDir, "template"))
    temp_folder_select = filedialog.askdirectory(initialdir=temp_folder_path)
    path = glob.glob(temp_folder_select + "/*.jpg")  
    if len(path) != 2:
        messagebox.showerror("エラー", "フォルダ内の画像は2枚にしてください。")
        sys.exit()
    temp_path = [re.sub(r"\\", "/", path[i]) for i in range(len(path))]  
    if "left" not in os.path.basename(temp_path[0]):
        temp_path[0], temp_path[1] = temp_path[1], temp_path[0]  
    return temp_path


def images_path(iDir):
    typ = [("jpgファイル", "*.jpg")]
    img_path = [
        filedialog.askopenfilename(filetypes=typ, initialdir=iDir) for i in range(2)
    ]
    return img_path


def images_import(img_path):
    buf = [
        np.fromfile(img_path[i], np.uint8) for i in range(len(img_path))
    ]
    img = [
        cv2.imdecode(buf[j], cv2.IMREAD_UNCHANGED) for j in range(len(img_path))
    ]
    img_gray = [
        cv2.cvtColor(img[k], cv2.COLOR_RGB2GRAY) for k in range(len(img))
    ]
    return img_gray


def templates_import(temp_path):
    buf = [np.fromfile(temp_path[i], np.uint8) for i in range(len(temp_path))]
    tmp = [cv2.imdecode(buf[j], cv2.IMREAD_UNCHANGED) for j in range(len(temp_path))]
    tmp_gray = [cv2.cvtColor(tmp[k], cv2.COLOR_RGB2GRAY) for k in range(len(tmp))]
    return tmp_gray


def templates_matching(img_gray, tmp_gray):
    before_results = [
        cv2.matchTemplate(img_gray[0], tmp_gray[i], cv2.TM_CCOEFF_NORMED)
        for i in range(len(img_gray))
    ]
    after_results = [
        cv2.matchTemplate(img_gray[1], tmp_gray[j], cv2.TM_CCOEFF_NORMED)
        for j in range(len(tmp_gray))
    ]
    before_idx = [cv2.minMaxLoc(before_results[k]) for k in range(len(before_results))]
    after_idx = [cv2.minMaxLoc(after_results[l]) for l in range(len(after_results))]
    matching_points = []
    for m in range(2):
        matching_points.append(before_idx[m][3])
    for n in range(2):
        matching_points.append(after_idx[n][3])
    return matching_points


def images_trimming(matching_points, img_gray):
    offset_left_up = -30
    offset_right_bottom = 830 

    trim_left_bf = [offset_left_up + matching_points[0][i] for i in range(2)]
    trim_left_af = [offset_left_up + matching_points[2][j] for j in range(2)]
    trim_right_bf = [offset_right_bottom + matching_points[1][k] for k in range(2)]
    trim_right_af = [offset_right_bottom + matching_points[3][l] for l in range(2)]

    img_trim_bf = img_gray[0][
        trim_left_bf[1] : trim_right_bf[1], trim_left_bf[0] : trim_right_bf[0]
    ]
    img_trim_af = img_gray[1][
        trim_left_af[1] : trim_right_af[1], trim_left_af[0] : trim_right_af[0]
    ]
    return img_trim_bf, img_trim_af
def brightness_adjustment(img_trim):
    for i in range(1, 2):
        plt.subplot(4, 4, i)
        plt.imshow(img_trim[i])
        plt.colorbar()


main()