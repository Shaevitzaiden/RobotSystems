#!/usr/bin/python3
# coding=utf8
import numpy as np
import time
from math import sqrt
import sys

sys.path.append('/home/aiden/RobotSystems/ArmPi/')
from Motion import Motion
from DoodleInput import DoodleInput


class DoodleDraw(Motion):
    def __init__(self) -> None:
        super().__init__()
        self.coords = None
        self.reset() # reset arm position to start
        # time.sleep(0.5)
        self.start_xy = (0, 10) # starting position
    
    def draw(self, coords_array):
        self.coords = coords_array
        self._preproces_coords()
        
        self.move_arm(self.coords[0,0],self.coords[0,1],4,-90,-90,0)
        time.sleep(1)
        
        for i in range(len(self.coords)-1):
            self.move_arm(self.coords[i,0], self.coords[i,1],-1,-90,-90,0)
            time.sleep(0.1)
            # Check if next point is discontinuous and if so lift up and go to next point
            coord_dist = sqrt((self.coords[i+1,0]-self.coords[i,0])**2 + (self.coords[i+1,1]-self.coords[i,1])**2)
            if coord_dist > 0.5:
                self._reposition((self.coords[i,0], self.coords[i,1]), (self.coords[i+1,0], self.coords[i+1,1]))
        self.reset()

    def _reposition(self, current_point, next_point):
        # give it a moment to finish previous motion
        time.sleep(0.5)
        
        # lift arm
        self.move_arm(current_point[0], current_point[1], 4, -90, -90, 0)

        # move arm to hover above next point
        self.move_arm(next_point[0], next_point[1], 4, -90, -90, 0)
        time.sleep(1)
        
    def _preproces_coords(self):
        # Center drawing 
        self.coords[:,0] = self.coords[:,0] - (np.amax(self.coords[:,0]) + np.amin(self.coords[:,0]))/2
        self.coords[:,1] = self.coords[:,1] - np.amin(self.coords[:,1])
        # scale drawing to drawable region
        self.coords = self.coords / 10 # naive but seems to work fine
        self.coords[:,1] += 7.5
        # Round and remove duplicates to speed up drawing
        self.coords = np.round(self.coords, 2)
        i = 1
        while i < len(self.coords):
            if (self.coords[i] == self.coords[i-1]).all():
                self.coords = np.delete(self.coords, i-1, 0)
            else:
                i += 1


if __name__ == "__main__":
    doodle = DoodleInput()
    drawer = DoodleDraw()
    
    drawer.draw(doodle.coords)

