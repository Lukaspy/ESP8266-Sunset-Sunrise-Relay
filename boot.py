import utime
import network
from ntptime import settime

sta_if = network.WLAN(network.STA_IF)
#Halt booting until internet connectivity is established
while not sta_if.isconnected():
    print(".", end="")
    utime.sleep(1)
