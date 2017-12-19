import sfml
import sfml.sf
import sfml.graphics
import sfml.system
import sfml.window
import os
import zlib

from random import *
from math import *
from sfml import *
from sfml.sf import Keyboard as Keys, Clock as Clock

os.stat_float_times(False)

TARGET_FPS = 60

WIDTH = 1000
HEIGHT = 800

DEBUG = False
DEBUG_DIST = -1

NOCLIP = False

CONSOLE_FONT_SIZE = 22

LINEAR_DAMPENING = 0.8
ANGULAR_DAMPENING = 0.98

MAX_COLLISION_DIST = 50
MAX_COLLISION_DIST_SQ = MAX_COLLISION_DIST * MAX_COLLISION_DIST

def read_file_text(fname):
	f = open(fname, "r")
	content = f.read()
	f.close()
	return content

def compute_hash_int(data):
	# Because hash() is not deterministic, ugh
	return zlib.adler32(data.encode())

# Compute hash of a file as integer and store it in the file modification time, funky, eh?
def create_time_hash(fname):
	dta = read_file_text(fname)

	hsh = compute_hash_int(dta)
	os.utime(fname, (os.path.getatime(fname), hsh))
	return

def check_time_hash(fname):
	dta = read_file_text(fname)

	hsh1 = os.path.getmtime(fname)
	hsh2 = compute_hash_int(dta)
	return hsh1 == hsh2

# For data serialization
def to_str(val):
	if val == None:
		return "None"
	elif isinstance(val, str):
		return "\"{0}\"".format(val)

	return str(val)

def from_str(val):
	val = val.strip()

	if val == "None":
		return None
	elif val.startswith("\"") and val.endswith("\""):
		return val[1:-1]

	try:
		return int(val)
	except:
		return None

def getrootdir():
	return os.path.dirname(os.path.abspath(__file__))

def getfile(f):
	return os.path.join(getrootdir(), f)

def randchance(min, max):
	return float(randint(min, max)) / 100

def randchoice(c):
	shuffle(c)
	return c[0]

def lerp1(a, b, t):
	return a + (b - a) * t

def lerp2(a, b, t):
	return (lerp1(a[0], b[0], t), lerp1(a[1], b[1], t))

def lerp3(a, b, t):
	return (lerp1(a[0], b[0], t), lerp1(a[1], b[1], t), lerp1(a[2], b[2], t))

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
	S.outline_thickness = 2

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
	if NOCLIP:
		return False

	if vec_dist_sqr(a.position, b.position) - ((a.radius + b.radius) ** 2) <= 0:
		return True

	return False

def drawText(wind, position, size, text):
	if not hasattr(drawText, "textObject"):
		f = sf.Font.from_file(getfile("fonts/FantasqueSansMono-Regular.ttf"))

		drawText.textObject = sf.Text()
		drawText.textObject.font = f
		drawText.textObject.color = sf.Color.WHITE
		
	drawText.textObject.position = position
	drawText.textObject.character_size = size
	drawText.textObject.string = text
	wind.draw(drawText.textObject)
	return

def handleEvents(W, OnKey, OnText):
	for event in W.events:
		if event.type == sfml.window.Event.CLOSED:
			W.close()
		elif event == sf.Event.KEY_PRESSED or event == sf.Event.KEY_RELEASED:
			OnKey(event == sf.Event.KEY_PRESSED, event["code"])
		elif event == sf.Event.TEXT_ENTERED:
			OnText(event["unicode"])

	return

def createWindow(title):
	Ctx = sf.ContextSettings()
	Ctx.antialiasing_level = 8
	W = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), title, sf.Style.DEFAULT, Ctx)
	return W

class Shader():
	def __init__(self, fpath):
		self.Shader = sf.Shader.from_file(fragment = getfile(fpath))
		return

	def setparam(self, p, val):
		self.Shader.set_parameter(p, val)
		return

	def bind(self):
		sf.Shader.bind(self.Shader)
		return

	def unbind(self):
		sf.Shader.bind(None)
		return

class RT():
	def __init__(self):
		self.RT = sf.RenderTexture(WIDTH, HEIGHT)
		self.Icon = Icon(self.RT.texture)
		return

	def clear(self):
		self.RT.clear(graphics.Color.BLACK)
		return

	def display(self):
		self.RT.display()
		return

	def draw(self, wind, shdr = None):
		self.Icon.draw(wind, (0, 0), shdr)
		return

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
		Scale = 26 - ((level - 1) * 7)
		T = Scale * 0.25
		S = gen_rand_shape(S, 16, Scale - T, Scale + T)

		setup_shape(S)
		self.Shape = S

		self.radius = Scale + T
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
		S.outline_color = graphics.Color.BLUE
		self.Shape = S

		self.radius = Scale * 2
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

	TurnAmount = 0
	MoveAmount = 0
	NextShotTime = 0
	Lives = 4

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

		self.Debug = make_debug_shape(self.radius)

		return

	def draw(self, wind):
		draw_physics(self, wind)
		return

	def update(self, dt):
		calc_physics(self, dt, True)
		return


class Icon():
	def __init__(self, path, centered = False, scale = 1, color = None):
		self.centered = centered

		if isinstance(path, str):
			self.texture = sf.Texture.from_file(getfile(path))
		elif isinstance(path, sf.Texture):
			self.texture = path
			
		self.texture.smooth = True

		self.sprite = sf.Sprite(self.texture)
		self.sprite.scale((scale, scale))

		# color != None crashes /facepalm
		if isinstance(color, sf.Color):
			self.sprite.color = color

		return

	def draw(self, wind, pos, shdr = None):
		x = pos[0]
		y = pos[1]

		if self.centered:
			x = x - (self.texture.width / 2)
			y = y - (self.texture.height / 2)

		self.sprite.position = (x, y)

		states = graphics.RenderStates.DEFAULT
		if shdr != None:
			states.shader = shdr.Shader

		wind.draw(self.sprite, states)
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

class Config():
	cfgname = "data.cfg"
	dict = {}

	antitamper_success = False

	def __init__(self):
		self.antitamper_success = self.readcfg()
		return

	def remove(self, name, update_from_file = True):
		name = name.strip()
		if name in self.dict:
			del self.dict[name]

		if update_from_file:
			self.writecfg()

		return

	def set(self, name, val, update_from_file = True):
		self.dict[name.strip()] = val

		if update_from_file:
			self.writecfg()
		return val

	def get(self, name, default = None, update_from_file = True):
		if update_from_file:
			self.readcfg()

		return self.dict.get(name, default)

	def default(self, name, value):
		v = self.get(name, value)

		if not isinstance(v, type(value)):
			self.set(name, value)
		else:
			self.set(name, v)

		return self.get(name, None, False)

	def readcfg(self):
		# Make sure the file exists
		open(getfile(self.cfgname), "a").close()

		if not check_time_hash(getfile(self.cfgname)):
			return False

		f = open(getfile(self.cfgname), "r")
		lines =	f.readlines()
		f.close()

		for l in lines:
			kv = l.split("=")
			self.set(kv[0], from_str(kv[1]))

		return True

	def writecfg(self):
		# Ditto
		open(getfile(self.cfgname), "a").close()
		f = open(getfile(self.cfgname), "w")
		
		for k in self.dict:
			f.write("{0}={1}\n".format(k, to_str(self.dict[k])))

		f.close()
		create_time_hash(getfile(self.cfgname))
		return True
