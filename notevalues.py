import numpy as np
from pitchestimators import PitchValues
from threading import Thread

freqs = np.array([
	16.35, 17.32, 18.35, 19.45, 20.6, 21.83, 
	23.12, 24.5, 25.96, 27.5, 29.14, 30.87, 
	32.7, 34.65, 36.71, 38.89, 41.20, 43.65, 
	46.25, 49, 51.91, 55, 58.27, 61.74, 
	65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 
	92.5, 98, 103.83, 110, 116.54, 123.47, 
	130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 
	185, 196, 207.65, 220, 233.08, 246.94, 
	261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 
	369.99, 392, 415.3, 440,466.16, 493.88, 
	523.25, 554.37, 587.33, 622.25, 659.26, 698.46,
	739.99, 783.99, 830.61, 880, 932.33, 987.77, 
	1046.5, 1108.73, 1174.66, 1244.51, 1318.51, 
	1396.91, 1479.98, 1567.98, 1661.22, 1760, 1864.66, 
	1975.53, 2093, 2217.46, 2349.32, 2489.02, 2637.02, 
	2793.83, 2959.96, 3135.96, 3322.44, 3520, 3729.31, 
	3951.07, 4186.01, 4434.92, 4698.64, 4978.03, 5274.04, 
	5587.65, 5919.91, 6271.93, 6644.88, 7040, 7458.62, 
	7902.13, 8372.02, 8869.84, 9397.27, 9956.06, 10548.08, 
	11175.3, 11839.82, 12543.86, 13289.75, 14080, 14917.24, 
	15804.26, 16744.04, 17739.69, 18794.55, 19912.13])

STR_2_UNICODE_NOTE = {
	'C': 0,
	'C' + u'\u266f' + '/' + 'D' + u'\u266d': 1,
	'D': 2,
	'D' + u'\u266f' + '/' + 'E' + u'\u266d': 3,
	'E': 4,
	'F': 5,
	'F' + u'\u266f' + '/' + 'G' + u'\u266d': 6,
	'G': 7,
	'G' + u'\u266f' + '/' + 'A' + u'\u266d': 8,
	'A': 9,
	'A' + u'\u266f' + '/' + 'B' + u'\u266d': 10,
	'B': 11}

NOTES_IN_OCT = 12

def get_note_info(pitch):
	fdiff = np.abs(freqs - pitch)
	idx   = np.argmin(fdiff)
	note_num = idx % NOTES_IN_OCT
	octave   = idx // NOTES_IN_OCT
	flipped = {
		v: k for k, v in STR_2_UNICODE_NOTE.items()}
	return flipped[note_num] + " (%s)"%octave

def main():
	pv = PitchValues()
	t = Thread(target=pv.audioloop)
	t.daemon = True
	t.start()

	try:
		while True:
			if not pv.q.empty():
				info = pv.q.get()
				yp = info["yin"]
				cp = info["crepe"]
				print("Yin estimate:", get_note_info(yp))
				print("Crepe estimate:", get_note_info(cp))
	except KeyboardInterrupt:
		print("closing stream")

		pv.close()

if __name__ == '__main__':
	main()