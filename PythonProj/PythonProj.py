import clr
import sys

clr.AddReference("System")
clr.AddReference("System.Reflection")
clr.AddReference("System.Drawing")
clr.AddReference("System.IO")
clr.AddReference("System.Numerics")
from System import *
from System.Numerics import *

clr.AddReference("Utils")
from Utils import *

# Initialize important(tm) stuff
Utility.Init()

'''
class Texture:
	Width = 0
	Height = 0
	Pixels = []

	def __init__(self, filename):
		Console.WriteLine("Loading {0}", filename)
		Bmp = Drawing.Bitmap(filename)
		self.Width = int(Bmp.Width)
		self.Height = int(Bmp.Height)

		for i in range(self.Width * self.Height):
			x = i % self.Width
			y = i / self.Width
			self.Pixels.append(Pixel(Bmp.GetPixel(x, y)))

		return

	def Get(self, u, v):
		x = int(u * self.Width)
		y = int((1.0 - v) * self.Height)

		if x < 0:
			x = 0
		if x >= self.Width:
			x = self.Width - 1
		if y < 0:
			y = 0
		if y >= self.Height:
			y = self.Height - 1

		P = self.Pixels[y * self.Width + x]
		return (P.R, P.G, P.B)
'''


class ModelLoader:
	@staticmethod
	def Load(filename, swapyz=False):
		vertices = []
		normals = []
		texcoords = []
		faces = []
		textures = []

		Console.WriteLine("Loading {0}", filename)

		for line in open(filename, "r"):
			if line.startswith("#"): continue
			values = line.split()
			if not values: continue

			if values[0] == "usemtl":
				if values[1] not in textures:
					textures.append(String(values[1]).replace("*", "#"))
			elif values[0] in ("v", "vn"):
				v = map(float, values[1:4])
				if swapyz:
					v = v[0], v[2], v[1]

				v = list(v)
				if values[0] == "v":
					vertices.append(v)
				else:
					normals.append(v)
			elif values[0] == "vt":
				texcoords.append(list(map(float, values[1:3])))
			elif values[0] == "f":
				face = []
				texcoord = []
				norms = []

				vals = values[1:]
				if (len(vals) != 3):
					return

				for v in vals:
					w = v.split("/")
					face.append(int(w[0]))

					if len(w) >= 2 and len(w[1]) > 0:
						texcoord.append(int(w[1]))
					else:
						texcoord.append(0)

					if len(w) >= 3 and len(w[2]) > 0:
						norms.append(int(w[2]))
					else:
						norms.append(0)

				faces.append((face, norms, texcoord))

		return (vertices, normals, texcoords, faces, textures)


class Renderer:
	Window = None
	
	@staticmethod
	def Init():
		Renderer.Window = RenderWindow()
		return
	
	@staticmethod
	def Point(x, y, rgb):
		Renderer.Window.PutPixel(x, y, rgb[0], rgb[1], rgb[2])
		return

	@staticmethod
	def Line(start, end, rgb):
		#x0 = int((start[0] + 1) * Renderer.Window.Width / 2)
		#y0 = int((start[1] + 1) * Renderer.Window.Height / 2)
		#x1 = int((end[0] + 1) * Renderer.Window.Width / 2)
		#y1 = int((end[1] + 1) * Renderer.Window.Height / 2)
		x0 = int(start[0])
		y0 = int(start[1])
		x1 = int(end[0])
		y1 = int(end[1])
		steep = False

		if (abs(x0 - x1) < abs(y0 - y1)):
			x0, y0 = y0, x0
			x1, y1 = y1, x1
			steep = True
		
		if (x0 > x1):
			x0, x1 = x1, x0
			y0, y1 = y1, y0

		dx = x1 - x0
		dy = y1 - y0
		derror2 = abs(dy) * 2
		error2 = 0
		y = y0

		for x in range(x0, x1):
			if (steep):
				Renderer.Point(y, x, rgb)
			else:
				Renderer.Point(x, y, rgb)

			error2 += derror2
			if (error2 > dx):
				y += 1 if (y1 > y0) else -1
				error2 -= dx * 2
		return

	@staticmethod
	def Rectangle(a, b, c, d, color):
		Renderer.Line(a, b, color)
		Renderer.Line(b, c, color)
		Renderer.Line(c, d, color)
		Renderer.Line(d, a, color)
		return

	@staticmethod
	def Triangle(a, b, c, tex):
		W = Renderer.Window.Width
		H = Renderer.Window.Height

		a = (int(a[0] * W), int(a[1] * H))
		b = (int(b[0] * W), int(b[1] * H))
		c = (int(c[0] * W), int(c[1] * H))

		xmin, ymin, xmax, ymax = bbox(a, b, c)
		if xmax < 0 or ymax < 0 or xmin == xmax or ymin == ymax:
			return

		if xmin >= Renderer.Window.Width or ymin >= Renderer.Window.Height:
			return
		
		for pyd in range(ymax - ymin + 1):
			for pxd in range(xmax - xmin + 1):
				p = (xmin + pxd, ymin + pyd)
				barycentric_screen = barycentric(a, b, c, p)

				if barycentric_screen[0] < 0 or barycentric_screen[1] < 0 or barycentric_screen[2] < 0:
					continue

				Renderer.Point(p[0], p[1], tex.Get(barycentric_screen[0], barycentric_screen[1]))

		if False:
			Renderer.Line(a, b, (255, 0, 0))
			Renderer.Line(b, c, (0, 255, 0))
			Renderer.Line(c, a, (0, 0, 255))

		#ra, rb, rc, rd, rcolor = ((xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin), (100, 100, 100))
		#Renderer.Rectangle(ra, rb, rc, rd, rcolor)
		return
	
def bbox(a, b, c):
	xmax = max(a[0], max(b[0], c[0]))
	ymax = max(a[1], max(b[1], c[1]))

	xmin = min(a[0], min(b[0], c[0]))
	ymin = min(a[1], min(b[1], c[1]))
	return xmin, ymin, xmax, ymax

def barycentric(a, b, c, p):
	U = Vector3.Cross(Vector3(c[0] - a[0], b[0] - a[0], a[0] - p[0]), Vector3(c[1] - a[1], b[1] - a[1], a[1] - p[1]))

	if abs(U.Z) < 1:
		return (-1, 1, 1)
	
	return (1.0 - (U.X + U.Y) / U.Z, U.Y / U.Z, U.X / U.Z)

rnd = Random()
def random_byte():
	return rnd.Next(0, 256)

def random_color():
	return (random_byte(), random_byte(), random_byte())

def pymain():
	#mdl = "models\\level.obj"
	mdl = "models\\diablo3_pose\diablo3_pose.obj"
	#mdl = "models\\teapot.obj"
	#mdl = "models\\gourd.obj"

	vertices, normals, texcoords, faces, textures = ModelLoader.Load(mdl)
	mdl_tex = Texture("models\\diablo3_pose\\diffuse.png")

	xmax = 0
	ymax = 0
	zmax = 0

	xmin = 0
	ymin = 0
	zmin = 0

	for v in vertices:
		xmax = max(xmax, v[0])
		ymax = max(ymax, v[1])
		zmax = max(zmax, v[2])

		xmin = min(xmin, v[0])
		ymin = min(ymin, v[1])
		zmin = min(zmin, v[2])

	bmax = max(xmax, max(ymax, zmax))
	bmin = min(xmin, min(ymin, zmin))
	bscale = bmax - bmin
	boffset = abs(bmin)


	for v in vertices:
		v[0] = (v[0] + boffset) / bscale;
		v[1] = (v[1] + boffset) / bscale;
		v[2] = (v[2] + boffset) / bscale;

	Utility.FetchTextures(textures)
	#for tex in textures:
	#    Console.WriteLine("{0}.jpg", tex);

	Renderer.Init()

	while Renderer.Window.IsOpen:
		Renderer.Window.Clear(0, 0, 0)

		#Renderer.Triangle((100, 50, 0), (300, 50, 0), (200, 250, 0), mdl_tex)

		'''
		for y in range(Renderer.Window.Height):
		    for x in range(Renderer.Window.Width):
				Renderer.Point(x, y, mdl_tex.Get(Single(x) / Renderer.Window.Width, Single(y) / Renderer.Window.Height))
		'''

		
		for face in faces:
			f = face[0]
			t = face[2]

			v0 = vertices[f[0] - 1]
			v1 = vertices[f[1] - 1]
			v2 = vertices[f[2] - 1]
			Renderer.Triangle(v0, v1, v2, mdl_tex)
		

		Renderer.Window.Update()
	return

if __name__ == "__main__":
	try:
		pymain()
	except:
		Utility.WriteError(sys.exc_info())