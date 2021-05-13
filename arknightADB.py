import os
from sys import stdout
from cv2 import cv2
import time
from tqdm import tqdm


adb = ".\\tools\\adb.exe"

normal_start_img = None
normal_start2_img = None
normal_end_img = None
lizhi_img = None


def loadImg(filepath):
    return cv2.cvtColor(cv2.imread(filepath), cv2.CV_8U)


def touch(x, y):
    os.system(build_adbshell_cmd("shell input tap %s %s" % (str(x), str(y))))


def screenCap():
    os.system(build_adbshell_cmd("shell screencap -p /sdcard/screen.png")+"&&"+build_adbshell_cmd("pull /sdcard/screen.png .\\cache\\screen.png|echo off"))
    return loadImg(".\\cache\\screen.png")

def build_adbshell_cmd(cmd):
    return adb+" "+cmd

def normal_start():
    touch("1283.5", "740.5")


def normal_start_2():
    touch("1241.5", "569.5")


def normal_end():
    touch("720", "405")


def lizhi():
    touch("1230", "650")


def matchTemp(screen, img):
    res = cv2.matchTemplate(screen, img, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #print(max_loc[0]+img.shape[1]/2, max_loc[1]+img.shape[0]/2)
    return (max_loc[0]+img.shape[1]/2, max_loc[1]+img.shape[0]/2)


def normal_circle(count: int, mode: bool):
    with tqdm(total=count, desc="刷图进度") as pbar:
        for c in range(count):
            if(c <= count):
                while(True):
                    screen = screenCap()
                    if(matchTemp(screen, lizhi_img) == (1307.5, 451.0) and mode):
                        lizhi()
                    if(matchTemp(screen, normal_start_img) == (1283.5, 740.5)):
                        normal_start()
                    if(matchTemp(screen, normal_start2_img) == (1241.5, 569.5)):
                        normal_start_2()
                    if(matchTemp(screen, normal_end_img) == (1070.5, 548.5)):
                        normal_end()
                        break
                    time.sleep(1)
                pbar.update(1)
            else:
                break


if __name__ == "__main__":
    os.system(adb+" kill-server")
    print("连接模拟器")
    os.system(adb+" connect 127.0.0.1:7555")
    print("ADB进程已启动")
    normal_start_img = loadImg(".\\picture\\normal_start.png")
    normal_start2_img = loadImg(".\\picture\\normal_start_2.png")
    normal_end_img = loadImg(".\\picture\\normal_end.png")
    lizhi_img = loadImg(".\\picture\\lizhi.png")
    print("资源文件已加载")
    print("======加载完毕======")

    while(True):
        print("========菜单========")
        print("1)普通模式")
        print("2)普通模式(碎石)")
        print("3)剿灭模式(暂无)")
        print("4)剿灭模式(碎石)")
        print("5)截图")
        print("6)退出")
        print("========END=========")
        mode = int(input("选择模式:"))
        if(mode == 1):
            normal_circle(int(input("输入刷图次数:")), False)
        elif(mode == 2):
            normal_circle(int(input("输入刷图次数:")), True)
        elif(mode == 3):
            print("暂无")
        elif(mode == 4):
            print("暂无")
        elif(mode == 5):
            screenCap()
            print("保存在cache文件夹里面")
        elif(mode == 6):
            break
    os.system(adb+" disconnect 127.0.0.1:7555")
    os.system(adb+" kill-server")
