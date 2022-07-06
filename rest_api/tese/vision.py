import cv2 as cv
import numpy as np
import threading

class Vision: 
    # properties
    needle_img = None
    w = 0
    h = 0
    method = None
    rectangles = []
    # tracker_type = "GOTURN"
    tracks = []

    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        
        # self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        self.needle_img = cv.imread(needle_img_path, 1)
        # print(self.needle_img)
        # Save the dimensions of the needle image
        self.w = self.needle_img.shape[1]
        self.h = self.needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method
        self.rectangles = []

    # encontra todas as needle_img em haystack_img
    # devolve lista de retangulos
    def find(self, haystack_img, threshold=0.7):

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        # rectangles = list(self.rectangles)
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.w, self.h]
            rectangles.append(rect)
            rectangles.append(rect)

        aux, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        self.rectangles = aux
        self.init_tracks(haystack_img)
        return aux

    # inicializa goturn tracker de todos os retangulos no frame
    def init_tracks(self, frame):
        aux_track = []
        for bbox in self.rectangles:
            tracker = cv.TrackerGOTURN_create()
            # tracker = cv.TrackerMIL_Create()
            tracker.init(frame, bbox)
            aux_track.append(tracker)
        self.tracks = aux_track

    def track(self, frame):
        aux_bb=[]
        for tr in self.tracks:
            # Update tracker
            ok, bbox = tr.update(frame)
            aux_bb.append(bbox)
        self.rectangles = aux_bb

    def th_track(self, frame):
        aux_bb=[]
        threads=[]
        for tr in self.tracks:
            t1 = threading.Thread(target=self.update_tracker, args=(frame, aux_bb, tr))
            t1.start()
            threads.append(t1)
            # t1.start()
            # Update tracker
            # ok, bbox = tr.update(frame)
            # aux_bb.append(bbox)
        # for th in threads:
        #     th.start()
        self.rectangles = aux_bb
        return threads

    def update_tracker(self, frame, bboxes, tr):
        # Update tracker
        ok, bbox = tr.update(frame)
        bboxes.append(bbox)

    def draw(self, haystack_img):
        if len(self.rectangles):
            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv. MARKER_CROSS

            # Loop over all the locations and draw their rectangle
            for (x, y, w, h) in self.rectangles:
                # Determine the center position
                # center_x = x + int(w/2)
                # center_y = y + int(h/2)
                # Save the points
                # points.append((center_x, center_y))

                # Determine the box position
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                            lineType=line_type, thickness=2)

        
# points = findClickPositions('spawn_weapon.jpg', 'brawlhalla_game_2.jpg', threshold=0.75, debug_mode='rectangles')
# print(points)
# print('Done.')