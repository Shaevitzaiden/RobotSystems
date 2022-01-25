import concurrent.futures
from bus import Bus
from sensor import Sensor
from interpreter import Interpreter
from controller import Controller
from picarx_improved import Picarx
from time import sleep
from readerwriterlock import rwlock


def follow_line(sensor, interpretor, controller):
    while True:
        adc_data = sensor.get_grayscale_data()
        val = interpretor.get_edge_relation(adc_data)
        controller.follow_line(val)


if __name__ == "__main__":
    sensor_bus = Bus()
    interp_bus = Bus()
    
    px = Picarx()
    s = Sensor()
    i = Interpreter(polarity=-1)
    c = Controller(px, scaling_factor=14)
    
    sensor_delay = 1
    interp_delay = 1
    control_delay = 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(s.bus_produce, sensor_bus, sensor_delay)
        eInterpreter = executor.submit(i.bus_consume_produce, sensor_bus, interp_bus, interp_delay)
        eController = executor.submit(c.bus_consume, interp_bus, control_delay)

    eSensor.result()
    eInterpreter.result()
    eController.result()
    
    # follow_line(s, i, c)
