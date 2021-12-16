import aubio
import crepe
import numpy as np
import pyaudio
import queue
import time

audioparams = {
	"FS": 44100,
	"channels": 1,
	"buffersize": 2048,
	"volume_thresh": 0.01}

class PitchValues(object):
	def __init__(self):
		# Initialize audio 
		# p = pyaudio.PyAudio()
		# self.q = queue.Queue()
		# self.stream = p.open(
		# 	format = pyaudio.paFloat32,
		# 	channels = audioparams["channels"],	# Mono
		# 	rate = audioparams["FS"],	# Sampling Rate
		# 	input = True,
		# 	frames_per_buffer = audioparams["buffersize"])	# Frame Size
		# time.sleep(1)

		self.YINdetector = aubio.pitch(
			"default", audioparams["buffersize"], audioparams["buffersize"], audioparams["FS"])
		self.YINdetector.set_unit("Hz")
		self.YINdetector.set_silence(-40)
	
	def handleYIN(self, samples):
		return self.YINdetector(samples)[0]

	def handleCREPE(self, samples):
		return crepe.predict(samples, audioparams["FS"], viterbi = True)

	def audioloop(self):

		while True:
			data = self.stream.read(
				audioparams["buffersize"]//2, exception_on_overflow = False)
			samples = np.fromstring(data, dtype=np.float32)

			pitchYIN = self.handleYIN(samples)
			pitchCREPE = self.handleCREPE(samples)

			# Compute the energy (volume) of the
			# current frame.
			volume = np.sum(samples**2)/len(samples) * 100

			if not pitchYIN or volume < audioparams["volume_thresh"]:
				continue

			self.q.put({"yin": pitchYIN, "crepe": pitchCREPE})

	def close(self):
		self.stream.stop_stream()
		self.stream.close()