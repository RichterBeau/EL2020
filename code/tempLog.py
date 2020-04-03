#Import Libraries
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as sql
import smtplib


#declare pins
redPin = 22
tempPin = 17

#temp sensor
tempSensor = Adafruit_DHT.DHT11

blinkDur = .1
blinkTime = 7

#for database
con = sql.connect('temperature.db')
cur = con.cursor()

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)

def blink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readTemp(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32

	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}'.format(temperature)
		humid = '{1:0.1f}'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')

	return tempFahr, humid

#Read temp and humidity
tempFahr, hum = readTemp(tempPin)

try:
	while True:
		time.sleep(60)
		temp, hum = readTemp(tempPin)
		cur.execute('INSERT INTO temperature values(?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'),temp,hum))
		con.commit()
		print "%-30s %-20s" %(temp, hum)

except KeyboardInterrupt:
	os.system('clear')
	con.close()
	GPIO.cleanup
