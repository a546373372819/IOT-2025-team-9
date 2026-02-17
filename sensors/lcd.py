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
    # Standard I2C Backpack Pin Mapping
    MASK_RS = 0x01  # P0 - Register Select
    MASK_RW = 0x02  # P1 - Read/Write
    MASK_E  = 0x04  # P2 - Enable
    MASK_BL = 0x08  # P3 - Backlight
    # Data pins D4-D7 are mapped to P4-P7

    def __init__(self, i2c_address):
        self.pcf = PCF8574_GPIO(i2c_address)
        self.backlight = self.MASK_BL
        self.init_lcd()

    def pulse_enable(self, data):
        # Pulse Enable pin High then Low to "latch" the data
        self.pcf.chip.writeByte(data | self.MASK_E | self.backlight)
        time.sleep(0.0005)
        self.pcf.chip.writeByte((data & ~self.MASK_E) | self.backlight)
        time.sleep(0.0005)

    def write_4_bits(self, value):
        self.pcf.chip.writeByte(value | self.backlight)
        self.pulse_enable(value)

    def send_command(self, cmd):
        # Send high nibble, then low nibble (RS = 0)
        self.write_4_bits(cmd & 0xF0)
        self.write_4_bits((cmd << 4) & 0xF0)

    def send_data(self, data):
        # Send high nibble, then low nibble (RS = 1)
        self.write_4_bits((data & 0xF0) | self.MASK_RS)
        self.write_4_bits(((data << 4) & 0xF0) | self.MASK_RS)

    def init_lcd(self):
        """ The mandatory 'Handshake' sequence to wake up the LCD """
        time.sleep(0.05)
        self.write_4_bits(0x30) # Special wakeup 1
        time.sleep(0.005)
        self.write_4_bits(0x30) # Special wakeup 2
        time.sleep(0.001)
        self.write_4_bits(0x30) # Special wakeup 3
        self.write_4_bits(0x20) # Set to 4-bit mode
        
        # Now we can use send_command for configuration
        self.send_command(0x28) # 2 lines, 5x8 font
        self.send_command(0x0C) # Display ON, Cursor OFF
        self.send_command(0x01) # Clear display
        time.sleep(0.005)

    def display_value(self, value: str):
        """ Now correctly displays strings/letters! """
        # Clear screen first if you want fresh text every time
        self.send_command(0x01) 
        time.sleep(0.002)
        
        for char in str(value):
            self.send_data(ord(char))

    def cleanup(self):
        self.send_command(0x01) # Clear screen on exit

#NOTE: Send string of max 16 chars
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
