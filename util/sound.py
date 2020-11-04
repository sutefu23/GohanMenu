import os
import simpleaudio as sa
import time


class SOUND:
	def onRead(self):
		f = os.path.join(os.path.dirname(__file__), "read.wav")
		wave_obj = sa.WaveObject.from_wave_file(f)
		play_obj = wave_obj.play()
		#play_obj.wait_done()

	def onFalse(self):
		pass
		
	def onError(self):
		pass

if __name__ == '__main__' :
	sound = SOUND()
	sound.onRead()