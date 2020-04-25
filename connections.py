class Connection:
    type = "None"

    def __init__(self, *args, **kwargs):
        self.setup(*args, **kwargs)

    def transmit(self, data):
        raise NotImplementedError

    def setup(self, *args, **kwargs):
        raise NotImplementedError


class ConsoleConn(Connection):
    type = "Console"

    def transmit(self, data):
        print(data)

    def setup(self):
        pass
