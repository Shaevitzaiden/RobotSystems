#!/usr/bin/python3
# coding=utf8
import numpy as np
import sys
# import pandas as pd
sys.path.append('/home/aiden/RobotSystems/ArmPi/')
import time
from math import sqrt
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *
from Motion import Motion
from DoodleInput import DoodleInput



if __name__ == "__main__":
    arm = Motion()
    doodle = DoodleInput()
    
    # coords = pd.read_csv('draw_coords.csv')
    # coords = coords.to_numpy()
    coords = np.loadtxt('draw_coords.csv', delimiter=",")
    coords = coords/10
    coords = np.round(coords, 2)
    
    coords[:,0] -= 10
    coords[:,1] += 1
    
    i = 1
    while i < len(coords):
        if (coords[i] == coords[i-1]).all():
            coords = np.delete(coords, i-1, 0)
        else:
            i += 1
    
    print("Starting Masta' Peace! (˘ ³˘)♥ ")
    
    arm.move_arm(coords[0,0]-7.5,coords[0,1],-1,-90,-90,0)
    time.sleep(1)
    for i in range(len(coords)):
        arm.move_arm(coords[i,0]-7.5,coords[i,1],-1,-90,-90,0)
        
    arm.reset()
    print("All done!")