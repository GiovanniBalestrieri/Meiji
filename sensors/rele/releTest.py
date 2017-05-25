import RPi.GPIO as GPIO
from time import sleep

# The script as below using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)

rele1 = 12
rele2=16
rele3 = 20
rele4=21
rele5=26
rele6 = 19
rele7=13
rele8 = 22


# Set relay pins as output
GPIO.setup(rele1, GPIO.OUT)
GPIO.setup(rele2, GPIO.OUT)
GPIO.setup(rele3, GPIO.OUT)
GPIO.setup(rele4, GPIO.OUT)

GPIO.setup(rele5, GPIO.OUT)
GPIO.setup(rele6, GPIO.OUT)
GPIO.setup(rele7, GPIO.OUT)
GPIO.setup(rele8, GPIO.OUT)

def fire(dt):
    # Turn all relays ON
    GPIO.output(rele1, GPIO.HIGH)
    sleep(dt)
    GPIO.output(rele2, GPIO.HIGH)
    sleep(dt)
    GPIO.output(rele3, GPIO.HIGH)
    sleep(dt)
    GPIO.output(rele4, GPIO.HIGH)
    sleep(dt)
    GPIO.output(rele5, GPIO.HIGH)
    sleep(dt)
    GPIO.output(rele6, GPIO.HIGH)
    sleep(dt)
    GPIO.output(rele7, GPIO.HIGH)
    sleep(dt)
    GPIO.output(rele8, GPIO.HIGH)
    sleep(2) 

while (True):
    
    # Turn all relays ON
    fire(0.5)
	# Turn all relays OFF
    GPIO.output(rele1, GPIO.LOW)
    GPIO.output(rele2, GPIO.LOW)
    GPIO.output(rele3, GPIO.LOW)
    GPIO.output(rele4, GPIO.LOW)   
    GPIO.output(rele5, GPIO.LOW)
    GPIO.output(rele6, GPIO.LOW)
    GPIO.output(rele7, GPIO.LOW)
    GPIO.output(rele8, GPIO.LOW)   
    sleep(5)
