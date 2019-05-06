from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from gpiozero import MCP3008
import time
import datetime
import sys
import json
import random
import paho.mqtt.publish as publish

class AdvancedResource(Resource):
    def __init__(self, name="Advanced"):
        super(AdvancedResource, self).__init__(name)
        #self.payload = "Advanced resource"
        #pot = MCP3008(0)
        val = random.randint(11,22)
        global currenttemp
        currenttemp = val
        self.payload = "Hello From RPi3!!, Temp value is : %s" % (val)
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET_advanced(self, request, response):
        #pot = MCP3008(0)
        #val = pot.value
        #response.payload = "Temp value is : %s" % (currenttemp * 10000)
	
	response.payload = json.dumps({"Temp" : "%s" %(currenttemp)})
        response.max_age = 20
        response.code = defines.Codes.CONTENT.number
        return self, response

    def render_POST_advanced(self, request, response):
        #pot = MCP3008(0)
        val = random.randint(10,30)
        global currenttemp
        
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #self.payload = "Trigering new Temp Measurement which is : %s at timestamp %s" % ((val * 10000), st)        
        unit = request.payload
        print "Request URI: %s" %(unit)
        if str(unit).strip() == "C":
            response.payload = json.dumps({"Response" : "Trigering new Temp Measurement using C: which is : %s at timestamp %s" % (val, st)})
            currenttemp = val
        elif str(unit).strip() == "F":
            val = (val * 9) / 5 + 32
            response.payload = json.dumps({"Response" : "Trigering new Temp Measurement using F: which is : %s at timestamp %s" % (val, st)})
            currenttemp = val
        elif str(unit).strip() == "K":
            val = val + 273.15
            response.payload = json.dumps({"Response" : "Trigering new Temp Measurement using K: which is : %s at timestamp %s" % (val, st)})
            currenttemp = val
        else:
            response.payload = json.dumps({"Response" : "Trigering new Temp Measurement using C: which is : %s at timestamp %s" % (val, st)})
            currenttemp = val
        self.payload = request.payload
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))        
        response.code = defines.Codes.CREATED.number
        return self, response

    def render_PUT_advanced(self, request, response):
        self.payload = request.payload
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = json.dumps({"Response" : "Publishing Temp Info from MQTT Broker - Rpi/Temperature at Host %s" %(sys.argv[1])})
        response.code = defines.Codes.CHANGED.number
        publish.single("Rpi/Temperature", str(currenttemp), hostname=str(sys.argv[1]))
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('temperature/', AdvancedResource(Resource))
        #self.add_resource('temperature/Kelvin', AdvancedResource(Resource))
        #self.add_resource('temperature/Farenheit', AdvancedResource(Resource))

def main():
    server = CoAPServer("0.0.0.0", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."

if __name__ == '__main__':
    main()

