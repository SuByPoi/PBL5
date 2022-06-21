import RPi.GPIO as GPIO

pir_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)


mainRoom_pin = 25
div = 0

GPIO.setup(mainRoom_pin, GPIO.OUT)
lastStage = 0
while True:
    print(GPIO.input(pir_pin))
    if(GPIO.input(pir_pin) == 1 and GPIO.input(pir_pin) != lastStage):
        if(div % 2):
            GPIO.output(mainRoom_pin, GPIO.HIGH)
        else:
            GPIO.output(mainRoom_pin, GPIO.LOW)
        div = div + 1
    lastStage = lastStage + 1
    