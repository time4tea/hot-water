import machine

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

    def arrow(self, image: images.Bitmap):
        image.blit(self.epd.fb, 296 - (image.width + 4), (128 // 2) - (image.height + 8), self.epd.black,
                   self.epd.white)

    def heat(self, image: images.Bitmap):
        image.blit(self.epd.fb, 296 - (image.width + 4), (128 // 2) + 8, self.epd.black, self.epd.white)

    def update(self):
        self.epd.display()


class State:
    def __init__(self):
        self.temp = None
        self.heating = False
        self.increasing = None

    def cb(self, topic, value):
        print(f"{topic} -> {value}")

        if topic == b"sensor.hw.temp":
            latest_temp = float(value)
            print(f"Temperature update to {latest_temp}")

            if self.temp is not None:
                self.increasing = latest_temp > self.temp

            self.temp = latest_temp

        elif topic == b'sensor.hw.status':
            print(f"Heating update tp {value}")
            self.heating = value == b'heat_water'

    def draw(self, d: Display):
        d.clear()
        if self.temp is None:
            d.show_temp("??")
        else:
            d.show_temp(f"{self.temp:#.1f}")

        if self.increasing is not None:
            d.arrow(images.up if self.increasing else images.down)

        if self.heating:
            d.heat(images.heat)

        d.update()


epd = EPD_2in9(greyscale=True, landscape=True)
wu = Writer(epd.fb, ubuntu)

d = Display(epd, wu)

s = State()

epd.init()

d.show_status("Connecting...")
d.update()

do_connect(config["wlan"]["ssid"], config["wlan"]["pw"])

mq = umqtt.simple.MQTTClient(client_id=config["mqtt"]["name"], server=config["mqtt"]["server"])
mq.connect()

s.draw(d)

mq.set_callback(s.cb)
mq.subscribe("sensor.hw.temp")
mq.subscribe("sensor.hw.status")

s.draw(d)

while True:
    try:
        r = mq.wait_msg()
        if r is not None:
            s.draw(d)
    except OSError:
        machine.soft_reset()