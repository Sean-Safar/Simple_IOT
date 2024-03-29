import machine
from machine import Pin,Timer,RTC,ADC,TouchPad
from neopixel import NeoPixel
import network
import esp32
import ntptime
import socket

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ssid = ""
    pswrd = ""

    if wlan.isconnected():
        wlan.disconnect
    if not wlan.isconnected():
        wlan.connect(ssid,pswrd)
    while not wlan.isconnected():
        pass
    print("Connected to ")
    print("IP Address: {}".format(wlan.ifconfig()[0]))

def measure(self):
    global temp
    global hall
    temp = str(esp32.raw_temperature())
    hall = str(esp32.hall_sensor())
    print("Temperature: {}".format(temp))
    print("Hall Sensor: {}".format(hall))
    sockaddr = socket.getaddrinfo('api.thingspeak.com', 80)[0][-1]
    s = socket.socket()
    s.connect(sockaddr)
    s.send("GET https://api.thingspeak.com/update?api_key=PQJDPH37WSCAMIAT&field1=" +temp+ "&field2=" +hall+ "HTTP/1.0\r\n\r\n")
    s.close() 
   
if __name__ == '__main__':
    connect_wifi()
    Timer_measure = Timer(1)
    Timer_measure.init(mode=Timer.PERIODIC, period=30000, callback=measure)

