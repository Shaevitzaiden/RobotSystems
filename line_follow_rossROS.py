import concurrent.futures
import sys, os
from unicodedata import name
from sensor import Sensor
from interpreter import Interpreter
from controller import Controller
from ultrasonic_interpreter import UltrasonicInterpreter
from ultrasonic_sensor import Ultrasonic
from picarx_improved import Picarx
from time import sleep
from readerwriterlock import rwlock

# directory = os.getcwd()
sys.path.append(r"/home/aiden/RobotSystems/rossROS")
from rossros import Bus, ConsumerProducer, Consumer, Producer, Timer


if __name__ == "__main__":
    sensor_bus = Bus(initial_message=[1,1,1],name="sensor bus")
    ultra_bus = Bus(name="ultra sensor bus")
    interp_bus = Bus(name="interpretor bus")
    ui_bus = Bus(name="ultra interp bus")
    termination_bus = Bus(name="termination bus")
    
    px = Picarx()
    s = Sensor()
    i = Interpreter(polarity=-1)
    u = Ultrasonic()
    ui = UltrasonicInterpreter()
    c = Controller(px, scaling_factor=14)
    
    timer = Timer(termination_bus, 3, 0.01,termination_bus)
    s_producer = Producer(s, output_busses=sensor_bus, delay=0.05, termination_busses=termination_bus, name="sensor producer")
    i_cp = ConsumerProducer(i, input_busses=sensor_bus, output_busses=interp_bus,delay=0.05, termination_busses=termination_bus, name="interpretor consumer-producer")
    c_consumer = Consumer(c, input_busses=[interp_bus, ui_bus], delay=0.05, termination_busses=termination_bus, name="controller consumer")
    u_producer = Producer(u, output_busses=ultra_bus, delay=0.05, termination_busses=termination_bus, name="ultra producer")
    ui_cp = ConsumerProducer(ui, input_busses=ultra_bus, delay=0.5, termination_bus=termination_bus, name="ultra interpreter")

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        eSensor = executor.submit(s_producer)
        eInterpreter = executor.submit(i_cp)
        eUltraSensor = executor.submit(u_producer)
        eUltraInterpreter = executor.submit(ui_cp)
        sleep(0.1)
        eController = executor.submit(c_consumer)
        eTimer = executor.submit(timer)

    eSensor.result()
    eInterpreter.result()
    eController.result()
    eTimer.result()
    eUltraSensor.result()
    eUltraInterpreter.result()

