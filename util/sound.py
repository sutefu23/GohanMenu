import config

if config.環境 == "開発":
	import FakeRPi.GPIO as GPIO
else:
	import RPi.GPIO as GPIO

import time

class SOUND:
	SOUNDER = 20 #GIOP NO.

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.SOUNDER, GPIO.OUT , initial = GPIO.LOW)

	def onRead(self):
		self.play(Hz = 960, wait = 0.2)

	def onFalse(self):
		self.play(Hz = 262, wait = 0.2)
		self.play(Hz = 262, wait = 0.5)
		
	def onError(self):
		self.play(Hz = 262, wait = 5)


	def play(self, Hz = 960 ,wait = 0.2 ):
		p = GPIO.PWM(self.SOUNDER ,1)
		p.ChangeFrequency(Hz)
		p.start(50)
		time.sleep(wait)
		p.stop()


	def __del__(self):
		GPIO.cleanup()
	
if __name__ == '__main__' :
		sound = SOUND()


