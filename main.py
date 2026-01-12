
from display import EPD_2in9

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
