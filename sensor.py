from adc import ADC
from time import sleep

class Sensor(object):
    def __init__(self):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")

    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

    def bus_produce(self, bus, delay):
        while True:
            bus.write(self.get_graysscale_data())
            sleep(delay)

# if __name__ == "__main__":
#     import time
#     GM = Grayscale_Module(950)
#     while True:
#         print(GM.get_grayscale_data())
#         time.sleep(1)
