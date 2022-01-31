from adc import ADC
from time import sleep
import logging
from logdecorator import log_on_end, log_on_error, log_on_start

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)

class Sensor(object):
    def __init__(self):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")

    def __call__(self):
        return self.get_grayscale_data
        
    # @log_on_start(logging.DEBUG, "Sensor method started")
    # @log_on_start(logging.DEBUG, "Sensor method finished")
    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

    # def bus_produce(self, bus, delay):
    #     while True:
    #         sensor_val = self.get_grayscale_data()
    #         bus.write(sensor_val)
    #         sleep(delay)

# if __name__ == "__main__":
#     import time
#     GM = Grayscale_Module(950)
#     while True:
#         print(GM.get_grayscale_data())
#         time.sleep(1)
