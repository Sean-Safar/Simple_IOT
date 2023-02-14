import machine
import esp32
from machine import Pin,Timer
from neopixel import NeoPixel
import network
import socket

# Global variables
temp = str(esp32.raw_temperature()) # measure temperature sensor data
hall = str(esp32.hall_sensor()) # measure hall sensor data
red_led = Pin(13, Pin.OUT)
red_led.value(0)
red_led_state = 'OFF'# string, check state of red led, ON or OFF
wlan = network.WLAN(network.STA_IF)

def connect_wifi():
    #wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #ssid = "Safar"
    ssid = "Rise Resident"
    pswrd = "Boilermakers*100"
    #pswrd = "sports23"
    if wlan.isconnected():
        wlan.disconnect
    if not wlan.isconnected():
        wlan.connect(ssid,pswrd)
    while not wlan.isconnected():
        pass
    print("Connected to Safar")
    print("IP Address: {}".format(wlan.ifconfig()[0]))
    
def web_page():
    global temp,hall,red_led_state
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage


connect_wifi()
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_addr = socket.getaddrinfo(str(wlan.ifconfig()[0]),80)[0][-1]
s.bind(sock_addr)
s.listen(1)

web_page()

while True:
    conn, addr = s.accept()
 
    print("Connected to {}".format(str(addr)))
    request = conn.recv(1024)
    request = str(request)

    if '/?red_led=on' in request:
        red_led.value(1)
        red_led_state = 'ON'
    elif '/?red_led=off' in request:
        red_led.value(0)
        red_led_state = 'OFF'

    temp = str(esp32.raw_temperature())
    hall = str(esp32.hall_sensor())

    conn.sendall(web_page())
    conn.close()
