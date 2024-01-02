
from rutinas.AccesoLPR.rutAccesoLPR import *


import os,signal
RUN = True
def receiveSignal(signalNumber, frame):
        print("HBL STOPPED")
        exit()
        global RUN
        RUN = False
def pid(): 
    pid = os.getpid()
    print("HBL THREAD NUMBER",pid)
        
    with open("stop.sh","w") as f:
        f.write(f"sudo kill -9 {pid}")

if __name__ =="__main__":
    
    
    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)
    
    pid()
    
    rutinaAccesoLPR()