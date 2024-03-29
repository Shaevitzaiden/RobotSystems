from sensor import Sensor
from interpreter import Interpreter
from controller import Controller
from picarx_improved import Picarx
from time import sleep

def follow_line(sensor, interpretor, controller):
    go = 1
    while go == 1:
        adc_data = sensor.get_grayscale_data()
        val = interpretor.get_edge_relation(adc_data)
        controller.follow_line(val)

if __name__ == "__main__":
    px = Picarx()
    s = Sensor()
    i = Interpreter(polarity=-1)
    c = Controller(px, scaling_factor=14)

    follow_line(s, i, c)
