from SoftwareRenderer import *
import sys

def Rect(a, b, c, d):
    Renderer.Line(a, b, (255, 255, 255))
    Renderer.Line(b, c, (255, 255, 255))
    Renderer.Line(c, d, (255, 255, 255))
    Renderer.Line(d, a, (255, 255, 255))

def main():
    Renderer.Initialize()

    Msh = ModelLoader.Load("E:\\Projects2017\\PythonProject\\obj_models\\diablo3_pose\\diablo3_pose.obj")

    while True:
        Renderer.Clear((0, 0, 0))

        #for n in range(10):
        Rect((100, 100), (200, 100), (200, 200), (100, 200))

        #for i in range(100):
        #    Renderer.Point((100 + i, 500), (255, 255, 255))

        #Renderer.Line((100, 100), (220, 240), (255, 255, 255))

        #for i in range(100):
        #    Renderer.Point((100 + i, 100), (255, 255, 255))

        Renderer.Update()

    return 0


if __name__ == "__main__":
    sys.exit(main())