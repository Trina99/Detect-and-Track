from audioop import avg
from datetime import datetime
from distutils.spawn import spawn
import cv2 as cv
from cv2 import threshold
from matplotlib.pyplot import draw
import numpy as np
from time import time,sleep
from tese.windowcapture import WindowCapture
from tese.vision import Vision
# from windowcapture import WindowCapture
# from vision import Vision
import threading
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# user variables
# threshold = 0.65
# window = 'Brawlhalla'
# img_path = 'tese/spawn_weapon_2.jpg'


def list_windows():
    # shows all the open window names
    windows = WindowCapture.list_window_names()
    print(windows)
    return windows

def execute(window = 'None', threshold = 0.65, stop=False):

    # avg_fps = 0
    # loops_number = 0
    fpsss = []
    # initialize the WindowCapture class
    wincap = WindowCapture(window)
    thr = threading.Thread(target=sleep, args=(1))

    # wincap = WindowCapture()
    # initialize the Vision class
    # print(os.getcwd())
    img_path="imgs/target.png"
    spawn_weapon = Vision(img_path)

    # de quantas em quantas iterações corre o object detection
    obj_det_run = 10
    i = obj_det_run
    rectangles = []
    beggining_time = time()
    loop_time = beggining_time
    first_run = True
    # rectangles = []
    # screenshot = None
    # threads=[]
    # t1 = None
    # detecting = False

    while(True):
        # get an updated image of the game
        screenshot = wincap.get_screenshot()

        if not thr.is_alive() and spawn_weapon.new_trackers != []:
            spawn_weapon.tracks = spawn_weapon.new_trackers
            spawn_weapon.new_trackers = []

        if i >= obj_det_run:
            # display the processed image
            if not thr.is_alive():
                rectangles = spawn_weapon.find(screenshot, float(threshold))

                # inicializa o track de cada quadrado
                # beg = time()
                if len(rectangles) > 0:
                    thr = threading.Thread(target=spawn_weapon.init_tracks, args=(screenshot,))
                    thr.start()
                i = 0

            if first_run and len(rectangles) > 0: 
                first_run = False
                thr.join()
                spawn_weapon.tracks = spawn_weapon.new_trackers
                spawn_weapon.new_trackers = []
            # print(f"init tracks time: {time() - beg}")
            # detecting = True
        


        # calcula e mostra os fps
        fps = 1 / (time() - loop_time)
        # print('FPS {}'.format(fps))
        
        fpsss.append(fps)
        # loops_number += 1
        # avg_fps = avg_fps + ((fps - avg_fps)/loops_number)

        loop_time = time()

        # spawn_weapon.track(screenshot)

        threads = spawn_weapon.th_track(screenshot)
        for th in threads:
            th.join()

        # desenha os quadrados detetados
        spawn_weapon.draw(screenshot)
        i += 1

        cv.namedWindow("Matches", cv.WINDOW_NORMAL)
        #cv.setWindowProperty("Matches", cv.WND_PROP_TOPMOST, cv.WINDOW_FULLSCREEN)
        cv.imshow('Matches', screenshot)

        # press 'q' with the output window focused to exit
        if cv.waitKey(1) == ord('q') or stop():
            cv.destroyAllWindows()
            break
    # print(window, img_path, threshold)
    print('Done.')

    now = datetime.now().strftime("%d-%m-%Y_%H.%M.%S")
    print(now)
    pname = "".join(letra for letra in window if letra.isalnum())
    f = open(f"videos\\{pname}.{now}", "a")
    f.write("Info:\n")
    f.write(f"Total time ran: { time() - beggining_time }\n")
    toPrint = min(fpsss)
    f.write(f"Min FPS: {toPrint}\n")
    toPrint = max(fpsss)
    f.write(f"Max FPS: {toPrint}\n")
    toPrint = sum(fpsss) / len(fpsss)
    f.write(f"Average FPS: {toPrint}\n")
    f.write(f"Average detection precision: {spawn_weapon.avg_precision}\n")
    f.close()



# shows all the open window names
# list_windows()

# execute('PokeММO',0.65)