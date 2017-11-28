import sdl2
import sdl2.ext
import sdl2.pixels
import sdl2.render
import sdl2.surface
import sys
import os

class ModelLoader:
    def Load(filename, swapyz = False):
        vertices = []
        normals = []
        texcoords = []
        faces = []
        textures = []

        for line in open(filename, "r"):
            if line.startswith("#"): continue
            values = line.split()
            if not values: continue

            if values[0] == "usemtl":
                if values[1] not in textures:
                    textures.append(values[1])
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
    #WindowSurface = None
    Renderer = None

    Width = 800
    Height = 600

    @staticmethod
    def Initialize(W, H, VW, VH):
        sdl2.ext.init()

        Renderer.Width = VW
        Renderer.Height = VH

        Renderer.Window = sdl2.ext.Window("SoftwareRenderer Window", size = (W, H))
        Renderer.Window.show()
        #Renderer.WindowSurface = Renderer.Window.get_surface()
        Renderer.Renderer = sdl2.ext.Renderer(Renderer.Window)

        sdl2.render.SDL_RenderSetLogicalSize(Renderer.Renderer.renderer, VW, VH)
        return

    @staticmethod
    def Clear(rgb):
        #sdl2.ext.fill(Renderer.WindowSurface, sdl2.ext.Color(r, g, b))
        Renderer.Renderer.clear(sdl2.ext.Color(*rgb))
        return

    def Point(xy, rgb):
        Renderer.Renderer.draw_point((xy[0], Renderer.Height - xy[1]), sdl2.ext.Color(*rgb))
        #Renderer.DoEvents()
        #Renderer.Update()
        return

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
                Renderer.Point((y, x), rgb)
            else:
                Renderer.Point((x, y), rgb)

            error2 += derror2
            if (error2 > dx):
                y += 1 if (y1 > y0) else -1
                error2 -= dx * 2
        return

    @staticmethod
    def DoEvents():
        events = sdl2.ext.get_events()
        for e in events:
            if e.type == sdl2.SDL_QUIT:
                sys.exit()
        return

    @staticmethod
    def Update():
        Renderer.Renderer.present()
        Renderer.Window.refresh()
        return


from SoftwareRenderer import *
import io
import sys

def Rect(a, b, c, d):
    Renderer.Line(a, b, (255, 255, 255))
    Renderer.Line(b, c, (255, 255, 255))
    Renderer.Line(c, d, (255, 255, 255))
    Renderer.Line(d, a, (255, 255, 255))

def main():
    vertices, normals, texcoords, faces, textures = ModelLoader.Load("models\\level.obj")

    for tex in textures:
        print(tex)

    Renderer.Initialize(800, 600, 400, 300)
    while True:
        Renderer.Clear((255, 255, 255))

        facenum = -1
        for face in faces:
            f = face[0]
            facenum += 1

            for i in range(3):
                v0idx = f[i] - 1
                v1idx = f[(i + 1) % 3] - 1

                v0 = vertices[v0idx]
                v1 = vertices[v1idx]

                x0 = (v0[0] + 1) * Renderer.Width / 2
                y0 = (v0[1] + 1) * Renderer.Height / 2
                x1 = (v1[0] + 1) * Renderer.Width / 2
                y1 = (v1[1] + 1) * Renderer.Height / 2
                Renderer.Line((x0, y0), (x1, y1), (0, 0, 0))

            # Update after every 10 faces
            if facenum % 20 == 0:
                Renderer.Update()
                Renderer.DoEvents()

        Renderer.DoEvents()
        Renderer.Update()

    return 0


if __name__ == "__main__":
    sys.exit(main())