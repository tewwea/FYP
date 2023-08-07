

import time
import math
import pycom
import serial
import machine
from pycoproc_1 import Pycoproc


from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

MG_PIN = machine.Pin(14)
BOOL_PIN = machine.Pin(15)
READTIMES = 10
READINTERVAL = 50
DC_GAIN = 6.85
ZERO_POINT_VOLTAGE = 0.33

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

def MGRead():
    readings = []
    for i in range(READTIMES):
        readings.append(machine.ADC.read(MG_PIN))
    return sum(readings) / READTIMES

volts = MGRead(MG_PIN)
CO2Curve = [0.961, -2.178, 0.00903]
def MGGetPercentage(volts):
    if volts >= ZERO_POINT_VOLTAGE:
        return -1
    else:
        return pow(10, ((volts / DC_GAIN) - CO2Curve[1]) / CO2Curve[2] + CO2Curve[0])

percentage = MGGetPercentage(volts)
print("CO2:", percentage, "ppm")


    
    

vmax = 4.2
vmin = 3.3
battery_voltage = py.read_battery_voltage()
battery_percentage = (battery_voltage - vmin / (vmax - vmin))*100
print("Battery voltage: " + str(py.read_battery_voltage()), " percentage: ", battery_percentage)
if(pybytes_enabled):
    pybytes.send_signal(1, mpp.pressure())
    pybytes.send_signal(2, si.temperature())
    pybytes.send_signal(3, li.acceleration())
    pybytes.send_signal(4, si.humidity())
    pybytes.send_signal(5, mp.altitude())
    pybytes.send_signal(6, percentage())
    print("Sent data to pybytes")

time.sleep(5)
py.setup_sleep(10)
py.go_to_sleep()