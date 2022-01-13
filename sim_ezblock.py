import logging
import math
import time

# logging_format = "%( asctime )s: %( message )s"
# logging.basicConfig(format=logging_format, level=logging.INFO, datefmt ="% H:%M:%S")
# logging.getLogger().setLevel(logging.DEBUG )

##############################################################################################
class Servo(object):
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50
    def __init__(self, pwm):
        super().__init__()
        self.pwm = pwm
        # self.angle = 0

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        if angle < -90:
            angle = -90
        if angle > 90:
            angle = 90
        # self.angle = angle
        return angle
##############################################################################################

##############################################################################################
timer = [{"arr": 0}] * 4
class PWM():
    def __init__(self, channel, debug="critical"):
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError("PWM channel should be between [P1, P14], not {0}".format(channel))
        self.timer = int(channel/4)
        self._pulse_width = 0

    def prescaler(self, *prescaler):
        if len(prescaler) == 0:
            return self._prescaler
        else:
            self._prescaler = int(prescaler[0]) - 1


    def period(self, *arr):
        global timer
        if len(arr) == 0:
            return timer[self.timer]["arr"]
        else:
            timer[self.timer]["arr"] = int(arr[0]) - 1

    def pulse_width(self, *pulse_width):
        if len(pulse_width) == 0:
            return self._pulse_width
        else:
            self._pulse_width = int(pulse_width[0])
            # reg = self.REG_CHN + self.channel
            # self.i2c_write(reg, self._pulse_width)

    def pulse_width_percent(self, *pulse_width_percent):
        global timer
        if len(pulse_width_percent) == 0:
            return self._pulse_width_percent
        else:
            self._pulse_width_percent = pulse_width_percent[0]
            temp = self._pulse_width_percent / 100.0
            # print(temp)
            pulse_width = temp * timer[self.timer]["arr"]
            self.pulse_width(pulse_width)
##############################################################################################

##############################################################################################
class Pin(object):
    def __init__(self, *value):
        super().__init__()
        pass

    def value(self, *value):
        if len(value) == 0:
            result = 1
            return result
        else:
            value = value[0]
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()
##############################################################################################

##############################################################################################
class ADC():
    ADDR=0x14                   # The address of the expansion board is 0x14
    def __init__(self, chn):    # Parameters, number of channels, there are 8 adc channels on the Raspberry Pi expansion board: 
                                # "A0, A1, A2, A3, A4, A5, A6, A7"
        super().__init__()
        pass
        
    def read(self):
        value = 1       # The number of adc channel read --- write data once, read data twice (the range of read data is 0~4095)
        return value

    def read_voltage(self):   # Convert the read data into voltage values（0~3.3V）
        read = 1
        return read*3.3/4095
##############################################################################################

##############################################################################################
class fileDB(object):
    """A file based database.
    A file based database, read and write arguments in the specific file.
    """
    def __init__(self, db=None):
        # '''Init the db_file is a file to save the datas.'''
		# Check if db_file is defined
        if db != None:
            self.db = db
        else:
            self.db = "config"

    def get(self, name, default_value=None):
        """Get value by data's name. Default value is for the arguemants do not exist"""
        return default_value
##############################################################################################