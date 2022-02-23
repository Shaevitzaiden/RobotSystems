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
    def __init__(self, arm) -> None:
        self.is_moving = False
        self.action_finished = False
        self.unreachable = False
        self.goal = ()
        self.servo1 = 500
        
    def open_claw(self):
        Board.setBusServoPulse(1, self.servo1 - 280, 500)  # paws open
        time.sleep(1)

    def close_claw(self):
        Board.setBusServoPulse(1, self.servo1 - 200, 500)  # Claws open to drop objects
        time.sleep(1)

    def rotate_gripper(self, angle):
        Board.setBusServoPulse(2, angle, 500)


if __name__ == "__main__":
    arm = ArmIK()
    mp = MotionPrimitives(arm)

    mp.open_claw()
    mp.close_claw()
    mp.rotate_gripper(90)
