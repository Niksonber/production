import serial
import time
from queue import Queue
from threading import Thread, Lock


class GcodeSender():
    def __init__(self, port = '/dev/ttyACM0', baudrate=250000, fileName='3DBenchy.gcode'):
        #self.queue = queue
        self.port = port
        self.baudrate = baudrate
        self.fileName = fileName
        self.stop = False
        self.error = None
    
    def run(self):
        self.thread = Thread(target=self.__loop__)
        self.thread.start()

    def __loop__(self):
        self.sendGcode()

    def removeComment(self, string, char):
        indx = string.find(char)
        if indx == -1:
            return string
        return string[:indx]

    def findString(self, string, code):
        if (string.find(code)==-1):
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
                initial = True
                for line in f:  
                    if self.stop or self.error!= None:
                        break
                    l = self.removeComment(line, ';')
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
                        while not self.findString(out,b'ok') \
                               and not self.stop:
                            if self.findString(out,b'Error'):
                                self.error = out.decode()
                                break
                            # read gcode line or give a timeout
                            out = s.readline()
                            if out != b'' :
                                print(out)
                            if time.time()-t > .5 and initial:
                                initial = False
                                break
                            time.sleep(.1)
                        time.sleep(.1)
        print('fim')

if __name__ == '__main__':
    port = '/dev/ttyACM0'
    baudrate = 250000
    g1 = GcodeSender(port, baudrate, '3DBenchy.gcode')
    #g2 = GcodeSender('/dev/ttyACM1', baudrate, '3DBenchy2.gcode')  
    g1.run()
    #g2.run()