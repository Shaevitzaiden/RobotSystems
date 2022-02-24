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


class Motion:
    def __init__(self, arm) -> None:
        self.is_moving = False
        self.grasping = False
        self.servo1 = 500
        self.arm = arm

        # Placement positions 
        self.quick_place_coords = {
            'red':   (-15 + 0.5, 12 - 0.5, 1.5),
            'green': (-15 + 0.5, 6 - 0.5,  1.5),
            'blue':  (-15 + 0.5, 0 - 0.5,  1.5),
        }

    def stack(self, blocks, stack_pose=(0, 10, 1.5, 0), order=('red','green','blue')):
        """ Sequentially stacks blocks
        :params dict blocks: dictionary of blocks with keys as color and items as poses (x_c, y_c, rotation_angle)
        :params 
        """
        for i in range(3):
            if i > 0:
                stack_pose[2] += 1.5
            try:
                pose = blocks[order[i]]
                self.pick_and_place(pose, stack_pose)
            except KeyError:
                pass
    
    def sort(self, blocks, order=('red','green','blue')):
        

    def pick_and_place(self, pose, new_pose):
        """ Picks up a block and places it somewhere
        :params tuple pose: (x_center, y_center, rotation_angle) for block
        :params tuple new_pose: (x_new, y_new, z_new, rotation_angle) for block 
        """
        # Lower arm
        self.move_arm(pose[0], pose[1]-2, 5, -90, -90, 0)
        
        # Open and rotate gripper
        self.open_gripper()
        self.rotate_gripper(getAngle(pose[0], pose[1], pose[2]))

        # Move into grabbing position
        self.move_arm(pose[0], pose[1], 0, -90, -90, 0)

        # Close gripper
        self.close_gripper()

        # Move block to (x, y, z)
        self.move_arm(new_pose[0], new_pose[1], new_pose[2], -90, -90, 0)

        # Rotate gripper and release
        self.rotate_gripper(getAngle(new_pose[0], new_pose[1], new_pose[3]))
        self.open_gripper()

    def move_arm(self, x, y, z, a0, a1, a2):
        self.arm.setPitchRangeMoving((x, y, z), a0, a1, a2)
        time.sleep(0.2)
       
    def open_gripper(self):
        Board.setBusServoPulse(1, self.servo1 - 280, 500)
        self.grasping = True
        time.sleep(2)

    def close_gripper(self):
        Board.setBusServoPulse(1, self.servo1 - 50, 500)
        self.grasping = False 
        time.sleep(2)

    def rotate_gripper(self, angle):
        Board.setBusServoPulse(2, angle, 500)
        time.sleep(2)

    def reset(self):
        self.close_claw()
        self.rotate_gripper(500)
        self.move_arm(0, 10, 10, -30, -30, -90)
    

if __name__ == "__main__":
    arm = ArmIK()
    mp = Motion(arm)

    mp.move_arm(-8, 25, 10, -30, -30, -90)
    mp.open_gripper()
    mp.close_gripper()
    mp.rotate_gripper(90)

    mp.reset()
