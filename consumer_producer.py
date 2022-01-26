from time import sleep

class Consumer():
    def __init__(self) -> None:
        pass

    def consume(func, bus_in, delay, out=False, loop=True):
        while loop:
            val = bus_in.read()
            # If value on bus is to be processed and posted elsewhere
            if out:
                return func(val)
            # No message is return, simply run the function
            else:
                func(val)
                sleep(delay)


class Producer():
    def __init__(self) -> None:
        pass

    def produce(func, bus_out, message, delay, loop=True):
        while loop:
            bus_out.write(message)
            sleep(delay)


class ConsumerProducer(Consumer, Producer):
    def __init__(self):
        super().__init__()
        pass

    def consume_produce(self, func, bus_in, bus_out, delay):
        while True:
            val = self.consume(func, bus_in, 0, out=True, loop=False)
            self.produce(bus_out, val, 0, loop=False)
            sleep(delay)