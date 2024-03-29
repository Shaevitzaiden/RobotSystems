import concurrent.futures
from picarx_improved import Picarx
from bus import Bus
from consumer_producer import Consumer, Producer, ConsumerProducer
from sensor import Sensor
from interpreter import Interpreter
from controller import Controller
from time import sleep
from readerwriterlock import rwlock


if __name__ == "__main__":
    sensor_bus = Bus()
    interp_bus = Bus()
    
    px = Picarx()
    s = Sensor()
    i = Interpreter(polarity=-1)
    c = Controller(px, scaling_factor=14)

    s_producer = Producer()
    i_cp = ConsumerProducer()
    c_consumer = Consumer()

        
    sensor_delay = 0.01
    interp_delay = 0.01
    control_delay = 0.01
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(s_producer.produce, s.get_grayscale_data, sensor_bus, sensor_delay)
        eInterpreter = executor.submit(i_cp.consume_produce, i.get_edge_relation, sensor_bus, interp_bus, interp_delay)
        sleep(0.1)
        eController = executor.submit(c_consumer.consume, c.follow_line, interp_bus, control_delay)

    eSensor.result()
    eInterpreter.result()
    eController.result()
    
    # follow_line(s, i, c)
