from SoftwareRenderer import *
import sys

def main():
    Renderer.Initialize()

    while True:
        Renderer.Clear(0, 0, 0)

        for i in range(100):
            Renderer.Point(100 + i, 100, 255, 255, 255)

        Renderer.Update()

    return 0


if __name__ == "__main__":
    sys.exit(main())