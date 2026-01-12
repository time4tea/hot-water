# import time
#
# import images
# import machine
# import network
# import socket
#
# import ubuntu
# import umqtt.simple
# from config import config
from display import EPD_2in9
# from writer import Writer

# led = machine.Pin("LED", machine.Pin.OUT)
#
# class Remote:
#     def __init__(self, ip, port):
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.ip = ip
#         self.port = port
#
#     def send(self, data):
#         self.socket.sendto(data, (self.ip, self.port))
#
# class Flasher:
#     def __init__(self):
#         self.pin = machine.Pin("LED", machine.Pin.OUT)
#
#     def flash(self, n):
#         for x in range(0, n):
#             self.pin.high()
#             time.sleep_ms(50)
#             self.pin.low()
#             time.sleep_ms(50)
#
# flasher = Flasher()
#
# def do_connect(ssid: str, key: str, timeout_ms=15000):
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     time.sleep_ms(500)  # give firmware a chance
#
#     if wlan.isconnected():
#         led.on()
#         return wlan
#
#     wlan.connect(ssid, key)
#     start = time.ticks_ms()
#
#     while True:
#         status = wlan.status()
#
#         if status == network.STAT_CONNECTING:
#             print("Connecting")
#             flasher.flash(1)
#
#         if status == network.STAT_GOT_IP:
#             print("Got IP")
#             flasher.flash(2)
#             return wlan
#
#         if status == network.STAT_CONNECT_FAIL:
#             print("Failed retrying")
#             flasher.flash(10)
#             wlan.disconnect()
#             time.sleep_ms(1000)
#             wlan.connect(ssid, key)
#
#         if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
#             print("Gave up")
#             led.off()
#             return None
#
#         time.sleep_ms(200)
#
#
# class Display:
#     def __init__(self, epd, w):
#         self.epd = epd
#         self.w = w
#
#     def clear(self, colour=None):
#         self.epd.fb.fill_rect(0, 0, 296, 128, colour if colour is not None else self.epd.white)
#
#     def show_status(self, text):
#         self.clear(self.epd.black)
#         self.epd.fb.text(text, 0, 0, self.epd.white)
#
#     def show_temp(self, value):
#         self.w.set_textpos(20, 10)
#         self.w.printstring(value, invert=True)
#
#     def arrow(self, image: images.Bitmap):
#         image.blit(self.epd.fb, 296 - (image.width + 4), (128 // 2) - (image.height + 8), self.epd.black,
#                    self.epd.white)
#
#     def heat(self, image: images.Bitmap):
#         image.blit(self.epd.fb, 296 - (image.width + 4), (128 // 2) + 8, self.epd.black, self.epd.white)
#
#     def update(self):
#         self.epd.display()
#
#
# class State:
#     def __init__(self):
#         self.temp = None
#         self.heating = False
#         self.increasing = None
#
#     def cb(self, topic, value):
#         print(f"{topic} -> {value}")
#
#         if topic == b"sensor.hw.temp":
#             latest_temp = float(value)
#             print(f"Temperature update to {latest_temp}")
#
#             if self.temp is not None:
#                 self.increasing = latest_temp > self.temp
#
#             self.temp = latest_temp
#
#         elif topic == b'sensor.hw.status':
#             print(f"Heating update tp {value}")
#             self.heating = value == b'heat_water'
#
#     def draw(self, d: Display):
#         d.clear()
#         if self.temp is None:
#             d.show_temp("??")
#         else:
#             d.show_temp(f"{self.temp:#.1f}")
#
#         if self.increasing is not None:
#             d.arrow(images.up if self.increasing else images.down)
#
#         if self.heating:
#             d.heat(images.heat)
#
#         d.update()



epd = EPD_2in9(greyscale=True, landscape=False)
epd.init()
epd.fb.fill_rect(0, 0, 127, 74, epd.black)
epd.fb.text('GRAY1',10, 33, epd.white)
epd.fb.fill_rect(0, 74, 127, 74, epd.darkgray)
epd.fb.text('GRAY2',10, 107, epd.grayish)
epd.fb.fill_rect(0, 148, 127, 74, epd.grayish)
epd.fb.text('GRAY3',10, 181, epd.darkgray)
epd.fb.fill_rect(0, 222, 127, 74, epd.white)
epd.fb.text('GRAY4',10, 255, epd.black)
epd.display()
epd.delay_ms(500)

# flasher.flash(1)

# wifi = do_connect(config["wlan"]["ssid"], config["wlan"]["pw"])
# remote = Remote('192.168.0.127', 1880)
#
# s = State()
#
# remote.send(b'Connecting to mq')
#
# flasher.flash(10)
# print("Connecting to mq")
#
# mq = umqtt.simple.MQTTClient(client_id=config["mqtt"]["name"], server=config["mqtt"]["server"])
# mq.connect()
#
# remote.send(b'Connected to mq')
# print("Connected to mq")
#
# mq.set_callback(s.cb)
# mq.subscribe("sensor.hw.temp")
# mq.subscribe("sensor.hw.status")
# remote.send(b'Subscribed')


# while True:
#     try:
#         r = mq.wait_msg()
#         if r is not None:
#             remote.send("Updating display")
#     except OSError:
#         machine.soft_reset()



# try:
#
#     epd = EPD_2in9(greyscale=True, landscape=True)
#     flasher.flash(2)
#     wu = Writer(epd.fb, ubuntu)
#
#     d = Display(epd, wu)
#
#     s = State()
#
#     epd.init()
#     flasher.flash(3)
#     d.show_status("Connecting...")
#     d.update()
#
#     flasher.flash(2)
#     wifi = do_connect(config["wlan"]["ssid"], config["wlan"]["pw"])
#
#     if wifi is None:
#         d.show_status("didn't connect ...")
#         d.update()
#     else:
#         d.show_status(wifi.ifconfig()[0])
#         d.update()
#
#     remote = Remote('192.168.0.127', 1880)
#
#     remote.send(b'Connecting to mq')
#
#     flasher.flash(10)
#     print("Connecting to mq")
#
#     mq = umqtt.simple.MQTTClient(client_id=config["mqtt"]["name"], server=config["mqtt"]["server"])
#     mq.connect()
#
#     remote.send(b'Connected to mq')
#     print("Connected to mq")
#     s.draw(d)
#
#     mq.set_callback(s.cb)
#     mq.subscribe("sensor.hw.temp")
#     mq.subscribe("sensor.hw.status")
#
#     s.draw(d)
#     flasher.flash(1)
#     remote.send("Updating display")
#
#     while True:
#         try:
#             r = mq.wait_msg()
#             if r is not None:
#                 remote.send("Updating display")
#                 s.draw(d)
#                 flasher.flash(1)
#         except OSError:
#             machine.soft_reset()
# except:
#     flasher.flash(50)
#     raise
