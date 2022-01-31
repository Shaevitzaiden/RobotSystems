import concurrent.futures
import sys, os
from sensor import Sensor
from interpreter import Interpreter
from controller import Controller
from picarx_improved import Picarx
from time import sleep
from readerwriterlock import rwlock

# directory = os.getcwd()
sys.path.append(r"/home/aiden/RobotSystems/rossROS")
from rossros import Bus, ConsumerProducer, Consumer, Producer, Timer


if __name__ == "__main__":
    sensor_bus = Bus(initial_message=[1,1,1],name="sensor bus")
    interp_bus = Bus(name="interpretor bus")
    termination_bus = Bus(name="termination bus")
    
    px = Picarx()
    s = Sensor()
    i = Interpreter(polarity=-1)
    c = Controller(px, scaling_factor=14)
    
    
    # timer = Timer(termination_bus, 3, 0.01,termination_bus)
    # s_producer = Producer(s.get_grayscale_data, output_busses=sensor_bus, delay=0.05, termination_busses=termination_bus, name="sensor producer")
    # i_cp = ConsumerProducer(i.get_edge_relation, input_busses=sensor_bus, output_busses=interp_bus,delay=0.05, termination_busses=termination_bus, name="interpretor consumer-producer")
    # c_consumer = Consumer(c.follow_line, input_busses=interp_bus, delay=0.05, termination_busses=termination_bus, name="controller consumer")

    timer = Timer(termination_bus, 3, 0.01,termination_bus)
    s_producer = Producer(s, output_busses=sensor_bus, delay=0.05, termination_busses=termination_bus, name="sensor producer")
    i_cp = ConsumerProducer(i, input_busses=sensor_bus, output_busses=interp_bus,delay=0.05, termination_busses=termination_bus, name="interpretor consumer-producer")
    c_consumer = Consumer(c, input_busses=interp_bus, delay=0.05, termination_busses=termination_bus, name="controller consumer")



    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        eSensor = executor.submit(s_producer)
        eInterpreter = executor.submit(i_cp)
        eController = executor.submit(c_consumer)
        eTimer = executor.submit(timer)

    eSensor.result()
    eInterpreter.result()
    eController.result()
    eTimer.result()
    
    # follow_line(s, i, c)
