import board
import busio
import adafruit_mcp9808
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import threading
import time

##############PHYSICAL DEVICES ATTACHED TO BOARD################################
lcd_columns = 16
lcd_rows = 2

i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808(i2c)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.color = [0,0,100]
lcd.message = 'Initializing\nBurninator...'


##################CONTROL OBJECTS###############################################
class Burninator:
    def __init__(self, home, away, sleep):
        #Poll this value to see whether or not the furnace should be engaged
        self.burn = False
        #Poll this to check home/away state
        self.state = 'away'
        #Various temperature setpoints and readings
        self.currentTemp = False
        self.homeTemp = home
        self.awayTemp = away
        self.sleepTemp = sleep

########################DATA GATHERING OBJECTS##################################
class DataCollector:
    def __init__(self):
        #Time in seconds that the furnace has been running today
        self.burnTime = 0
        #Use these two to calculate average daily set point
        self.avgSetPoint = 0
        self.avgSetPointIterator = 0


##########################INTERFACE FUNCTIONS###################################
class Interface:
    def __init__(self, timeout, ):
        self.page = 0
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





##########################MAIN THREAD FUNCTIONS#################################

def interfaceThread():
    '''polls buttons for change in state, updates display output'''
    pass

def burninator():
    '''Main action thread for thermostat, regulates temperature and logs data'''
    pass

def stateGetServer():
    '''listens for commands from other devices regarding set-point and home/away state'''
    pass

print(mcp.temperature * 9 / 5 + 32)
