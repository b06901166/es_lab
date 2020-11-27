import sys
import binascii
import struct
import time
from bluepy.btle import *

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(data)
    def enable_notify(self,  chara_uuid):
        setup_data = b"\x01\x00"
        notify = self.ble_conn.getCharacteristics(uuid=chara_uuid)[0]
        notify_handle = notify.getHandle() + 1
        self.ble_conn.writeCharacteristic(notify_handle, setup_data, withResponse=True)

button_service_uuid = UUID(0xA000)
button_char_uuid    = UUID(0xA001)

p = Peripheral("e5:d3:1d:fc:b0:d3", "random")
p.setDelegate(MyDelegate())
print("Connected")
ButtonService=p.getServiceByUUID(button_service_uuid)
try:
    setup_data = b"\x01\x00"
    notify = ButtonService.getCharacteristics(button_char_uuid)[0]
    notify_handle = notify.getHandle() + 1
    p.writeCharacteristic(notify_handle, setup_data, withResponse=True)
    print("writing done")
    while True:
        if p.waitForNotifications(1.0):
            print("Notification")
            continue
    print("Waiting")
finally:
    p.disconnect()
    print ("Disconnected")