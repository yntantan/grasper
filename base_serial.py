import serial
import struct

DEFAULT_SERIAL_PATH = "/dev/tty.wchusbserial1420"
DEFAULT_BAUD_RATE = 9600


class Servo:

    def __init__(self, path=DEFAULT_SERIAL_PATH, baud_rate=DEFAULT_BAUD_RATE):
        self.path = path
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.path, self.baud_rate, timeout=1)
        #header length command count time (id angle) * 6
        #  2      1       1      1     2    1   2

    def move(self, time, value):
        if time is None or value is None:
            return
        count = len(value)
        s = struct.Struct("=HBBBH" + "BH" * count)
        header = [21845, count*3+5, 3, count, time]
        for kv in value.items():
            header.extend(kv)
        bs = s.pack(*header)
        print("execute:" + str(bs))
        self.ser.write(bs)

    def __del__(self):
        self.ser.close()


if __name__ == '__main__':
    s = Servo()
    s.move(2000, {1:500,2:500})
    # s.move(1000, {2:2500})
    # s.move(1000, {2:1000})
    # s.move(500, {1:1500})
    # s.move(500, {1:500})
    # s.move(500, {1:1500})