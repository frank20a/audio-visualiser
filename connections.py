

class Connection:
    type = "None"

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.setup(*args, **kwargs)

    def transmit(self, data):
        raise NotImplementedError

    def setup(self, *args, **kwargs):
        raise NotImplementedError

    def process(self, data):
        res = []
        iter = self.parent.ledList.root
        while iter is not None:
            res.append(data[iter.pos[0]][iter.pos[1]])
            iter = iter.child
        return res


class ConsoleConn(Connection):
    type = "Console"

    def transmit(self, data):
        print(self.process(data))

    def setup(self):
        pass
