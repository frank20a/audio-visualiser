from serial import Serial
from Dialogs import SerialConnDialog
from Exceptions import ConnectionInterrupted

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


class Shredder(Connection):
    type = "Shredder"

    def transmit(self, data):
        pass

    def setup(self):
        pass


class ConsoleConn(Connection):
    type = "Console"

    def transmit(self, data):
        print(self.process(data))

    def setup(self):
        pass


class SerialConn(Connection):
    type = "Serial"

    def transmit(self, data):
        for i in self.process(data):
            self.ser.write(i)
        # if self.ser.read().decode() != '#': raise(ConnectionInterrupted)

    def setup(self):
        import serial.tools.list_ports

        try:
            resp = SerialConnDialog(self.parent, serial.tools.list_ports.comports()).show()
            self.ser = Serial(resp[0], int(resp[1]))
            print(self.ser.readline().decode())
        except IndexError: print("Closed unexpectedly")
        except Exception as e: print(e)


class NetworkConn(Connection):
    type = "Network"


if __name__ == "__main__":
    A = SerialConn(None)