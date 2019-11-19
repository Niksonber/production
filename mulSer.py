import serial
import time
from queue import Queue
from threading import Thread


class GcodeSender(Thread):
    def __init__(self, port = '/dev/ttyACM0', baudrate=250000, fileName='3DBenchy.gcode'):
        #self.queue = queue
        self.port = port
        self.baudrate = baudrate
        self.fileName = fileName
    
    def run(self):
        self.thread = Thread(target=self.__loop__)
        self.thread.start()

    def __loop__(self):
        self.sendGcode()

    def removeComment(self, string):
        indx = string.find(';')
        if indx == -1:
            return string
        return string[:indx]

    def findOK(self, string):
        if (string.find(b'ok')==-1):
            return False
        return True

    def sendGcode(self):    
        with open(self.fileName,'r') as f:
            with serial.Serial(self.port, baudrate=self.baudrate, timeout=0.1) as s:
                time.sleep(1)
                s.flushInput()
                #set auto-temperature report every 1s
                print(b'M155 S1\n')
                s.write(b'M155 S1\n')
                for line in f:  
                    l = self.removeComment(line)
                    l = l.strip()
                    if  (l.isspace()==False and len(l)>0) :
                        l = l + '\n'
                        print(l)
                        # write gcode line
                        s.write(l.encode())
                        # read gcode line or give a timeout
                        out = s.readline() 
                        if out != b'' :
                            print(out)
                        t = time.time()
                        # read until not find 'ok'
                        while not self.findOK(out):
                            # read gcode line or give a timeout
                            out = s.readline()
                            if out != b'' :
                                print(out)
                            if t-time.time() > .5:
                                break

if __name__ == '__main__':
    port = '/dev/ttyACM0'
    baudrate = 250000
    g1 = GcodeSender(port, baudrate, '3DBenchy.gcode')
    g2 = GcodeSender('/dev/ttyACM1', baudrate, '3DBenchy2.gcode')  
    g1.run()
    g2.run()