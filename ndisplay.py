# *****************************************************************************
# * | File        :	  Pico_CapTouch_ePaper_Test_2in9.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-06-02
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import micropython
from machine import Pin, SPI, I2C
import framebuf
import utime

# Display resolution
EPD_WIDTH = 128
EPD_HEIGHT = 296

WF_PARTIAL_2IN9 = [
    0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0A,0x0,0x0,0x0,0x0,0x0,0x0,
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
    0x22,0x17,0x41,0xB0,0x32,0x36,
]

WF_PARTIAL_2IN9_Wait = [
    0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0A,0x0,0x0,0x0,0x0,0x0,0x2,
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
    0x22,0x17,0x41,0xB0,0x32,0x36,
]

Gray4 = [
    0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x20, 0x60, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x28, 0x60, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x2A, 0x60, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x02, 0x00, 0x05, 0x14, 0x00, 0x00,
    0x1E, 0x1E, 0x00, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x02, 0x00, 0x05, 0x14, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x24, 0x22, 0x22, 0x22, 0x23, 0x32, 0x00, 0x00, 0x00,
    0x22, 0x17, 0x41, 0xAE, 0x32, 0x28
]

# e-Paper
RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

# TP
TRST    = 16
INT     = 17

# key
KEY0 = 2
KEY1 = 3
KEY2 = 15

class config():
    def __init__(self, i2c_addr):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        self.busy_pin = Pin(BUSY_PIN, Pin.IN)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)

        self.trst_pin = Pin(TRST, Pin.OUT)
        self.int_pin = Pin(INT, Pin.IN)

        self.key0 = Pin(KEY0, Pin.IN, Pin.PULL_UP)
        self.key1 = Pin(KEY1, Pin.IN, Pin.PULL_UP)
        self.key2 = Pin(KEY2, Pin.IN, Pin.PULL_UP)

        self.spi = SPI(1)
        self.spi.init(baudrate=4_000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.address = i2c_addr
        self.i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebytes(self, data):
        self.spi.write(data)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def i2c_writebyte(self, reg, value):
        wbuf = [(reg >> 8) & 0xff, reg & 0xff, value]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_write(self, reg):
        wbuf = [(reg >> 8) & 0xff, reg & 0xff]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_readbyte(self, reg, len):
        self.i2c_write(reg)
        rbuf = bytearray(len)
        self.i2c.readfrom_into(self.address, rbuf)
        return rbuf

    def module_exit(self):
        self.reset_pin.value(0)
        self.trst_pin.value(0)


class PortraitFrameBuffer(framebuf.FrameBuffer):
    def __init__(self, width, height, greyscale=True):
        divisor = 4 if greyscale else 8
        self.height = height
        self.width = width
        self.backing = bytearray(height * width // divisor)
        super().__init__(self.backing, width, height, framebuf.GS2_HMSB if greyscale else framebuf.MONO_HLSB)

    def buffer(self):
        return self.backing


class LandscapeFrameBuffer(framebuf.FrameBuffer):
    def __init__(self, width, height, greyscale=True):
        self.divisor = 4 if greyscale else 8
        self.height = height
        self.width = width

        self.size = height * width // self.divisor

        self.backing = bytearray(self.size)
        self.format = framebuf.GS2_HMSB if greyscale else framebuf.MONO_HLSB
        super().__init__(self.backing, self.width, self.height, self.format)

    @micropython.native
    def buffer(self):
        temp_backing = bytearray(self.size)
        temp = framebuf.FrameBuffer(temp_backing, self.height, self.width, self.format)

        for x in range(self.width):
            for y in range(self.height):
                color = self.pixel(x, y)
                temp.pixel(self.height - 1 - y, x, color)
        return temp_backing

class GreyscaleLut:

    def __init__(self):
        self.lutA = [0] * 256
        self.lutB = [0] * 256

        for v in range(256):
            p1 = p2 = 0
            for shift in (0, 2, 4, 6):
                pix = (v >> shift) & 0x03

                # pass 1: black + gray2
                p1 = (p1 << 1) | (1 if pix < 2 else 0)

                # pass 2: black + gray1
                p2 = (p2 << 1) | (1 if pix in (0, 2) else 0)

            self.lutA[v] = p1
            self.lutB[v] = p2

class EPD_2in9:
    def __init__(self, greyscale = False, landscape: bool = False):
        self.config = config(0x48)

        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.greyscale = greyscale

        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55

        self.lut = WF_PARTIAL_2IN9
        self.lut_l = WF_PARTIAL_2IN9_Wait
        self.gs_lut = GreyscaleLut()

        if landscape:
            self.fb = LandscapeFrameBuffer(self.height, self.width, greyscale)
        else:
            self.fb = PortraitFrameBuffer(self.width, self.height, greyscale)

    # Hardware reset
    def reset(self):
        self.config.reset_pin.value(1)
        self.config.delay_ms(50)
        self.config.reset_pin.value(0)
        self.config.delay_ms(2)
        self.config.reset_pin.value(1)
        self.config.delay_ms(50)

    def send_command(self, command):
        self.config.dc_pin.value(0)
        self.config.cs_pin.value(0)
        self.config.spi_writebyte([command])
        self.config.cs_pin.value(1)

    def send_datas(self, datas):
        self.config.dc_pin.value(1)
        self.config.cs_pin.value(0)
        self.config.spi_writebytes(datas)
        self.config.cs_pin.value(1)

    def send_data(self, data):
        self.config.dc_pin.value(1)
        self.config.cs_pin.value(0)
        self.config.spi_writebyte([data])
        self.config.cs_pin.value(1)

    def wait_for_idle(self):
        while self.config.busy_pin.value() == 1:  # 0: idle, 1: busy
            self.config.delay_ms(10)

    def TurnOnDisplay(self):
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xF7)
        self.send_command(0x20)  # MASTER_ACTIVATION
        self.wait_for_idle()

    def TurnOnDisplay_Partial(self):
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0x0F)
        self.send_command(0x20)  # MASTER_ACTIVATION
        self.wait_for_idle()

    def TurnOnDisplay_4Gray(self):
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xC7)
        self.send_command(0x20)  # MASTER_ACTIVATION
        self.wait_for_idle()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def SendLut(self, isQuick):
        self.send_command(0x32)
        if isQuick:
            lut = self.lut
        else:
            lut = self.lut_l

        for i in range(0, 153):
            self.send_data(lut[i])
        self.wait_for_idle()

    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44)  # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start >> 3) & 0xFF)
        self.send_data((x_end >> 3) & 0xFF)
        self.send_command(0x45)  # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def SetCursor(self, x, y):
        self.send_command(0x4E)  # SET_RAM_X_ADDRESS_COUNTER
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x >> 3) & 0xFF)

        self.send_command(0x4F)  # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.wait_for_idle()

    def SetLut(self, lut):
        self.send_command(0x32)
        for i in range(0, 153):
            self.send_data(lut[i])
        self.wait_for_idle()
        self.send_command(0x3f)
        self.send_data(lut[153])
        self.send_command(0x03)  # gate voltage
        self.send_data(lut[154])
        self.send_command(0x04)  # source voltage
        self.send_data(lut[155])  # VSH
        self.send_data(lut[156])  # VSH2
        self.send_data(lut[157])  # VSL
        self.send_command(0x2c)  # VCOM
        self.send_data(lut[158])

    def init(self):
        if self.greyscale:
            self._init_greyscale()
        else:
            self._init_mono()

    def _init_mono(self):
        # EPD hardware init start
        self.reset()

        self.wait_for_idle()
        self.send_command(0x12)  # SWRESET
        self.wait_for_idle()

        self.send_command(0x01)  # Driver output control
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width - 1, self.height - 1)

        self.send_command(0x21)  # Display update control
        self.send_data(0x00)
        self.send_data(0x80)

        self.SetCursor(0, 0)
        self.wait_for_idle()
        # EPD hardware init end
        return 0

    def _init_greyscale(self):
        self.reset()

        self.wait_for_idle()
        self.send_command(0x12)  # SWRESET
        self.wait_for_idle()

        self.send_command(0x01)  # Driver output control
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)

        self.SetWindow(8, 0, self.width, self.height - 1)

        self.send_command(0x3C)
        self.send_data(0x04)

        self.SetCursor(8, 0)
        self.wait_for_idle()

        self.SetLut(Gray4)
        # EPD hardware init end
        return 0

    def display(self):
        if self.greyscale:
            self._display_grey()
        else:
            self._display(self.fb.buffer())

    def _display(self, image):
        if image is None:
            return
        self.send_command(0x24) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            # for i in range(0, int(self.width / 8)):
            self.send_data(image[i])
        self.TurnOnDisplay()

    def display_Base(self, image):
        if image is None:
            return
        self.send_command(0x24) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.send_command(0x26) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.TurnOnDisplay()

    def display_Partial(self, image):
        if (image == None):
            return

        self.config.reset_pin.value(0)
        self.config.delay_ms(0.2)
        self.config.reset_pin.value(1)

        self.SendLut(1)
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.wait_for_idle()

        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x24) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.TurnOnDisplay_Partial()

    def _display_grey(self):

        b = self.fb.buffer()

        out1 = bytearray(4736)
        out2 = bytearray(4736)

        lut = self.gs_lut

        for i in range(4736):
            b0 = b[2*i]
            b1 = b[2*i + 1]

            out1[i] = (lut.lutA[b0] << 4) | lut.lutA[b1]
            out2[i] = (lut.lutB[b0] << 4) | lut.lutB[b1]

        self.send_command(0x24)
        self.send_datas(out1)
        self.send_command(0x26)
        self.send_datas(out2)

        self.TurnOnDisplay_4Gray()

    def Clear(self, color):
        self.send_command(0x24)  # WRITE_RAM
        for i in range(0, self.height * int(self.width / 8)):
            self.send_data(color)
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10)  # DEEP_SLEEP_MODE
        self.send_data(0x01)

        self.config.delay_ms(2000)
        self.module_exit()
