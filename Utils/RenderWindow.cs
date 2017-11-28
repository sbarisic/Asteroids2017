using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Utils {
	public class RenderWindow {

		public RenderWindow(int Width = 800, int Height = 600, int VirtWidth = 400, int VirtHeight = 300) {
			if (SDL.SDL_Init(SDL.SDL_INIT_VIDEO) != 0)
				throw new Exception(SDL.SDL_GetError());
		}

		public void Update() {
			SDL.SDL_Event E;

			while (SDL.SDL_PollEvent(out E) != 0) {
				if (E.type == SDL.SDL_EventType.SDL_QUIT) {

				}
			}
		}
	}
}
