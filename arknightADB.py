from subprocess import Popen
from cv2 import cv2
import time
from tqdm import tqdm
adb = ".\\tools\\adb.exe "
env = {"PATH":".\\tools"}

def loadImg(filepath):
    return cv2.cvtColor(cv2.imread(filepath), cv2.CV_8U)


def touch(x, y):
    adb_cmd(["shell","input","tap",str(x),str(y)])


def screenCap():
    adb_cmd(["shell","screencap","-p","/mnt/shared/MuMu共享文件夹/screen.png"])
    adb_cmd(["pull","/mnt/shared/MuMu共享文件夹/screen.png",".\\cache\\screen.png"])
    return loadImg(".\\cache\\screen.png")

def adb_cmd(command:list)-> Popen:
    temp = [adb]
    temp.extend(command)
    return Popen(temp,env=env)
class arknight():
    normal_start_img = None
    normal_start2_img = None
    normal_end_img = None
    lizhi_img = None

    def init(self) -> None:
        adb_cmd(["kill-server"])
        adb_cmd(["connect","127.0.0.1:7555"])
        adb_cmd(["remount"])
        self.normal_start_img = loadImg(".\\picture\\normal_start.png")
        self.normal_start2_img = loadImg(".\\picture\\normal_start_2.png")
        self.normal_end_img = loadImg(".\\picture\\normal_end.png")
        self.lizhi_img = loadImg(".\\picture\\lizhi.png")

    def exit(self):
        adb_cmd(["disconnect","127.0.0.1:7555"])
        adb_cmd(["kill-server"])

    def normal_start(self):
        touch("1283.5", "740.5")

    def normal_start_2(self):
        touch("1241.5", "569.5")

    def normal_end(self):
        touch("720", "405")

    def lizhi(self):
        touch("1230", "650")

    def matchTemp(self, screen, img):
        res = cv2.matchTemplate(screen, img, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #print(max_loc[0]+img.shape[1]/2, max_loc[1]+img.shape[0]/2)
        return (max_loc[0]+img.shape[1]/2, max_loc[1]+img.shape[0]/2)

    def normal_circle(self, count: int, mode: bool):
        with tqdm(total=count, desc="刷图进度") as pbar:
            for c in range(count):
                if(c <= count):
                    while(True):
                        screen = screenCap()
                        if(self.matchTemp(screen, self.lizhi_img) == (1307.5, 451.0) and mode):
                            self.lizhi()
                        if(self.matchTemp(screen, self.normal_start_img) == (1283.5, 740.5)):
                            self.normal_start()
                        if(self.matchTemp(screen, self.normal_start2_img) == (1241.5, 569.5)):
                            self.normal_start_2()
                        if(self.matchTemp(screen, self.normal_end_img) == (1070.5, 548.5)):
                            self.normal_end()
                            break
                        time.sleep(3)
                    pbar.update(1)
                else:
                    break


if __name__ == "__main__":
    arknight = arknight()
    arknight.init()
    while(True):
        print("1)普通模式")
        print("2)普通模式(碎石)")
        print("3)剿灭模式(暂无)")
        print("4)剿灭模式(碎石)")
        print("5)截图")
        print("6)退出")
        mode = int(input("选择模式:"))
        if(mode == 1):
            arknight.normal_circle(int(input("输入刷图次数:")), False)
        elif(mode == 2):
            arknight.normal_circle(int(input("输入刷图次数:")), True)
        elif(mode == 3):
            print("暂无")
        elif(mode == 4):
            print("暂无")
        elif(mode == 5):
            screenCap()
        elif(mode == 6):
            arknight.exit()
            break
