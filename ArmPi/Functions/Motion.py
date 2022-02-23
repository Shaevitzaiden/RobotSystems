#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/aiden/RobotSystems/ArmPi/')
import cv2
import time
import Camera
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *


class MotionPrimitives:
    def __init__(self) -> None:
        self.is_moving = False
        self.action_finished = False
        self.unreachable = False
        self.goal = ()
        
    def 


