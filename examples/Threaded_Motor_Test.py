# This code is for testing the BrickPi with a Lego Motor 

from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import threading

BrickPiSetup()  # setup the serial port for communication
BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

#This thread is used for keeping the motors running
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while True:
            BrickPiUpdateValues()       # Ask BrickPi to update values for senso
            time.sleep(.1)              # sleep for 100 ms
thread1 = myThread(1, "Thread-1", 1)    # Setup and start the thread
thread1.setDaemon(True)
thread1.start()

# The main code below runs once the thread is set up.
while True:
    print "Running Forward"
    BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = 200  #Set the speed of MotorB (-255 to 255)
    time.sleep(3)                     # sleep for 3 s
    print "Running Reverse"
    BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = -200  #Set the speed of MotorB (-255 to 255)
    time.sleep(3)                      # sleep for 3 s