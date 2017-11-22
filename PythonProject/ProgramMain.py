from SoftwareRenderer import *
import sys

def Rect(a, b, c, d):
    Renderer.Line(a, b, (255, 255, 255))
    Renderer.Line(b, c, (255, 255, 255))
    Renderer.Line(c, d, (255, 255, 255))
    Renderer.Line(d, a, (255, 255, 255))

def main():
    Renderer.Initialize()

    vertices, normals, texcoords, faces = ModelLoader.Load("E:\\Projects2017\\PythonProject\\obj_models\\diablo3_pose\\diablo3_pose.obj")

    while True:
        Renderer.Clear((0, 0, 0))

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
                Renderer.Line((x0, y0), (x1, y1), (255, 255, 255))

            # Update after every 10 faces
            if facenum % 10 == 0:
                Renderer.Update()
                Renderer.DoEvents()

        Renderer.DoEvents()
        Renderer.Update()

    return 0


if __name__ == "__main__":
    sys.exit(main())