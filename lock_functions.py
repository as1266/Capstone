import serial
import time
import io

class Lock:
    def __init__(self, locker_id):
        self.locker_id = locker_id
        
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',\
            baudrate=38400,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=1)
                
    def open_locker(self):
        if not self.ser.is_open:
            self.ser.open()
        prefix = 'open'
        suffix ='\r'
        command = prefix + str(self.locker_id) + suffix
        self.ser.write(bytes(command, 'utf8'))
        time.sleep(.3)
        self.ser.close()

    def close_locker(self):
        if not self.ser.is_open:
            self.ser.open()
        prefix = 'close'
        suffix ='\r'
        command = prefix + str(self.locker_id) + suffix
        self.ser.write(bytes(command, 'utf8'))
        time.sleep(.3)
        self.ser.close()

    def is_locker_open(self):
        locker_is_open = None
        if not self.ser.is_open:
            self.ser.open()
        prefix = 'status'
        suffix ='\r'
        statuscommand = prefix + str(self.locker_id) + suffix
        self.ser.write(bytes(statuscommand, 'utf8'))

        readlist = [""]
        while True:
            line = self.ser.readline();
            if line:
                readlist.append(line)
            else:
                break
        self.ser.close()

        for x in readlist:
            if "open" in str(x):
                locker_is_open = True
            if "close" in str(x):
                locker_is_open = False
                
        return locker_is_open
