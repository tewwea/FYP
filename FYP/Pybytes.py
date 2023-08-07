import time
import pycom
from pycoproc_1 import Pycoproc


from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE


pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

py = Pycoproc(Pycoproc.PYSENSE)

pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True

mp = MPL3115A2(py,mode=ALTITUDE) 
print("Temperature: " + str(mp.temperature()))
print("Altitude: " + str(mp.altitude()))
mpp = MPL3115A2(py,mode=PRESSURE) 
print("Pressure: " + str(mpp.pressure()))

si = SI7006A20(py)
print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")
t_ambient = 24.4
print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")


lt = LTR329ALS01(py)
print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

li = LIS2HH12(py)
print("Acceleration: " + str(li.acceleration()))
print("Roll: " + str(li.roll()))
print("Pitch: " + str(li.pitch()))





if(pybytes_enabled):
    pybytes.send_signal(1, mpp.pressure())
    pybytes.send_signal(2, si.temperature())
    pybytes.send_signal(3, mp.altitude())
    pybytes.send_signal(4, si.humidity())
    print("Sent data to pybytes")

