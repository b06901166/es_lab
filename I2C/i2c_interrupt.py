import smbus
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

bus = smbus.SMBus(1)
bus.write_byte_data(0x53,0x27, 0xff)
bus.write_byte_data(0x53,0x31, 0x0B)
bus.write_byte_data(0x53,0x2D, 0x08)
bus.write_byte_data(0x53,0x2E, 0x80)
#activity detect config
bus.write_byte_data(0x53,0x24,20)
int_act = 0x10
intEnable = bus.read_byte_data(0x53,0x2E)
bus.write_byte_data(0x53,0x2E,int_act)

#inactivity detect config
bus.write_byte_data(0x53,0x25,20)
bus.write_byte_data(0x53,0x26,1)
int_inact = 0x08
intEnable = bus.read_byte_data(0x53,0x2E)
#bus.write_byte_data(0x53,0x2E, 0x10)
#print(bus.read_byte_data(0x53,0x2E))

bus.write_byte_data(0x53,0x2F,0xef)

#inter = bus.read_byte_data(0x53,0x30)
def my_callback(channel):
    inter = bus.read_byte_data(0x53,0x30)
    if((inter&0x10)==0x10):
        print("ACT detected\n")
        bytes = bus.read_i2c_block_data(0x53,0x32,6)
    	x = bytes[0] | (bytes[1]<<8)
    	if(x&(1<<16-1)):
        	x = x - (1<<16)
    	y = bytes[2] | (bytes[3]<<8)
    	if(y&(1<<16-1)):
        	y = y - (1<<16)
    	z = bytes[4] | (bytes[5]<<8)
    	if(z&(1<<16-1)):
        	z = z - (1<<16)
    	x = x*0.004
    	y = y*0.004
    	z = z*0.004
    	x = round(x,4)
    	y = round(y,4)
    	z = round(z,4)
    	print "x = %.3fG, y = %.3fG, z = %.3fG"%(x,y,z)
        print("\n")
GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback)
try:
    while(True):
        inter = bus.read_byte_data(0x53,0x30)
        sleep(1);
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
GPIO.cleanup()

