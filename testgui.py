import matplotlib
import matplotlib.backends.backend_agg as agg
import micbutton
import notevalues as nv
import numpy as np
import os
import pitchestimators
import pyaudio
import pygame
import pylab
#import struct
import threading as Thread
import time
from tkinter import *
from pygame.locals import *
from scipy.fftpack import fft
matplotlib.use("Agg")

# Initialize pygame
pygame.init()
pygame.font.init()
screenWidth, screenHeight = 1000, 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
zIcon = pygame.image.load('Graphics/zicon.ico')
pygame.display.set_icon(zIcon)
pygame.display.set_caption('Pitch Tracking Comparison')
clock = pygame.time.Clock()

# Background Image
bg = pygame.image.load('Graphics/background.png')

# Set text fonts
fontTitle = pygame.font.SysFont('Helvetica Neue', 55) # y-padding 40
fontf0 = pygame.font.SysFont('Helvetica Neue', 40)
fontOther = pygame.font.SysFont('Helvetica Neue', 34)

pe = pitchestimators.PitchValues()

audioparams = {
	"FS": 44100,
	"channels": 1,
	"buffersize": 2048,
	"volume_thresh": 0.01}

p = pyaudio.PyAudio()
stream = p.open(
	format = pyaudio.paFloat32,
	channels = audioparams["channels"],
	rate = audioparams["FS"],
	input = True,
	output = True,
	frames_per_buffer = audioparams["buffersize"])

global is_off

# Set up matplotlib
fig = pylab.figure(figsize = [6.3, 2], dpi = 100)

# Variable plotting
wf_samp  = np.arange(0, 2 * audioparams["buffersize"], 2) #from 0 to 4096, step size 2
print(np.shape(wf_samp))
#spec_freq = np.linspace(0, FS, FRAME_SIZE)

ax = fig.gca()
print(np.shape(np.random.rand(audioparams["buffersize"])))
line, = ax.plot(wf_samp, np.random.rand(audioparams["buffersize"]), '_', lw = 2)
ax.set_ylim(-1, 1)
ax.set_xlim(0, audioparams["buffersize"])
ax.plot([1, 2, 4])

f0_val_yin = 17792.13
note_val_yin = 'A' + u'\u266f' + '/' + 'B' + u'\u266d'
f0_val_crepe = 17798.55
note_val_crepe = 'A' + u'\u266f' + '/' + 'B' + u'\u266d'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKRED = (127, 0, 0)

def static_text():
	screenTitle = fontTitle.render("PITCH TRACKING COMPARISON", True, WHITE)
	titleRect = screenTitle.get_rect(center = (screenWidth/2, screenHeight - 750))
	f0Title = fontf0.render("f" + u'\u2080', True, WHITE)
	noteTitle = fontOther.render("Note (Octave)", True, WHITE)
	yinTitle = fontOther.render("YIN:", True, WHITE)
	crepeTitle = fontOther.render("CREPE:", True, WHITE)

	screen.blit(screenTitle, titleRect)
	screen.blit(f0Title, (560, 310))
	screen.blit(noteTitle, (685, 315))
	screen.blit(yinTitle, (100, 400))
	screen.blit(crepeTitle, (100, 600))

	tableLine1 = pygame.draw.rect(screen, WHITE, (666, 309, 6, 400))
	tableLine1 = pygame.draw.rect(screen, WHITE, (500, 370, 400, 6))
	tableLine1 = pygame.draw.rect(screen, WHITE, (500, 540, 400, 6))

def update_text():

	f0_val_yin_update = fontOther.render('{0:.2f}'.format(f0_val_yin), True, WHITE)
	note_yin_update = fontOther.render(str(note_val_yin), True, WHITE)
	f0_val_crepe_update = fontOther.render('{0:.2f}'.format(f0_val_crepe), True, WHITE)
	note_crepe_update = fontOther.render(str(note_val_crepe), True, WHITE)

	screen.blit(f0_val_yin_update, (500, 400))
	screen.blit(note_yin_update, (714, 400))
	screen.blit(f0_val_crepe_update, (500, 600))
	screen.blit(note_crepe_update, (714, 600))

def mic_Button():


	def switch():
		global is_on
		if is_on:
			micOn_btn.config(image = micOff)
			is_on = False
		else:
			micOn_btn.config(image = micOn)
			is_on = True

	# Load button images
	micOn = pygame.image.load('Graphics/micOn.png').convert_alpha()
	micOff = pygame.image.load('Graphics/micOff.png').convert_alpha()
	#micOn_btn = micbutton.MicButton(100, 200, micOn, 0.8, command = switch)
	#micOff_btn = micbutton.MicButton(100, 200, micOff, 0.8, command = switch)

	screen.blit(micOn, (50, 100))

def tracking_Circles():
	# Red
	#circ_R = pygame.draw.circle(screen, RED, (365, 421), 100)
	#underCirc_R = pygame.draw.circle(screen, DARKRED, (365, 421), 160)
	circ_R = pygame.image.load('Graphics/offcirclesmall.png')
	underCirc_R = pygame.image.load('Graphics/offcirclebig.png')

	# Green
	#circ_G = pygame.draw.circle(screen, GREEN, (365, 621), 100)
	#underCirc_G = pygame.draw.circle(screen, GREEN, (365, 621), 160)
	circ_G = pygame.image.load('Graphics/goodcirclesmall.png')
	underCirc_G = pygame.image.load('Graphics/goodcirclebig.png')

	screen.blit(underCirc_R, (287, 336))
	screen.blit(circ_R, (287, 336))
	screen.blit(underCirc_G, (287, 540))
	screen.blit(circ_G, (287, 540))

running = True
while running:
	screen.fill((BLACK))
	screen.blit(bg, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Binary Data
	data = stream.read(audioparams["buffersize"], 
		exception_on_overflow = False)
	# Convert data to integers
	samples = np.fromstring(data, dtype = np.float32)
	#data_int = struct.unpack(str(2 * audioparams['buffersize']) + 'B', data)
	# np array, offset by 128

	f0_val_yin = pe.handleYIN(samples)
	note_val_yin = nv.get_note_info(f0_val_yin)
	f0_val_crepe = pe.handleCREPE(samples)
	note_val_crepe = nv.get_note_info(f0_val_crepe)
	#data_np = np.array(samples, dtype = 'b') + 128

	#print("min: %d, max: %d" % (min(data_int), max(data_int)))
	line.set_ydata(samples)

	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()

	size = canvas.get_width_height()
	surf = pygame.image.fromstring(raw_data, size, "RGB")
	screen.blit(surf, (270, 100))

	static_text()
	update_text()
	mic_Button()
	tracking_Circles()
	pygame.display.update()
	clock.tick(60)

stream.stop_stream()
stream.close()
