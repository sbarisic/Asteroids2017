import sfml
import sfml.sf
import sfml.graphics
import sfml.system
import sfml.window

from sfml import *

WIDTH = 800
HEIGHT = 600

class Rocket():
	def __init__(self):
		self.Shape = sf.CircleShape()

		return

	def draw(self, wind):
		wind.draw(self.Shape)
		return

def HandleEvents(W):
	for event in W.events:
		if event.type == sfml.window.Event.CLOSED:
			W.close()

	return

def CreateWindow():
	return sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "PyProject")

