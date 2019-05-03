from time import sleep
from gpiozero import LED

led = LED(13)

x = 0;

print "Starting the blink !"
while x < 5:
    led.on()
    sleep(1)
    led.off()
    x = x + 1

print "Stopping the blink !"


