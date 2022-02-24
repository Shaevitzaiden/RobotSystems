#!/usr/bin/python3
# coding=utf8
import sys
from Perception import Perception
from Motion import Motion

sys.path.append('/home/aiden/RobotSystems/rossROS/')
from rossros import Bus, ConsumerProducer, Consumer, Producer, Timer, runConcurrently

if __name__ == "__main__":
    perception_bus = Bus(initial_message={}, name="perception bus")

    p = Perception()
    m = Motion()

    p_producer = Producer(p, output_busses=perception_bus, delay=0.1, name="block position producer")
    m_consumer = Consumer(m.stack, input_busses=perception_bus, delay=0.05, name="motion controller consumer")

    prod_cons_list = [p_producer, m_consumer]
    runConcurrently(prod_cons_list)
