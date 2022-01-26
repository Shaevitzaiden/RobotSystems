class Consumer():
    def __init__(self) -> None:
        pass

    def consume(func, bus_in):
        val = bus_in.read()
        func(val) 




class ConsumerProducer():
    def __init__(self):
        super().__init__()
        pass