import cv2 as cv
from cv2 import threshold
from matplotlib.pyplot import draw
import numpy as np
from time import time
from tese.windowcapture import WindowCapture
from tese.vision import Vision
import threading
import os


# shows all the open window names
# WindowCapture.list_window_names()

# user variables
# threshold = 0.65
# window = 'Brawlhalla'
# img_path = 'tese/spawn_weapon_2.jpg'


def execute(window = 'Brawlhalla', threshold = 0.65):

    # initialize the WindowCapture class
    wincap = WindowCapture(window)
    # wincap = WindowCapture()
    # initialize the Vision class
    print(os.getcwd())
    img_path="rest_api/tese/imgs/spawn_weapon_2.jpg"
    spawn_weapon = Vision(img_path)

    # de quantas em quantas iterações corre o object detection
    obj_det_run = 10
    i = obj_det_run
    loop_time = time()
    rectangles = []
    screenshot = None
    threads=[]
    t1 = None
    detecting = False

    while(True):
        # get an updated image of the game
        screenshot = wincap.get_screenshot()

        if i == obj_det_run:
            # display the processed image
            # rectangles = spawn_weapon.find(screenshot, threshold)

            # corre o spawn_weapon.find em background
            t1 = threading.Thread(target=spawn_weapon.find, args=(wincap.get_screenshot(), threshold))
            t1.start()
            # inicializa o track de cada quadrado
            # spawn_weapon.init_tracks(screenshot)
            # detecting = True
            i = 0
        
        # calcula e mostra os fps
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        # spawn_weapon.track(screenshot)
        # corre o spawn_weapon.track que devolve threads
        # if detecting:
        #     detecting = False
            # t1.join()

        threads = spawn_weapon.th_track(screenshot)
        for th in threads:
            th.join()

        # desenha os quadrados detetados
        spawn_weapon.draw(screenshot)
        i += 1

        # cv.namedWindow("Matches", cv.WND_PROP_FULLSCREEN)
        # cv.setWindowProperty("Matches", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow('Matches', screenshot)

        # press 'q' with the output window focused to exit
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    print(window, img_path, threshold)
    print('Done.')

# run()