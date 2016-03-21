#!/usr/bin/python
import time
import pyttsx
import RPi.GPIO as gpio

LED_PIN = 2

gpio.setmode(gpio.BCM)
gpio.setup(LED_PIN, gpio.OUT)

def startWord(name,location,length):
	gpio.output(LED_PIN,True)
	print "started %s"%length
	time.sleep(length*0.1)
	gpio.output(LED_PIN,False)

speech = pyttsx.init("espeak",debug=True)

speech.setProperty('rate', 120)
speech.connect('started-word', startWord)

with open("henry5_prologue.txt","r") as henry5_prologue: 
	for line in henry5_prologue: 
		#while speech.isBusy(): pass
		speech.say(line)
		speech.runAndWait()
