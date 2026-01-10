import time
from machine import Pin

from display import EPD_2in9
from writer import  Writer

led = Pin("LED", Pin.OUT)

epd = EPD_2in9(greyscale=True, landscape=True)

# epd.clear(0xff)
# epd.TurnOnDisplay()

epd.init()
epd.fb.fill_rect(0, 0, 296, 32, epd.black)
epd.fb.text('GRAY1', 128, 8, epd.white)
epd.fb.fill_rect(0, 32, 296, 32, epd.darkgray)
epd.fb.text('GRAY2', 128, 40, epd.grayish)
epd.fb.fill_rect(0, 64, 296, 32, epd.grayish)
epd.fb.text('GRAY3', 128, 72, epd.darkgray)
epd.fb.fill_rect(0, 96, 296, 32, epd.white)
epd.fb.text('GRAY4', 128, 104, epd.black)
epd.display()

