import os
from cv2 import cv2
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
adb = ".\\tools\\adb.exe "


def loadImg(filepath):
    return cv2.cvtColor(cv2.imread(filepath), cv2.CV_8U)

def touch(x, y):
    os.system(adb+"shell input tap %s %s" % (x, y))


def screenCap():
    os.system(adb+"shell screencap -p /mnt/shared/MuMu共享文件夹/screen.png")
    os.system(adb+"pull /mnt/shared/MuMu共享文件夹/screen.png .\\cache\\screen.png |echo off")
    return loadImg(".\\cache\\screen.png")
class arknight():
    normal_start_img = None
    normal_start2_img = None
    normal_end_img = None

    def init(self):
        os.system(adb+"kill-server")
        os.system(adb+"connect 127.0.0.1:7555")
        os.system(adb+"remount |echo off")
        self.normal_start_img = loadImg(".\\picture\\normal_start.png")
        self.normal_start2_img = loadImg(".\\picture\\normal_start_2.png")
        self.normal_end_img = loadImg(".\\picture\\normal_end.png")

    def exit(self):
        os.system(adb+"disconnect 127.0.0.1:7555")
        os.system(adb+"kill-server")

    def normal_start(self):
        touch("1283.5", "740.5")

    def normal_start_2(self):
        touch("1241.5","569.5")

    def normal_end(self):
        touch("720","405")

    def showimgtm(self, screen, loc, img):
        shape = img.shape
        cv2.rectangle(
            screen, loc, (loc[0]+shape[1], loc[1]+shape[0]), (0, 0, 255), thickness=5)
        plt.imshow(screen)
        plt.show()



    def matchTemp(self, screen ,img):
        res = cv2.matchTemplate(screen, img, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #print(max_loc[0]+img.shape[1]/2, max_loc[1]+img.shape[0]/2)
        return (max_loc[0]+img.shape[1]/2, max_loc[1]+img.shape[0]/2)

    def normal_circle(self,count:int):
        with tqdm(total=count,desc="刷图进度") as pbar:
            for c in range(count):
                if(c <= count):
                    while(True):
                        screen = screenCap()
                        if(self.matchTemp(screen,self.normal_start_img)==(1283.5, 740.5)):
                            self.normal_start() 
                        if(self.matchTemp(screen,self.normal_start2_img)==(1241.5,569.5)):
                            self.normal_start_2()
                        if(self.matchTemp(screen,self.normal_end_img)==(1070.5,548.5)):
                            self.normal_end()
                            pbar.update(1)
                            break
                        time.sleep(3)
                else:
                    break



if __name__ == "__main__":
    arknight = arknight()
    arknight.init()
    while(True):
        print("1)普通模式")
        print("2)剿灭模式(暂无)")
        print("3)退出")
        mode = int(input("选择模式:"))
        if(mode == 1):
            arknight.normal_circle(int(input("输入刷图次数:")))
        elif(mode == 2):
            print("暂不开放")
        elif(mode == 3):
            arknight.exit()
            break
