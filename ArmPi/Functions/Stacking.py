#!/usr/bin/python3
# coding=utf8
import sys, os
from Perception import Perception
from Motion import Motion
from time import sleep
import concurrent.futures

sys.path.insert(0,"/home/aiden/RobotSystems/rossROS")
from rossros import Bus, ConsumerProducer, Consumer, Producer, Timer, runConcurrently


if __name__ == "__main__":
    perception_bus = Bus(initial_message={}, name="perception bus")

    p = Perception()
    m = Motion()

    p_producer = Producer(p, output_busses=perception_bus, delay=0.05, name="block position producer")
    m_consumer = Consumer(m.stack, input_busses=perception_bus, delay=0.1, name="motion controller consumer")

    # prod_cons_list = [p_producer, m_consumer]
    # runConcurrently(prod_cons_list)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        e_p = executor.submit(p_producer)
        sleep(0.5)
        e_m = executor.submit(m_consumer)
        
    e_p.result()
    e_m.result()
