import machine
from machine import Pin

import images
import ubuntu
import umqtt.simple
from display import EPD_2in9
from config import config
from writer import Writer


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

    def clear(self, colour=None):
        self.epd.fb.fill_rect(0, 0, 296, 128, colour if colour is not None else self.epd.white)

    def show_status(self, text):
        self.clear(self.epd.black)
        self.epd.fb.text(text, 0, 0, self.epd.white)

    def show_temp(self, value):
        self.w.set_textpos(20, 10)
        self.w.printstring(value, invert=True)

    def image(self, image: images.Bitmap):
        image.blit(self.epd.fb, 296 - (image.width + 4), (128 // 2) - (image.height // 2), self.epd.black, self.epd.white)

    def update(self):
        self.epd.display()


led = Pin("LED", Pin.OUT)

epd = EPD_2in9(greyscale=True, landscape=True)
wu = Writer(epd.fb, ubuntu)

d = Display(epd, wu)

epd.init()

d.show_status("Connecting...")
d.update()

do_connect(config["wlan"]["ssid"], config["wlan"]["pw"])

last_temp = None


def cb(topic, value):
    global last_temp
    print(value)

    temp = float(value)
    d.clear()
    d.show_temp(f"{temp:#.1f}")

    if last_temp is not None:
        if temp < last_temp:
            d.image(images.down)
        else:
            d.image(images.up)

    last_temp = temp
    d.update()


mq = umqtt.simple.MQTTClient(client_id=config["mqtt"]["name"], server=config["mqtt"]["server"])
mq.connect()

d.clear()
d.show_temp("??")
d.update()

mq.set_callback(cb)
mq.subscribe("sensor.hw.temp")

while True:
    r = mq.wait_msg()
    if r is None:
        machine.soft_reset()
