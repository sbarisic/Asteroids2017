from turtle import *
from random import *
import math

verts = []
lines = []
scale = 150

def rot_vec(v, a):
	s = math.sin((math.pi / 180) * a)
	c = math.cos((math.pi / 180) * a)
	return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)

def rand_color(color_scale = 0.5):
	return (float(randint(0, 255)) / 255 * color_scale, float(randint(0, 255)) / 255 * color_scale, float(randint(0, 255)) / 255 * color_scale)

obj_file = open("C:\\Users\\Carpmanium\\Desktop\\stuff\\name.obj", "r")
for line in obj_file:
	cmd = line.split(" ")
	if cmd[0] == "v":
		verts.append((float(cmd[1]) * scale, float(cmd[3]) * scale))
	elif cmd[0] == "l":
		lines.append((int(cmd[1]) - 1, int(cmd[2]) - 1))


tracer(0, 0)
penup()
for l in lines:
	ang = 90
	start = rot_vec(verts[l[0]], ang)
	end = rot_vec(verts[l[1]], ang)

	pencolor(rand_color())

	goto(start)
	pendown()
	goto(end)
	penup()
	update()

while True:
	pass