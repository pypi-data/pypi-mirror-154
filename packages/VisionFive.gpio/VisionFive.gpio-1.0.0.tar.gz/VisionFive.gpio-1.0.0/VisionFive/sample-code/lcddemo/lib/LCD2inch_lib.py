import os
import sys 
import time
import logging
import VisionFive.spi as spi
import VisionFive.gpio as gpio
import numpy as np
from PIL import Image,ImageDraw,ImageFont

class LCD_2inch():
    width  = 240
    height = 320    
    def __init__(self, rst_pin, dc_pin, dev):        
        self.rstpin = rst_pin
        self.dcpin  = dc_pin
        self.spidev  = dev      
        spi.getdev(self.spidev)
        spi.setmode(500000, 0, 8)
        gpio.setup(self.rstpin, gpio.OUT)
        gpio.setup(self.dcpin, gpio.OUT)
        
    def __del__(self):        
        spi.freedev()  
    
    def lcd_reset(self):   
        gpio.output(self.rstpin, gpio.HIGH)       
        gpio.output(self.rstpin, gpio.LOW)
        time.sleep(0.01)
        gpio.output(self.rstpin, gpio.HIGH)
       
    def lcd_spisend(self, data):
        spi.transfer(data)
        
    def lcd_sendcmd(self, cmd):   
        gpio.output(self.dcpin, gpio.LOW)
        spi.transfer(cmd)

    def lcd_senddata(self,data):
        gpio.output(self.dcpin, gpio.HIGH)
        spi.transfer(data)    
    
    def lcd_init(self):
        self.lcd_reset()      
        
        self.lcd_sendcmd(0x36)
        self.lcd_senddata(0x00) 
    
        self.lcd_sendcmd(0x3A) 
        self.lcd_senddata(0x05)
    
        self.lcd_sendcmd(0x21)
    
        self.lcd_sendcmd(0x2A)
        self.lcd_senddata(0x00)
        self.lcd_senddata(0x00)
        self.lcd_senddata(0x01)
        self.lcd_senddata(0x3F)
    
        self.lcd_sendcmd(0x2B)
        self.lcd_senddata(0x00)
        self.lcd_senddata(0x00)
        self.lcd_senddata(0x00)
        self.lcd_senddata(0xEF)
    
        self.lcd_sendcmd(0xB2)
        self.lcd_senddata(0x0C)
        self.lcd_senddata(0x0C)
        self.lcd_senddata(0x00)
        self.lcd_senddata(0x33)
        self.lcd_senddata(0x33)
    
        self.lcd_sendcmd(0xB7)
        self.lcd_senddata(0x35)
    
        self.lcd_sendcmd(0xBB)
        self.lcd_senddata(0x1F)
    
        self.lcd_sendcmd(0xC0)
        self.lcd_senddata(0x2C)
    
        self.lcd_sendcmd(0xC2)
        self.lcd_senddata(0x01)
    
        self.lcd_sendcmd(0xC3)
        self.lcd_senddata(0x12)  
    
        self.lcd_sendcmd(0xC4)
        self.lcd_senddata(0x20)
    
        self.lcd_sendcmd(0xC6)
        self.lcd_senddata(0x0F)
    
        self.lcd_sendcmd(0xD0)
        self.lcd_senddata(0xA4)
        self.lcd_senddata(0xA1)
    
        self.lcd_sendcmd(0xE0)
        self.lcd_senddata(0xD0)
        self.lcd_senddata(0x08)
        self.lcd_senddata(0x11)
        self.lcd_senddata(0x08)
        self.lcd_senddata(0x0C)
        self.lcd_senddata(0x15)
        self.lcd_senddata(0x39)
        self.lcd_senddata(0x33)
        self.lcd_senddata(0x50)
        self.lcd_senddata(0x36)
        self.lcd_senddata(0x13)
        self.lcd_senddata(0x14)
        self.lcd_senddata(0x29)
        self.lcd_senddata(0x2D)
    
        self.lcd_sendcmd(0xE1)
        self.lcd_senddata(0xD0)
        self.lcd_senddata(0x08)
        self.lcd_senddata(0x10)
        self.lcd_senddata(0x08)
        self.lcd_senddata(0x06)
        self.lcd_senddata(0x06)
        self.lcd_senddata(0x39)
        self.lcd_senddata(0x44)
        self.lcd_senddata(0x51)
        self.lcd_senddata(0x0B)
        self.lcd_senddata(0x16)
        self.lcd_senddata(0x14)
        self.lcd_senddata(0x2F)
        self.lcd_senddata(0x31)
        self.lcd_sendcmd(0x21)
    
        self.lcd_sendcmd(0x11)
    
        self.lcd_sendcmd(0x29)
        self.lcd_clear(0xff)    
    
    def lcd_setPos(self, Xstart, Ystart, Xend, Yend):
    
        self.lcd_sendcmd(0x2a)
        self.lcd_senddata(Xstart >>8)
        self.lcd_senddata(Xstart & 0xff)
        self.lcd_senddata((Xend - 1) >> 8)
        self.lcd_senddata((Xend - 1) & 0xff)    
        self.lcd_sendcmd(0x2b)
        self.lcd_senddata(Ystart >>8)
        self.lcd_senddata(Ystart & 0xff)
        self.lcd_senddata((Yend - 1) >> 8)
        self.lcd_senddata((Yend - 1) & 0xff)    
        self.lcd_sendcmd(0x2C)
    
    def lcd_clear(self, color):

        """Clear contents of image buffer"""
        
        _buffer = [color]*(self.width * self.height *2)  
               
        self.lcd_setPos(0, 0, self.width, self.height)
        gpio.output(self.dcpin, gpio.HIGH)        
        for i in range(0,len(_buffer)):
            self.lcd_spisend(_buffer[i])    
            
            
    def lcd_ShowImage(self, Image, Xstart, Ystart):    
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""               
        imwidth, imheight = Image.size
        
        if imwidth == self.height and imheight == self.width:            
            img = np.asarray(Image)
            pix = np.zeros((self.width, self.height,2), dtype = np.uint8)
            #RGB888 >> RGB565
            pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
            pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0), np.right_shift(img[...,[2]],3))
            pix = pix.flatten().tolist()
            
            self.lcd_sendcmd(0x36)
            self.lcd_senddata(0x70) 
            self.lcd_setPos(0, 0, self.height, self.width)
            
            gpio.output(self.dcpin, gpio.HIGH)  
            for i in range(0,len(pix),1):
               self.lcd_spisend(pix[i])
            
        else :            
            img = np.asarray(Image)
            pix = np.zeros((imheight, imwidth, 2), dtype = np.uint8)
            
            pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
            pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0), np.right_shift(img[...,[2]],3))

            pix = pix.flatten().tolist()
            
            self.lcd_sendcmd(0x36)
            self.lcd_senddata(0x00) 
            self.lcd_setPos(0, 0, self.width, self.height)
           
            gpio.output(self.dcpin, gpio.HIGH)  
            for i in range(0,len(pix)):
                self.lcd_spisend(pix[i])

    
    

