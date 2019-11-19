import serial
import time

def removeComment(string):
    indx = string.find(';')
    if indx == -1:
        return string
    return string[:indx]

def findOK(string):
    if (string.find(b'ok')==-1):
        return False
    return True

def sendGcode(fileName, port, baudrate):    
    with open(fileName,'r') as f:
        with serial.Serial(port, baudrate=baudrate, timeout=0.1) as s:
            time.sleep(1)
            s.flushInput()
            #set auto-temperature report every 1s
            print(b'M155 S1\n')
            s.write(b'M155 S1\n')
            for line in f:  
                l = removeComment(line)
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
                    while not findOK(out):
                        # read gcode line or give a timeout
                        out = s.readline()
                        if out != b'' :
                            print(out)
                        if t-time.time() > .5:
                            break

if __name__ == '__main__':
    port = '/dev/ttyACM0'
    baudrate = 250000
    sendGcode('3DBenchy.gcode', port, baudrate)