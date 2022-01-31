from time import sleep

class Consumer():
    def __init__(self) -> None:
        pass

    @staticmethod
    def consume(func, bus_in, delay):
        while True:
            val = bus_in.read()
            func(val)
            sleep(delay)


class Producer():
    def __init__(self) -> None:
        pass

    @staticmethod
    def produce(func, bus_out, delay):
        while True:
            message = func()
            bus_out.write(message)
            sleep(delay)


class ConsumerProducer():
    def __init__(self):
        pass

    @staticmethod
    def consume_produce(func, bus_in, bus_out, delay):
        while True:
            message_in = bus_in.read()
            val = func(message_in)
            bus_out.write(val)
            sleep(delay)
