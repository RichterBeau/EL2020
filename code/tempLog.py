import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import smtplib
import socket

text = ""

#SMTP variables
eFROM = "richter.beau16@gmail.com"
eTO = "6316455069@vtext.com"
Subject = "Temperature Warning"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)


redPin = 23
greenPin = 27
dataPin = 17

tempSensor = Adafruit_DHT.DHT11

blinkDur = .1
blinkTime = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)

def turnOn(pin):
    GPIO.output(pin,True)

def turnOff(pin):
    GPIO.output(pin,False)

def readF(dataPin):
    humidity, temperature = Adafruit_DHT.read_retry(tempSensor, dataPin)
    temperature = temperature * 9/5 + 32

    if humidity is not None and temperature is not None:
        tempFahr = '{0:0.1f}*F'.format(temperature)
        humid = '{0:1}%'.format(humidity)
    else:
        print('Error Reading Sensor')

    if temperature > 80 or temperature < 70:
        turnOn(redPin)
        turnOff(greenPin)
        text = "The temperature is " + tempFahr
        eMessage = 'Subject: {}\n\n{}'.format(Subject, text)
        server.login("richter.beau16@gmail.com", "mkvohzpjrvskfrec")
        server.sendmail(eFROM, eTO, eMessage)
        server.quit

    else:
        turnOn(greenPin)
        turnOff(redPin)

    return tempFahr,humid

try:
    with open("../log/templog.csv", "a") as log:
        while True:
                time.sleep(60)
                data = readF(dataPin)
                print (data)
                log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(data)))
            

except KeyboardInterrupt:
    os.system('clear')
    GPIO.cleanup()
