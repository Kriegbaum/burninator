import board
import busio
import adafruit_mcp9808
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import threading
import time
import os
import datetime
import gpiozero
from signal import pause

#LOOK INTO PID ALGORITHMS

#################GRAB LOCAL IP ADDRESS##########################################
ipSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    ipSock.connect(('10.255.255.255', 1))
    localIP = ipSock.getsockname()[0]
except:
    localIP = '127.0.0.1'
ipSock.close()
socket.setdefaulttimeout(1)

##################RELAY CONTROL OBJECT##########################################
relayPin = 'PUT PIN HERE'
relay = gpiozero.DigitalOutputDevice(relayPin)

##########################BUTTONS###############################################
up = gpiozero.Button(board.D3, bounce_time=0.2)
down = gpiozero.Button(board.D2, bounce_time=0.2)
left = gpiozero.Button(board.D10, bounce_time=0.2)
right = gpiozero.Button(board.D9, bounce_time=0.2)
select = gpiozero.Button(board.D8, bounce_time=0.2)
reset = gpiozero.Button(board.D7, bounce_time=0.2)


##############PHYSICAL DEVICES ATTACHED TO BOARD################################
lcd_columns = 16
lcd_rows = 2

i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808(i2c)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.color = [0,0,100]
lcd.message = 'Initializing\nBurninator...'



######################DATA COLLECTOR CONTROL OBJECTS############################
burnStart = 0
#Time in seconds that the furnace has been running today
burnTime = 0
#Use these two to calculate average daily set point
avgSetPoint = 0
avgSetPointIterator = 0
logFile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'burnLog.csv'), 'a+')

def writeData(self):
    data = (datetime.datetime.now(), self.avgSetPoint, self.burnTime)
    burnTime = 0
    avgSetPoint = 0
    avgSetPointIterator = 0
    logFile.write(data)

########################THERMOSTAT CONTROL OBJECTS##############################
#Poll this value to see whether or not the furnace should be engaged
burn = False
remoteSensors = False
#Poll this to check the home/away state
#Valid values, 'home', 'away', 'sleep'
state = 'away'
deadband = 3
currentTemp = mcp.temperature * 9 / 5 + 32

homeTemp = 69
awayTemp = 59
sleepTemp = 62
burnStart = False
setPoint = awayTemp

def burn():
    if burn:
        return True
    else:
        burn = True
        burnStart = datetime.datetime.now()
        relay.on()
def halt():
    if burn:
        burn = False
        burnTime += datetime.datetime.now() - burnStart
        relay.off()
    else:
        return False
def getTempLocal():
    return mcp.temperture * 9 / 5 + 32
def getTempGlobal():
    pass
def getTemp():
    if remoteSensors:
        return getTempGlobal()
    else:
        return getTempLocal()

##########################INTERFACE FUNCTIONS###################################
def plusMax(value, max):
    value += 1
    if value > max:
        value = max
    return value

def minusMin(value, min):
    value -= 1
    if value < min:
        value = min
    return value

class Interface:
    def __init__(self, timeout, ):
        self.page = 0
        self.pages = 4
        self.interfaceTimeout = threading.Timer(timeout, self.sleep)
        self.Awake = True

    def sleep(self):
        lcd.color = [0,0,0]
        self.awake = False

    def wake(self):
        lcd.color = [0,0,100]
        self.awake = True

    def bump(self):
        self.interfaceTimeout.cancel()
        self.interfaceTimeout.start()

    def nextPage(self):
        self.page += 1
        if self.page > self.pages - 1:
            self.page = 0
        lcd.clear()
        self.display()
        self.bump()

    def prevPage(self):
        self.page -= 1
        if self.page < 0:
            self.page = self.pages
        lcd.clear()
        self.display()
        self.bump()

    def increaseValue(self):
        if page == 0:
            setPoint = plusMax(setPoint, maxTemp)
            self.display()
            self.bump()
        elif page == 1:
            homeTemp = plusMax(homeTemp, maxTemp)
            self.display()
            self.bump()
        elif page == 2:
            awayTemp = plusMax(awayTemp, maxTemp)
            self.display()
            self.bump()
        elif page == 3:
            sleepTemp = pluxMax(sleepTemp, maxTemp)
            self.display()
            self.bump()
    def decreaseValue(self):
        if page == 0:
            setPoint = minusMin(setPoint, maxTemp)
            self.display()
            self.bump()
        elif page == 1:
            homeTemp = minusMin(homeTemp, maxTemp)
            self.display()
            self.bump()
        elif page == 2:
            awayTemp = minusMin(awayTemp, maxTemp)
            self.display()
            self.bump()
        elif page == 3:
            sleepTemp = minusMin(sleepTemp, maxTemp)
            self.display()
            self.bump()
    def display():
        if page == 0:
            lcd.message = "%s, %f F\nCurrent Set: %fF" % (state, currentTemp, setPoint)
        elif page == 1:
            lcd.message = "%s, %f F\nHome Temp: %fF" % (state, currentTemp, homeTemp)
        elif page == 2:
            lcd.message = "%s, %f F\nAway Temp: %fF" % (state, currentTemp, awayTemp)
        elif page == 3:
            lcd.message = "%s, %f F\nSleep Temp: %fF" % (state, currentTemp, sleepTemp)



##########################MAIN THREAD FUNCTIONS#################################
interface = Interface()

def interfaceThread():
    '''polls buttons for change in state, updates display output'''

    while True:
        up.when_pressed = interface.increaseValue
        down.when_pressed = interface.decreaseValue
        left.when_pressed = interface.prevPage
        right.when_pressed = interface.nextPage
        select.when_pressed = idontfuckinknow
        up.when_held = interface.increaseValue
        down.when_held = interface.decreaseValue
        pause()

def burninator():
    '''Main action thread for thermostat, regulates temperature and logs data'''
    while True:
        currentTemp = getTemp()
        if currentTemp < setPoint - deadband:
            burn()
        elif currentTemp > setPoint + deadband:
            halt()
        else:
            pass

def stateServer():
    '''listens for commands from other devices regarding set-point and home/away state'''
    pass
