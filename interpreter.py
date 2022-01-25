from re import L
import numpy as np
import time


class Interpreter():
    def __init__(self, sensitivity=0, polarity=1):
        self.sensitivity = sensitivity
        self.polarity = polarity

    def get_edge_relation(self, adc_vals):
        adc_vals_norm = [float(i)/max(adc_vals) for i in adc_vals]
        adc_vals_diff = max(adc_vals_norm)-min(adc_vals_norm)
        if adc_vals_diff > self.sensitivity:
            rel_dir = adc_vals_norm[0]-adc_vals_norm[2]
            print("Relative Direction: "+str(rel_dir))
            if self.polarity == 1:
                error = (max(adc_vals_norm)-np.mean(adc_vals_norm))/0.7
            elif self.polarity == -1:
                error = (min(adc_vals_norm)-np.mean(adc_vals_norm))/0.7
            print("Error: "+str(error))
            rel_dir_pol = rel_dir*error*self.polarity
        else:
            rel_dir_pol = 0
            print('straight')
        return rel_dir_pol

    def bus_consume_produce(self, bus_in, bus_out, delay):
        bus_out.write(self.get_edge_relation(bus_in.read()))
        time.sleep(delay)
