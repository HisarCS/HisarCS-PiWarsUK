import time
import gaugette.gpio
import gaugette.rotary_encoder

gpio = gaugette.gpio.GPIO()
#front right connected to BOARD pin 5, 7
fr = gaugette.rotary_encoder.RotaryEncoder(gpio, 7, 9)
#front left connected to BOARD pin 8, 10
fl = gaugette.rotary_encoder.RotaryEncoder(gpio, 15, 16)
#back right connected to BOARD pin 13, 15
br = gaugette.rotary_encoder.RotaryEncoder(gpio, 2, 3)
#back left connected to BOARD pin 11, 12
bl = gaugette.rotary_encoder.RotaryEncoder(gpio, 0, 1)

#start all encoders
ur.start()
ul.start()
br.start()
bl.start()

while True:
	#get the deltas of all encoders
	deltaa = ur.get_cycles()
	deltab = ul.get_cycles()
	deltac = br.get_cycles()
	deltad = bl.get_cycles()
	#print deltas of all encoders
	print("d: ", deltaa, deltab, deltac, deltad)
	time.sleep(0.1)
