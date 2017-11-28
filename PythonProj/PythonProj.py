import clr
import sys

clr.AddReference("System")
clr.AddReference("System.Reflection")
clr.AddReference("System.IO")
from System import *

clr.AddReference("Utils")
from Utils import *

# Initialize important(tm) stuff
Utility.Init()

class ModelLoader:
    def Load(filename, swapyz=False):
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

    @staticmethod
    def Init():
        Renderer.Window = RenderWindow()
        return

    @staticmethod
    def Update():
        pass

def pymain():
    Renderer.Init()
    
    Console.WriteLine("Done!")
    Console.ReadLine()
    return

if __name__ == "__main__":
    try:
        pymain()
    except:
        Utility.WriteError(sys.exc_info())