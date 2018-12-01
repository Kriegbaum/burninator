import board
import busio
import adafruit_mcp9808

##############PHYSICAL DEVICES ATTACHED TO BOARD################################
i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808(i2c_bus)

##################CONTROL OBJECTS###############################################
#Poll this value to see whether or not the furnace should be engaged
burn = False
#Poll this to check home/away state
occupied = False

#Various temperature setpoints and readings
currentTemp = False
homeTemp = 69 #Nice
awayTemp = 64

########################DATA GATHERING OBJECTS##################################
#Time in seconds that the furnace has been running today
burnTime = 0
#Use these two to calculate average daily set point
avgSetPoint = 0
avgSetPointIterator = 0

##########################MAIN THREAD FUNCTIONS#################################

def inputThread():
    '''polls buttons for change in state'''
    pass

def burninator():
    '''Main action thread for thermostat, regulates temperature and logs data'''
    pass

def stateGetServer():
    '''listens for commands from other devices regarding set-point and home/away state'''
    pass

print(mcp.temperature * 9 / 5 + 32)
