import sfml
import sfml.sf
import sfml.graphics
import sfml.system
import sfml.window

from sfml import *
from sfml.sf import Keyboard as Keys, Clock as Clock

TARGET_FPS = 60

WIDTH = 1000
HEIGHT = 800
DEBUG = False

LINEAR_DAMPENING = 0.8
ANGULAR_DAMPENING = 0.5

def vec_mul_scalar(s, vec):
	return (vec[0] * s, vec[1] * s)

def vec_sub_vec(a, b):
	return (a[0] - b[0], a[1] - b[1])

def vec_add_vec(a, b):
	return (a[0] + b[0], a[1] + b[1])

def setup_shape(S):
	S.outline_color = sf.Color.WHITE
	S.fill_color = sf.Color.TRANSPARENT
	S.outline_thickness = 1

def make_debug_shape(R):
	D = sf.CircleShape()
	setup_shape(D)
	D.outline_color = sf.Color.RED

	D.radius = R
	D.origin = (R, R)
	return D

def calc_physics(self, dt, dampen):
	if dampen:
		self.linear_vel = vec_sub_vec(self.linear_vel, vec_mul_scalar(LINEAR_DAMPENING * dt, self.linear_vel))
		self.angular_vel = self.angular_vel - (self.angular_vel * ANGULAR_DAMPENING * dt)

	self.position = vec_add_vec(self.position, self.linear_vel)
	self.angle = self.angle + self.angular_vel
	return

def draw_physics(self, wind):
	self.Shape.position = self.position
	self.Shape.rotation = 180 + self.angle
	wind.draw(self.Shape)

	if DEBUG:
		self.Debug.position = self.Shape.position
		wind.draw(self.Debug)

	return


class Bullet():
	position = (0, 0)
	angle = 0

	linear_vel = (0, 0)
	angular_vel = 0

	def __init__(self):
		S = sf.ConvexShape()
		S.point_count = 4

		Scale = 3
		T = 0.25 / Scale

		S.set_point(0, vec_mul_scalar(Scale, (-T, 2)))
		S.set_point(1, vec_mul_scalar(Scale, (T, 2)))
		S.set_point(2, vec_mul_scalar(Scale, (T, -2)))
		S.set_point(3, vec_mul_scalar(Scale, (-T, -2)))

		setup_shape(S)
		self.Shape = S

		if DEBUG:
			self.Debug = make_debug_shape(Scale * 2)

		return

	def draw(self, wind):
		draw_physics(self, wind)
		return

	def update(self, dt):
		calc_physics(self, dt, False)
		return


class Rocket():
	position = (0, 0)
	angle = 0

	linear_vel = (0, 0)
	angular_vel = 0

	def __init__(self):
		S = sf.ConvexShape()
		S.point_count = 4

		Scale = 5
		S.set_point(0, vec_mul_scalar(Scale, (-2, -2)))
		S.set_point(1, vec_mul_scalar(Scale, (0, 2)))
		S.set_point(2, vec_mul_scalar(Scale, (2, -2)))
		S.set_point(3, vec_mul_scalar(Scale, (0, -1)))

		setup_shape(S)
		self.Shape = S

		if DEBUG:
			self.Debug = make_debug_shape(Scale * 2)

		return

	def draw(self, wind):
		draw_physics(self, wind)
		return

	def update(self, dt):
		calc_physics(self, dt, True)
		return

def HandleEvents(W, OnKey):
	for event in W.events:
		if event.type == sfml.window.Event.CLOSED:
			W.close()
		elif event == sf.Event.KEY_PRESSED or event == sf.Event.KEY_RELEASED:
			OnKey(event == sf.Event.KEY_PRESSED, event["code"])

	return

def CreateWindow():
	Ctx = sf.ContextSettings()
	Ctx.antialiasing_level = 8
	W = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "PyProject", sf.Style.DEFAULT, Ctx)
	return W
