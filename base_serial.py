import serial
import struct
import time
import threading
from threading import Timer

DEFAULT_SERIAL_PATH = "/dev/tty.wchusbserial1420"
DEFAULT_BAUD_RATE = 9600


class Servo:

    def __init__(self, path=DEFAULT_SERIAL_PATH, baud_rate=DEFAULT_BAUD_RATE):
        self.path = path
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.path, self.baud_rate, timeout=1)
        self.last_run_time = 0
        self.last_time = time.time()
        #header length command count time (id angle) * 6
        #  2      1       1      1     2    1   2

    def wait_and_move(self, t, value):
        if t is None or value is None:
            return
        if self.last_time + self.last_run_time < time.time():
            self._move(t, value)
        else:
            interval = self.last_time + self.last_run_time - time.time()
            if interval <= 0:
                self._move(t, value)
            else:
                Timer(interval/1000, self._move, (t, value)).start()
        self.last_time += t
        self.last_run_time = t

    def _move(self, time, value):
        print(threading.current_thread())
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
    s.wait_and_move(2000, {2:500})
    s.wait_and_move(2000, {2:2500})
    s.wait_and_move(2000, {2:500})
    s.wait_and_move(2000, {1:500})
    s.wait_and_move(2000, {1:1500})
    s.wait_and_move(2000, {1:500})
    s.wait_and_move(2000, {3:500, 4:2500})
    s.wait_and_move(2000, {3:1500, 4:1500})
    s.wait_and_move(2000, {3:2500, 4:500})
    print("end")