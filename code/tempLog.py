import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import smtplib
import socket
import sqlite3 as sql

text = ""

#SMTP variables
eFROM = "richter.beau16@gmail.com"
eTO = "6316455069@vtext.com"
Subject = "Temperature Warning"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

#Connect to the database
con = sql.connect('../log/tempLog.db')
cur = con.cursor()

#Set initial cehckbit to 0
eChk = 0

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

def tempAlert(tempFahr):
    if eChk == 0:
        turnOn(redPin)
        turnOff(greenPin)
        text = "The Temperature is " + tempFahr
        eMessage = 'Subject: {}\n\n{}'.format(Subject, text)
        server.login("richter.beau16@gmail.com", "mkvohzpjrvskfrec")
        server.sendmail(eFROM, eTO, eMessage)
        server.quit
        eChek = 1


def readF(dataPin):
    humidity, temperature = Adafruit_DHT.read_retry(tempSensor, dataPin)
    temperature = temperature * 9/5 + 32

    if humidity is not None and temperature is not None:
        tempFahr = '{0:0.1f}'.format(temperature)
        humid = '{0:1}'.format(humidity)
    else:
        print('Error Reading Sensor')

    if temperature > 80 or temperature < 70:
        tempAlert(tempFahr)
    else:
        turnOn(greenPin)
        turnOff(redPin)
        eChek = 0

    return tempFahr,humid

try:
    with open("../log/templog.csv", "a") as log:
        while True:
                time.sleep(5)
                data = readF(dataPin)
                print (data)
                temp,hum = readF(dataPin)

                cur.execute('INSERT INTO templog values(?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'), temp, hum))
                con.commit()
                table = con.execute("select * from tempLog")
                os.system('clear')
                
                print "%-30s %-20s %-20s" %("Date/Time", "Temp", "Humidity")
                for row in table:
                    print "%-30s %-20s %-20s" %(row[0], row[1], row[2])
    

              #  log.write("{0},{1}\n".foermat(time.strftime("%Y-%m-%d %H:%M:%S"),str(data)))
            

except KeyboardInterrupt:
    os.system('clear')
    GPIO.cleanup()
