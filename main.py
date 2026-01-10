import machine
from machine import Pin
from network import WLAN

import umqtt.simple
from display import EPD_2in9
from writer import Writer
from secrets import secrets
import ubuntu

def do_connect(ssid: str, key: str):
    import machine, network
    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))


class Display:
    def __init__(self, epd, w):
        self.epd = epd
        self.w = w

    def show_status(self, text):
        self.epd.fb.fill_rect(0, 0, 296, 128, self.epd.black)
        self.epd.fb.text(text, 0, 0, self.epd.white)
        self.epd.display()

    def show_temp(self, value):
        self.epd.fb.fill_rect(0, 0, 296, 128, self.epd.white)
        self.w.set_textpos(20,10)
        self.w.printstring(value, invert=True)
        self.epd.display()

led = Pin("LED", Pin.OUT)

epd = EPD_2in9(greyscale=True, landscape=True)
wu = Writer(epd.fb, ubuntu)

d = Display(epd, wu)

epd.init()

d.show_status("Connecting...")

do_connect(secrets["ssid"], secrets["pw"])

def cb(topic, value):
    print(value)
    temp = f"{float(value):#.1f}"
    d.show_temp(temp)

mq = umqtt.simple.MQTTClient(client_id="therm", server="192.168.0.95")
mq.connect()

d.show_temp("??")

mq.set_callback(cb)
mq.subscribe("sensor.hw.temp")

while True:
    r = mq.wait_msg()
    if r is None:
        machine.soft_reset()


