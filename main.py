from ntptime import settime
import urequests
import utime
from machine import Pin
import json

#Replace these with your lat and long values
lat = 43.6954 
lng = -116.3540
led = Pin(13, Pin.OUT)

#sonoff led is active low, this sets it off by default
led.value(1) 
relay = Pin(12, Pin.OUT)
button = Pin(0, Pin.IN, Pin.PULL_UP)

#set internal time according to network time
settime()

def api_call():
    r = urequests.get("https://api.sunrise-sunset.org/json?lat={}&lng={}&formatted=0".format(lat, lng)).json()
    sunrise_loc = r["results"]["sunrise"] 
    sunset_loc = r["results"]["sunset"]
    #Make sunrise & sunset time into list of ints that utime.mktime() will convert; this is very likely the worst way to do this.
    sunrise = list(map(int, [sunrise_loc[0:4], sunrise_loc[5:7], sunrise_loc[8:10], sunrise_loc[11:13], sunrise_loc[14:16], sunrise_loc[17:19], 0, 0]))
    sunset = list(map(int, [sunset_loc[0:4], sunset_loc[5:7], sunset_loc[8:10], sunset_loc[11:13], sunset_loc[14:16], sunset_loc[17:19], 0, 0]))
    return sunrise, sunset

while True:
    rise_time, set_time = api_call()
    rise_time, set_time = utime.mktime(rise_time), utime.mktime(set_time) 
    if rise_time <= utime.time() < set_time:
        #Turn the led & relay on
        relay.value(1)
        led.value(0)
    elif set_time >= utime.time():
        #Turn the led & relay off
        relay.value(0)
        led.value(1)

    utime.sleep(300)
