from serial import Serial
import socket
from Dialogs import SerialConnDialog, NetworkConnDialog
from Exceptions import ConnectionInterrupted, ConnectionNotACKed
from time import sleep

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
            res.append(tuple(map(self.brightness_limit, data[iter.pos[0]][iter.pos[1]])))
            iter = iter.child
        return res

    def brightness_limit(self, n):
        return min(254, int(n * self.parent.sidebar.brightness.get() / 100))


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
        self.ser.write(bytearray([255]))        # Send new frame byte
        for i in self.process(data):
            self.ser.write(bytearray(i))        # Limit max data byte to 254 to implement new-frame byte
        # if self.ser.read().decode() != '#': raise(ConnectionInterrupted)

    def setup(self):
        import serial.tools.list_ports

        try:
            resp = SerialConnDialog(self.parent, serial.tools.list_ports.comports()).show()
            self.ser = Serial(resp[0], int(resp[1]))
            print(self.ser.readline().decode())
        except IndexError: print("Closed unexpectedly")
        except Exception as e: print(e)


class NetworkTCPConn(Connection):
    type = "Network-TCP"

    def transmit(self, data):
        try:
            self.socket.send(bytearray([255]))              # Make new frame handshake
            for i in self.process(data):
                self.socket.sendall(bytearray(i))       # Transmit data

        except (ConnectionAbortedError, OSError) as e:
            self.socket.close()
            self.socket = None
            print(e)
            self.parent.connect()
        except ConnectionNotACKed:
            print("Missed frame")

    def setup(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            resp = NetworkConnDialog(self.parent).show()
            self.socket.connect((str(resp[0]), int(resp[1])))

            # Get connection ACK
            ack = self.socket.recv(1024).decode()
            if ack != self.socket.getsockname()[0] + " ACK": raise ConnectionNotACKed(ack)
            else: print("Connected")
        except TimeoutError:
            print("Connection Timed Out")
        except ConnectionRefusedError:
            print("Connection was actively refused (Blocked port or server not running")
        except ConnectionNotACKed as e:
            print("Server responded with wrong ACK signal", end=' ')
            print(e)
            self.socket.close()


class NetworkUDPConn(Connection):
    type = "Network-UDP"

    def transmit(self, data):
        try:
            self.socket.sendto(bytearray([i for sub in self.process(data) for i in sub]), self.server)
        except (ConnectionAbortedError, OSError) as e:
            self.socket.close()
            self.socket = None
            print(e)
            self.parent.connect()

    def setup(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            resp = NetworkConnDialog(self.parent).show()
            self.server = (str(resp[0]), int(resp[1]))

            # Get connection ACK
            # ack = self.socket.recvfrom(1024)
            # if ack[0] != "ACK" or ack[1] != self.server[0]: raise ConnectionNotACKed
        except TimeoutError:
            print("Connection Timed Out")
        except ConnectionRefusedError:
            print("Connection was actively refused (Blocked port or server not running")
        except ConnectionNotACKed as e:
            print("Server responded with wrong ACK signal", end=' ')
            print(e)
            self.socket.close()


if __name__ == "__main__":
    A = NetworkTCPConn()