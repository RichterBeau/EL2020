import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os

redPin = 27
tempPin = 17
buttonPin = 26

tempSensor = Adafruit_DHT.DHT11

blinkDur = .1
blinkTime = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def oneBlink(pin):
    GPIO.output(pin,True)
    time.sleep(blinkDur)
    GPIO.output(pin,False)
    time.sleep(blinkDur)

def readF(tempPin):
    humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
    temperature = temperature * 9/5 + 32
    if humidity is not None and temperature is not None:
        tempFahr = '{0:0.1f}*F'.format(temperature)
    else:
        print('Error Reading Sensor')
    return tempFahr

try:
    with open("../log/templog.csv", "a") as log:
        while True:
            input_state = GPIO.input(buttonPin)
            if input_state == True:
                for i in range (blinkTime):
                    oneBlink(redPin)
                time.sleep(.2)
                data = readF(tempPin)
                print (data)
                log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(data)))
            

except KeyboardInterrupt:
    os.system('clear')
    GPIO.cleanup()
