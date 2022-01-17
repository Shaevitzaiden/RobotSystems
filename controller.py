from picarx_improved import Picarx
from time import sleep

class Controller():
    def __init__(self, picarx, scaling_factor=1):
        self.px = picarx
        self.scaling_factor = scaling_factor

    def follow_line(self, mag):
        angle = -self.scaling_factor * 40 * mag
        self.px.set_dir_servo_angle(angle)
        self.px.forward(40)
        return angle


if __name__ == "__main__":
    px = Picarx()
    c = Controller(px)