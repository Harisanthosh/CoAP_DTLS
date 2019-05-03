from time import sleep
from gpiozero import LED
import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("ledTopic", hostname="192.168.137.46", port=1883)
print "%s %s" % (msg.topic, msg.payload)
led = LED(13)

val = msg.payload
print val
if val == "ON":
    print "Inside ON"
    led.on()
    sleep(5)
    led.off()
elif val == "OFF":
    print "Inside OFF"
    led.off()
else:
    print "Invalid command sent from MQTT Broker"


    

