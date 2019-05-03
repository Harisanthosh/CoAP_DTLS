from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from gpiozero import MCP3008
import time
import datetime
#from exampleresources import BasicResource

class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        pot = MCP3008(0)
        val = pot.value
        self.payload = "Hello From RPi3!!, Temp value is : %s" % (val)
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        pot = MCP3008(0)
        val = pot.value
        self.payload = "Temp value is : %s" % (val * 10000)
        return self

    def render_PUT(self, request):
        #self.edit_resource(request)
        if request.payload == "0":
            self.payload = "msg one sent!"
        else:
            self.payload = "default msg sent!"
        return self

    def render_POST(self, request):
        res = BasicResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res  
    
        #res = self.init_resource(request, BasicResource())
    
        #return self

    def render_DELETE(self, request):
        return True

class Separate(Resource):

    def __init__(self, name="Separate", coap_server=None):
        super(Separate, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        #self.payload = "Separate"
        self.max_age = 60
        pot = MCP3008(0)
        val = pot.value
        self.payload = "Hello From RPi3!!, Temp value is : %s" % (val)
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        return self, self.render_GET_separate

    def render_GET_separate(self, request):
        #time.sleep(5)
        pot = MCP3008(0)
        val = pot.value
        self.payload = "Temp value is : %s" % (val * 10000)
        return self

    def render_POST(self, request):
        return self, self.render_POST_separate

    def render_POST_separate(self, request):
        pot = MCP3008(0)
        val = pot.value
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.payload = "Trigering new Temp Measurement which is : %s at timestamp %s" % ((val * 10000), st)
        #self.payload = request.payload
        return self

    def render_PUT(self, request):
        return self, self.render_PUT_separate

    def render_PUT_separate(self, request):
        self.payload = request.payload
        return self

    def render_DELETE(self, request):
        return self, self.render_DELETE_separate

    def render_DELETE_separate(self, request):
        return True

class AdvancedResource(Resource):
    def __init__(self, name="Advanced"):
        super(AdvancedResource, self).__init__(name)
        #self.payload = "Advanced resource"
        pot = MCP3008(0)
        val = pot.value
        global currenttemp
        currenttemp = val
        self.payload = "Hello From RPi3!!, Temp value is : %s" % (val)
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET_advanced(self, request, response):
        #pot = MCP3008(0)
        #val = pot.value
        response.payload = "Temp value is : %s" % (currenttemp * 10000)
        response.max_age = 20
        response.code = defines.Codes.CONTENT.number
        return self, response

    def render_POST_advanced(self, request, response):
        pot = MCP3008(0)
        val = pot.value
        global currenttemp
        currenttemp = val
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #self.payload = "Trigering new Temp Measurement which is : %s at timestamp %s" % ((val * 10000), st)
        self.payload = request.payload
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Trigering new Temp Measurement which is : %s at timestamp %s" % ((val * 10000), st)
        response.code = defines.Codes.CREATED.number
        return self, response

    def render_PUT_advanced(self, request, response):
        self.payload = request.payload
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        #self.add_resource('temperature/', Separate())
        #self.add_resource('temperature/', BasicResource())
        self.add_resource('temperature/', AdvancedResource())

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

