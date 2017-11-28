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
        y = int(v * self.Height)

        if x < 0:
            x = 0
        if x >= self.Width:
            x = self.Width - 1
        if y < 0:
            y = 0
        if y >= self.Height:
            y = self.Height - 1

        return Pixels[y * self.Width + x]



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
    def Triangle(a, b, c):

        return

def pymain():
    #mdl = "models\\level.obj"
    mdl = "models\\diablo3_pose\diablo3_pose.obj"

    vertices, normals, texcoords, faces, textures = ModelLoader.Load(mdl)
    mdl_tex = Texture("models\\diablo3_pose\\diffuse.png")

    Utility.FetchTextures(textures)
    #for tex in textures:
    #    Console.WriteLine("{0}.jpg", tex);

    Renderer.Init()

    while Renderer.Window.IsOpen:
        Renderer.Window.Clear(0, 0, 0)

        for face in faces:
            f = face[0]

            for i in range(3):
                v0idx = f[i] - 1
                v1idx = f[(i + 1) % 3] - 1

                v0 = vertices[v0idx]
                v1 = vertices[v1idx]

                x0 = (v0[0] + 1) * Renderer.Window.Width / 2
                y0 = (v0[1] + 1) * Renderer.Window.Height / 2
                x1 = (v1[0] + 1) * Renderer.Window.Width / 2
                y1 = (v1[1] + 1) * Renderer.Window.Height / 2
                Renderer.Line((x0, y0), (x1, y1), (255, 255, 255))

        Renderer.Window.Update()
    return

if __name__ == "__main__":
    try:
        pymain()
    except:
        Utility.WriteError(sys.exc_info())