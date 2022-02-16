#!/usr/bin/python3
# coding=utf8
from msilib.schema import Class
import sys
sys.path.append('/home/aiden/RobotSystems/ArmPi/')
import cv2
import time
import Camera
import threading
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *


class Perception():
    def __init__(self, camera) -> None:
        self.range_rgb = {
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255)
        }
        
        self.size = (640, 480)

        # Garbo
        self.count = 0
        self.track = False
        self._stop = False
        self.get_roi = False
        self.first_move = True
        self.center_list = []
        self.isRunning = False
        self.detect_color = 'None'
        self.action_finish = True
        self.start_pick_up = False
        self.target_color = ()
        self.start_count_t1 = True
        
        # Camera from which to receive frames
        self.camera = camera
        self.camera.camera_open() 

    def get_frame(self, show_frame=False):
        img = self.camera.frame
        frame = img.copy()
        return frame
    
    def preprocess(self, frame):
        frame_copy = frame.copy() # make a copy of the already copied frame?
        img_h, img_w = frame.shape[:2]  # get image dimensions
        cv2.line(frame, (0, int(img_h / 2)), (img_w, int(img_h / 2)), (0, 0, 200), 1)
        cv2.line(frame, (int(img_w / 2), 0), (int(img_w / 2), img_h), (0, 0, 200), 1)
        
        
        frame_resize = cv2.resize(frame_copy, self.size, interpolation=cv2.INTER_NEAREST) # resizes the frame to be smaller, size is set outside the function -------------> bad
        frame_gb = cv2.GaussianBlur(frame_resize, (11, 11), 11) # apply gaussian smoothing to resized frame
           
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # Convert image to LAB space
        return frame_lab

    def find_cube(self, frame_lab):
        """ Finds a cube in a frame if it exists
        :params frame: a frame in LAB space that has undergone preprocessing
        :return: None if no cube found, returns center of cube if found
        """
        for i in color_range:  # loop over the "color range" which isn't defined anywhere somehow
            if i in self.target_color:  # and if the color is the target color
                detect_color = i  # = the target color
                frame_mask = cv2.inRange(frame_lab, color_range[detect_color][0], color_range[detect_color][1])  # Makes a black and white image where the color of interest (of a block) is between the range making it white and the background black
                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))  # open operation
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6, 6), np.uint8))  # closed operation: attempts to remove false negatives imposed by the opening procedure
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # find the outline
                areaMaxContour, area_max = self.getAreaMaxContour(contours)  # find the largest contour (ideally the block) and return its area
        if area_max > 2500:  # have found the largest area
            rect = cv2.minAreaRect(areaMaxContour) # places a rectangle around the contour (again ideally the block)
            box = np.int0(cv2.boxPoints(rect))  # not sure tbh

            roi = getROI(box) # get roi
            get_roi = True 

            img_centerx, img_centery = getCenter(rect, roi, self.size, square_length)  # Get the coordinates of the center of the block
            world_x, world_y = convertCoordinate(img_centerx, img_centery, self.size) # Convert to real world coordinates

    def reset(self) -> None:
        """ Reset all defaults, no parameters, returns nothing"""
        self.count = 0
        self.track = False
        self._stop = False
        self.get_roi = False
        self.first_move = True
        self.center_list = []
        self.isRunning = False
        self.detect_color = 'None'
        self.action_finish = True
        self.start_pick_up = False
        self.target_color = ()
        self.start_count_t1 = True
 
    @staticmethod
    def getAreaMaxContour(contours):
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours:  # iterate over all contours
            contour_area_temp = math.fabs(cv2.contourArea(c))  # calculate the contour area
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp > 300:  # The contour with the largest area is valid only if the 
                                            # area is greater than 300 to filter out the noise
                    area_max_contour = c

        return area_max_contour, contour_area_max  # returns the largest contour

    