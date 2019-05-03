from gpiozero import MCP3008

# Connect Temp sensor to MCP 3008 A0 port

pot = MCP3008(0)
val = pot.value
print pot.value
conv_val = float(val) / 1000.0
print "Temp in C :"
print conv_val

