try:
    import RPi.GPIO as GPIO
    import smbus
except ImportError:
    pass

import time
import queue

class PCF8574_I2C(object):
	OUPUT = 0
	INPUT = 1
	
	def __init__(self,address):
		# Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
		self.bus = smbus.SMBus(1)
		self.address = address
		self.currentValue = 0
		self.writeByte(0)	#I2C test.
		
	def readByte(self):#Read PCF8574 all port of the data
		#value = self.bus.read_byte(self.address)
		return self.currentValue#value
		
	def writeByte(self,value):#Write data to PCF8574 port
		self.currentValue = value
		self.bus.write_byte(self.address,value)

	def digitalRead(self,pin):#Read PCF8574 one port of the data
		value = self.readByte()	
		return (value&(1<<pin)==(1<<pin)) and 1 or 0
		
	def digitalWrite(self,pin,newvalue):#Write data to PCF8574 one port
		value = self.currentValue #bus.read_byte(address)
		if(newvalue == 1):
			value |= (1<<pin)
		elif (newvalue == 0):
			value &= ~(1<<pin)
		self.writeByte(value)	

class PCF8574_GPIO(object):#Standardization function interface
	OUT = 0
	IN = 1
	BCM = 0
	BOARD = 0
	def __init__(self,address):
		self.chip = PCF8574_I2C(address)
		self.address = address
	def setmode(self,mode):#PCF8574 port belongs to two-way IO, do not need to set the input and output model
		pass
	def setup(self,pin,mode):
		pass
	def input(self,pin):#Read PCF8574 one port of the data
		return self.chip.digitalRead(pin)
	def output(self,pin,value):#Write data to PCF8574 one port
		self.chip.digitalWrite(pin,value)
            
class LCD:
    """
    Hardware wrapper for an LCD connected via PCF8574
    """
    def __init__(self, i2c_address):
        self.pcf = PCF8574_GPIO(i2c_address)

    def display_value(self, value: str):
        """
        For simplicity, write raw bits of value to PCF8574 pins
        """
        value_int = int(value) if value.isdigit() else 0
        for pin in range(8):
            self.pcf.output(pin, (value_int >> pin) & 1)
            
    def cleanup(self):
        pass  # PCF8574 doesn't need GPIO.cleanup

def run_lcd_loop(name, lcd, stop_event, lcd_queue, callback=None):
    while not stop_event.is_set():
        try:
            value = lcd_queue.get(timeout=0.5)
            value_str = str(value).rjust(4)
            if callback:
                callback(name, value_str)
            lcd.display_value(value_str)
        except queue.Empty:
            pass
        time.sleep(0.1)
