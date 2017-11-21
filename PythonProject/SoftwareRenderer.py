import sdl2
import sdl2.ext
import sdl2.pixels
import sdl2.render
import sdl2.surface
import sys

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
    def Clear(r, g, b):
        #sdl2.ext.fill(Renderer.WindowSurface, sdl2.ext.Color(r, g, b))
        Renderer.Renderer.clear(sdl2.ext.Color(r, g, b))
        return

    def Point(x, y, r, g, b):
        Renderer.Renderer.draw_point((x, y), sdl2.ext.Color(r, g, b))
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
