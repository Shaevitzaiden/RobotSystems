from re import L
import numpy as np
import time

import logging
from logdecorator import log_on_end, log_on_error, log_on_start

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)


class UltrasonicInterpreter():
    def __init__(self, slow_factor=2):
        self.slow_factor = slow_factor

    def __call__(self, sens_dist):
        return self.stop_or_not(sens_dist)

    @log_on_start(logging.DEBUG, "Ultrasonic Intepreter method started")
    @log_on_error(logging.DEBUG, "Ultrasonic method error")
    @log_on_end(logging.DEBUG, "Ultrasonic method finished")
    def stop_or_not(self, sens_dist):
        return np.tanh(sens_dist/self.slow_factor)

