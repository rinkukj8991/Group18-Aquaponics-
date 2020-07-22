import os
import glob
import time
import paho.mqtt.client as mqtt
import random
import spidev
from numpy import interp
import RPi.GPIO as gpio
gpio.setwarnings(False)
client= mqtt.Client()
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
gpio.setmode(gpio.BCM)
relayH = 18
relayC = 23
relayP = 24
relayO = 25
buz = 3
gpio.setwarnings(False)
gpio.setup(relayH,gpio.OUT)
gpio.setup(relayC,gpio.OUT)
gpio.setup(relayP,gpio.OUT)
gpio.setup(relayO,gpio.OUT)
gpio.setup(buz,gpio.OUT)
gpio.output(relayH,1)
gpio.output(relayC,1)
gpio.output(relayP,1)
gpio.output(relayO,1)
time.sleep(0.5)
gpio.output(relayO,0)
# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0)

client.connect('localhost', 1883, 60)
# Connect to the MQTT server and process messages in a background thread.
client.loop_start()
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

def analog(channel):
	spi.max_speed_hz = 1350000
	adc = spi.xfer2([1,(8+channel)<<4,0])
	output = ((adc[1]&3) << 8) + adc[2]
	out = interp(output, [0, 1023], [0,14])
	return out


def buz():
	gpio.output(buz,1)
	time.sleep(1)
	gpio.output(buz,0)
	time.sleep(1)

while True:
	#print(read_temp())
	temp = float(read_temp())
	ph=analog(0)
	ph=float(ph)-1
	ph = '{0:0.1f}' .format(ph)
	ph=float(ph)
	
	#print(ph)
	if (ph > float(6.8) and ph < float(7.6)):
		print("Normal")
		#time.sleep(2)
	else:
            #gpio.output(relayP,0)
            print("NOT Normal")
            time.sleep(0.5)
            for i in range (0,15):
                print(i)
                temp = float(read_temp())
                print(temp,ph)
                ph=analog(0)
                ph=float(ph)-1
                ph = '{0:0.1f}' .format(ph)
                ph=float(ph)
                #print(ph)
                time.sleep(1)
                if float(temp) < float(20):
                    gpio.output(relayH,0)
                    gpio.output(relayC,1)
                if float(30) <= float(temp) <= float(100):
                    gpio.output(relayC,0)
                    gpio.output(relayH,1)
                    gpio.output(3,1)
                    time.sleep(3)
                    gpio.output(3,0)
                    time.sleep(3)
                if float(20) < temp < float(30):
                    gpio.output(relayC,1)
                    gpio.output(relayH,1)
                if (ph > float(6.8) and ph < float(7.6)):
                    break
                if i==14:
                    gpio.output(3,1)
                    time.sleep(3)
                    gpio.output(3,0)
                    time.sleep(3)
                    gpio.output(relayP,1)
                    time.sleep(2)
                    gpio.output(relayP,0)
                    print("Motor ON")
                    time.sleep(5)
                    gpio.output(relayP,1)
                    time.sleep(1)
            time.sleep(0.5)
     

		
	
	client.publish('ph', ph)
	if float(temp) < float(20):
		gpio.output(relayH,0)
		gpio.output(relayC,1)
	if float(30) <= float(temp) <= float(100):
	       gpio.output(relayC,0)
	       gpio.output(relayH,1)
	       gpio.output(3,1)
	       time.sleep(3)
	       gpio.output(3,0)
	       time.sleep(3)
	if float(20) < temp < float(30):
		gpio.output(relayC,1)
		gpio.output(relayH,1)
		
	time.sleep(1)


