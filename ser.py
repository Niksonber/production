import serial
import time

def removeComment(string):
    if (string.find(';')==-1):
        return string
    return string[:string.index(';')]

def findOK(string):
    if (string.find('ok')==-1):
        return False
    return True
    
with open(args.file,'r') as f:
    with serial.Serial('/dev/ttyACM0', baudrate=250000, timeout=0.01) as s:
        time.sleep(1)
        s.flushInput()
        for line in f:
            l = removeComment(line)
            l = l.strip() # Strip all EOL characters for streaming
            if  (l.isspace()==False and len(l)>0) :
                s.write(l + '\n') # Send g-code block
                out = s.readline() # Wait for response with carriage return
                print(out)
                while not findOK(out):
                    out = s.readline() # Wait for response with carriage return
                    print(out)