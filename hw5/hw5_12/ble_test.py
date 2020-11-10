import sys
import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral


button_service_uuid = UUID(0xA000)
button_char_uuid    = UUID(0xA001)
LED_service_uuid    = UUID(0xA100)
LED_char_uuid       = UUID(0xA101)

p = Peripheral("e5:d3:1d:fc:b0:d3", "random")
ButtonService=p.getServiceByUUID(button_service_uuid)
LEDService = p.getServiceByUUID(LED_service_uuid)

try:
    ch = ButtonService.getCharacteristics(button_char_uuid)[0]
    ch2 = LEDService.getCharacteristics(LED_char_uuid)[0]
    while 1:
        if (ch.supportsRead()):
            val = binascii.b2a_hex(ch.read())
            if(val == "00"):
                print("The button is not pressed.")
            else:
                print("The button is pressed.")
        LED_in = raw_input("Turn on the LED ? (y/n)")
        writevalue = 0
        if(LED_in == 'y'):
            writevalue = "01"
        else:
            writevalue = "00"
        ch2.write(binascii.a2b_hex(writevalue))
        time.sleep(1)


finally:
    p.disconnect()  