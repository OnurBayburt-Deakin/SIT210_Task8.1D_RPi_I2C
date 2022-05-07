#Import modules
import smbus
import time

#Initialise variables
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

#Configure measurement modes
CONTINUOUS_LOW_RES_MODE = 0x13  # Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_HIGH_RES_MODE_1 = 0x10  # Start measurement at 1lx resolution. Time typically 120ms.
CONTINUOUS_HIGH_RES_MODE_2 = 0x11  # Start measurement at 0.5lx resolution. Time typically 120ms.
ONE_TIME_HIGH_RES_MODE_1 = 0x20  # Start measurement at 1lx resolution. Time typically 120ms. Powers down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21  # Start measurement at 0.5lx resolution. Time typically 120ms. Powers down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23  # Start measurement at 1lx resolution. Time typically 120ms. Powers down after measurement.
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#Read data from the I2C interface
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

#Convert data to numeral values
def convertToNumber(data):
  result = (data[1] + (256 * data[0])) / 1.2
  return result

#Main loop
if __name__ == "__main__":
  while True:
    lightLevel = readLight()
    lightLevel = int(lightLevel)
    
    if lightLevel > 400:  #Print messages based on brightness thresholds
        print("Too bright.")
        print("Light Level: " + format(lightLevel,'.2f') + "lx")
    elif lightLevel > 200 and lightLevel <= 400:
        print("Bright.")
        print("Light Level: " + format(lightLevel,'.2f') + "lx")
    elif lightLevel > 100 and lightLevel <= 200:
        print("Medium.")
        print("Light Level: " + format(lightLevel,'.2f') + "lx")
    elif lightLevel > 30 and lightLevel <= 100:
        print("Dark.")
        print("Light Level: " + format(lightLevel,'.2f') + "lx")
    elif lightLevel <= 30:
        print("Too dark.")
        print("Light Level: " + format(lightLevel,'.2f') + "lx")
        
    time.sleep(0.5)  #Measurement frequency
