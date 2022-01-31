from picarx_improved import Picarx
from time import sleep

import logging
from logdecorator import log_on_end, log_on_error, log_on_start

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)


class Controller():
    def __init__(self, picarx, scaling_factor=1):
        self.px = picarx
        self.scaling_factor = scaling_factor
        self.ultra_scale = 1

    def __call__(self, mag):
        return self.follow_line(mag)

    @log_on_start(logging.DEBUG, "Controller method started")
    @log_on_error(logging.DEBUG, "Controller method error")
    @log_on_end(logging.DEBUG, "Controller method finished")
    def follow_line(self, mag):
        angle = -self.scaling_factor * 40 * mag
        speed = abs(mag) * 20 + 30
        self.px.set_dir_servo_angle(angle)
        self.px.forward(speed*self.ultra_scale)
        return angle

    def ultrasonic_control(self, scale):
        self.ultra_scale = scale
