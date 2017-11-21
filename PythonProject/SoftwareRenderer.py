import sdl2
import sdl2.ext
import sdl2.pixels
import sdl2.render
import sdl2.surface
import sys

class ModelLoader:
    def Load(path):
        return

class Renderer:
    Window = None
    #WindowSurface = None
    Renderer = None

    Width = 800
    Height = 600

    @staticmethod
    def Initialize():
        sdl2.ext.init()

        Renderer.Window = sdl2.ext.Window("SoftwareRenderer Window", size = (Renderer.Width, Renderer.Height))
        Renderer.Window.show()
        #Renderer.WindowSurface = Renderer.Window.get_surface()
        Renderer.Renderer = sdl2.ext.Renderer(Renderer.Window)
        return

    @staticmethod
    def Clear(rgb):
        #sdl2.ext.fill(Renderer.WindowSurface, sdl2.ext.Color(r, g, b))
        Renderer.Renderer.clear(sdl2.ext.Color(*rgb))
        return

    def Point(xy, rgb):
        Renderer.Renderer.draw_point(xy, sdl2.ext.Color(*rgb))
        return

    def Line(start, end, rgb):
        x0 = start[0]
        y0 = start[1]
        x1 = end[0]
        y1 = end[1]
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
    def Update():
        events = sdl2.ext.get_events()
        for e in events:
            if e.type == sdl2.SDL_QUIT:
                sys.exit()

        Renderer.Renderer.present()
        Renderer.Window.refresh()
        return
