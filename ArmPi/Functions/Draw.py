#!/usr/bin/python3
# coding=utf8
import numpy as np
import sys
# import pandas as pd
sys.path.append('/home/aiden/RobotSystems/ArmPi/')
import time
from math import sqrt
# from LABConfig import *
# from ArmIK.Transform import *
# from ArmIK.ArmMoveIK import *
# import HiwonderSDK.Board as Board
# from CameraCalibration.CalibrationConfig import *
from Motion import Motion
from DoodleInput import DoodleInput


class DoodleDraw(Motion):
    def __init__(self) -> None:
        super().__init__()
        self.coords = None
        self.reset() # reset arm position to start
        self.current_xy = (0, 10) # starting position
    
    def draw(self, coords_array):
        self.coords = coords_array
        self._preproces_coords()
        
        self.move_arm(self.coords[0,0]-7.5,self.coords[0,1],-1,-90,-90,0)
        time.sleep(1)
        for i in range(len(self.coords)):
            self.move_arm(self.coords[i,0]-7.5, self.coords[i,1],-1,-90,-90,0)

    def _preproces_coords(self):
        # Center drawing 
        self.coords[:,0] = self.coords[:,0] - (np.amax(self.coords[:,0]) + np.amin(self.coords[:,0]))/2
        self.coords[:,1] = self.coords[:,1] - (np.amax(self.coords[:,1]) + np.amin(self.coords[:,1]))/2
        
        # scale drawing to drawable region
        self.coords = self.coords / 10 # naive but seems to work fine

        # Round and remove duplicates to speed up drawing
        self.coords = np.round(self.coords, 2)
        while i < len(self.coords):
            if (self.coords[i] == self.coords[i-1]).all():
                self.coords = np.delete(self.coords, i-1, 0)
            else:
                i += 1
        
        


    


if __name__ == "__main__":
    doodle = DoodleInput()
    drawer = DoodleDraw()
    
    drawer.draw(doodle.coords)



    # arm = Motion()
    # doodle = DoodleInput()
    
    # # coords = pd.read_csv('draw_coords.csv')
    # # coords = coords.to_numpy()
    # coords = np.loadtxt('draw_coords.csv', delimiter=",")
    # coords = coords/10
    # coords = np.round(coords, 2)
    
    # coords[:,0] -= 10
    # coords[:,1] += 1
    
    # i = 1
    # while i < len(coords):
    #     if (coords[i] == coords[i-1]).all():
    #         coords = np.delete(coords, i-1, 0)
    #     else:
    #         i += 1
    
    # print("Starting Masta' Peace! (˘ ³˘)♥ ")
    
    # arm.move_arm(coords[0,0]-7.5,coords[0,1],-1,-90,-90,0)
    # time.sleep(1)
    # for i in range(len(coords)):
    #     arm.move_arm(coords[i,0]-7.5,coords[i,1],-1,-90,-90,0)
        
    # arm.reset()
    # print("All done!")
