#!/usr/bin/python

import subprocess,wave,multiprocessing,time

import RPi.GPIO as gpio
import numpy

LED_PIN = 2
WAV_FILENAME = "tmp.wav"
UPDATE_PERIOD = 1.0/1000 #Hz
THRESHOLD = 50 #2**14

START_LOCK = multiprocessing.Lock()

def led_io():
	START_LOCK.acquire()
	wav_file = wave.open(WAV_FILENAME)
	nchannels, sampwidth, framerate, nframes, comptype, compname = wav_file.getparams()

	frames  = int(numpy.ceil(UPDATE_PERIOD*framerate))
	value = True

	rms_values = numpy.empty(nframes/frames)
	#while (wav_file.tell() < nframes):
	for i in range(nframes/frames):
		raw_data = wav_file.readframes(frames)
		data = numpy.fromstring(raw_data,dtype=numpy.int16)
		
		rms = numpy.mean(data**2)**0.5
		#print rms
		rms_values[i] = rms
	
	values = rms_values > THRESHOLD 

	START_LOCK.release()
	timestamp = time.time()
	for v in values:
		gpio.output(LED_PIN,bool(v))	
		sleep_time = UPDATE_PERIOD - (time.time() - timestamp)
		#print sleep_time
		time.sleep(sleep_time)
		timestamp = time.time()

	wav_file.close()

def say(text):
	subprocess.check_output([
				'pico2wave',
				'-w',WAV_FILENAME,
				'-l','en-GB',
				text
				])

	led_process = multiprocessing.Process(target=led_io)

	led_process.start()
	time.sleep(0.1)
	START_LOCK.acquire()
	subprocess.check_output([
				'aplay',
				WAV_FILENAME	
				])
	led_process.join()

gpio.setmode(gpio.BCM)
gpio.setup(LED_PIN, gpio.OUT)

with open("henry5_prologue.txt","r") as henry5_prologue: say(henry5_prologue.read())

