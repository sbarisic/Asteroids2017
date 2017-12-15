import sfml
import sfml.sf
import sfml.graphics
import sfml.system
import sfml.window
import os

from random import *
from math import *
from sfml import *
from sfml.sf import Keyboard as Keys, Clock as Clock

TARGET_FPS = 60

WIDTH = 1000
HEIGHT = 800
DEBUG = False

LINEAR_DAMPENING = 0.8
ANGULAR_DAMPENING = 0.98

MAX_COLLISION_DIST = 50
MAX_COLLISION_DIST_SQ = MAX_COLLISION_DIST * MAX_COLLISION_DIST

textObject = None

def getrootdir():
	return os.path.dirname(os.path.abspath(__file__))

def getfile(f):
	return os.path.join(getrootdir(), f)

def randchance(min, max):
	return float(randint(min, max)) / 100

def randchoice(c):
	shuffle(c)
	return c[0]

def to_rad(deg):
	return pi / 180 * deg

def vec_mul_scalar(s, vec):
	return (vec[0] * s, vec[1] * s)

def vec_sub_vec(a, b):
	return (a[0] - b[0], a[1] - b[1])

def vec_add_vec(a, b):
	return (a[0] + b[0], a[1] + b[1])

def vec_rand(lower, upper):
	return (randint(lower[0], upper[0]), randint(lower[1], upper[1]))

def vec_normal(angle):
	return (cos(angle), sin(angle))

def vec_mag_fast(vec):
	return (vec[0] ** 2) + (vec[1] ** 2)

def vec_mag(vec):
	return sqrt(vec_mag_fast(vec))

def vec_setx(vec, x):
	return (x, vec[1])

def vec_sety(vec, y):
	return (vec[0], y)

def vec_dist(a, b):
	return vec_mag(vec_sub_vec(a, b))

def vec_dist_sqr(a, b):
	return vec_mag_fast(vec_sub_vec(a, b))

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

	if self.position[0] + self.radius < 0:
		self.position = vec_setx(self.position, WIDTH + self.radius)

	elif self.position[0] - self.radius > WIDTH:
		self.position = vec_setx(self.position, -self.radius)

	if self.position[1] + self.radius < 0:
		self.position = vec_sety(self.position, HEIGHT + self.radius)

	elif self.position[1] - self.radius > HEIGHT:
		self.position = vec_sety(self.position, - self.radius)

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

def gen_rand_shape(s, point_cnt, lower_inc, upper_inc):
	s.point_count = point_cnt

	angle_seg = (2 * pi) / point_cnt
	for i in range(point_cnt):
		angle = angle_seg * i
		distance = randint(int(lower_inc), int(upper_inc))

		vec = vec_mul_scalar(distance, vec_normal(angle))
		s.set_point(i, vec)

		pass

	return s

def collides(a, b):
	if vec_dist_sqr(a.position, b.position) - ((a.radius + b.radius) ** 2) <= 0:
		return True

	return False

def drawText(wind, position, size, text):
	global textObject

	if textObject == None:
		f = sf.Font.from_file(getfile("fonts/FantasqueSansMono-Regular.ttf"))

		textObject = sf.Text()
		textObject.font = f
		textObject.color = sf.Color.WHITE
		
	textObject.position = position
	textObject.character_size = size
	textObject.string = text
	wind.draw(textObject)
	return

def handleEvents(W, OnKey):
	for event in W.events:
		if event.type == sfml.window.Event.CLOSED:
			W.close()
		elif event == sf.Event.KEY_PRESSED or event == sf.Event.KEY_RELEASED:
			OnKey(event == sf.Event.KEY_PRESSED, event["code"])

	return

def createWindow(title):
	Ctx = sf.ContextSettings()
	Ctx.antialiasing_level = 8
	W = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), title, sf.Style.DEFAULT, Ctx)
	return W

class Asteroid():
	position = (0, 0)
	angle = 0

	linear_vel = (0, 0)
	angular_vel = 0

	radius = 0
	level = 0
	score = 0

	def __init__(self, level):
		S = sf.ConvexShape()

		self.score = int(19 * (level ** 1.465))

		self.level = level
		Scale = 26 - ((level - 1) * 10)
		T = Scale * 0.25
		S = gen_rand_shape(S, 16, Scale - T, Scale + T)

		setup_shape(S)
		self.Shape = S

		self.radius = Scale + T
		if DEBUG:
			self.Debug = make_debug_shape(self.radius)

		return

	def draw(self, wind):
		draw_physics(self, wind)
		return

	def update(self, dt):
		calc_physics(self, dt, False)
		return

class Bullet():
	position = (0, 0)
	angle = 0

	linear_vel = (0, 0)
	angular_vel = 0

	end_life = 0
	radius = 0

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

		self.radius = Scale * 2
		if DEBUG:
			self.Debug = make_debug_shape(self.radius)

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

	radius = 0

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
		self.radius = Scale * 2

		if DEBUG:
			self.Debug = make_debug_shape(self.radius)

		return

	def draw(self, wind):
		draw_physics(self, wind)
		return

	def update(self, dt):
		calc_physics(self, dt, True)
		return


class Icon():
	def __init__(self, path, centered = False):
		self.centered = centered

		self.texture = sf.Texture.from_file(getfile(path))
		self.texture.smooth = True

		self.sprite = sf.Sprite(self.texture)
		return

	def draw(self, wind, pos):
		x = pos[0]
		y = pos[1]

		if self.centered:
			x = x - (self.texture.width / 2)
			y = y - (self.texture.height / 2)

		self.sprite.position = (x, y)
		wind.draw(self.sprite)
		return

class Sfx():
	def __init__(self, path):
		self.sound_buffer = sf.SoundBuffer.from_file(getfile(path))
		self.sound = sf.Sound(self.sound_buffer)

		return

	def play(self):
		self.sound.pitch = randchance(90, 110)
		self.sound.play()
		return

	def begin_play(self):
		self.sound.loop = True
		self.sound.pitch = 1
		self.sound.play()
		return

	def end_play(self):
		self.sound.stop()
		self.sound.loop = False
		return