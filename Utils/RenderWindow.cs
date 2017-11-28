using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Numerics;

namespace Utils {
	[StructLayout(LayoutKind.Sequential, Pack = 1)]
	public struct Pixel {
		public byte R, G, B, A;

		public Pixel(byte R, byte G, byte B, byte A) {
			this.R = R;
			this.G = G;
			this.B = B;
			this.A = A;
		}

		public Pixel(Color Clr) : this(Clr.R, Clr.G, Clr.B, Clr.A) {
		}

		public void Set(byte R, byte G, byte B) {
			this.R = R;
			this.G = G;
			this.B = B;
			this.A = 255;
		}
	}

	public unsafe class RenderWindow {
		Stopwatch SWatch;

		IntPtr Window;
		IntPtr Renderer;

		SDL.SDL_Rect RenderTextureRect;
		IntPtr RenderTexture;
		Pixel* RenderPixels;

		public int Width {
			get;
			private set;
		}

		public int Height {
			get;
			private set;
		}

		public bool IsOpen {
			get;
			private set;
		}

		public RenderWindow(int Width = 800, int Height = 600, int VirtWidth = 400, int VirtHeight = 300) {
			Console.Title = "IronPython Project";
			SWatch = Stopwatch.StartNew();

			if (SDL.SDL_Init(SDL.SDL_INIT_VIDEO) != 0)
				throw new Exception(SDL.SDL_GetError());
			SetHint(SDL.SDL_HINT_RENDER_SCALE_QUALITY, "nearest");

			SDL.SDL_CreateWindowAndRenderer(Width, Height, SDL.SDL_WindowFlags.SDL_WINDOW_SHOWN, out Window, out Renderer);
			if (Window == IntPtr.Zero)
				throw new Exception(SDL.SDL_GetError());

			SDL.SDL_RenderSetLogicalSize(Renderer, VirtWidth, VirtHeight);
			IsOpen = true;

			this.Width = VirtWidth;
			this.Height = VirtHeight;
			RenderTextureRect = new SDL.SDL_Rect();
			RenderTextureRect.x = 0;
			RenderTextureRect.y = 0;
			RenderTextureRect.w = VirtWidth;
			RenderTextureRect.h = VirtHeight;

			RenderTexture = SDL.SDL_CreateTexture(Renderer, SDL.SDL_PIXELFORMAT_ARGB8888, (int)SDL.SDL_TextureAccess.SDL_TEXTUREACCESS_STREAMING, VirtWidth, VirtHeight);
			RenderPixels = (Pixel*)Marshal.AllocHGlobal(VirtWidth * VirtHeight * sizeof(Pixel));
		}

		void SetHint(string Name, object Value) {
			if (SDL.SDL_SetHint(Name, Value.ToString()) == SDL.SDL_bool.SDL_FALSE)
				Console.WriteLine("{0} hint not set to {1}", Name, Value);
		}

		public void Clear(byte R, byte G, byte B) {
			for (int i = 0; i < Width * Height; i++)
				RenderPixels[i].Set(R, G, B);
		}

		public void PutPixel(int X, int Y, byte R, byte G, byte B) {
			if (X < 0 || X >= Width)
				return;
			if (Y < 0 || Y >= Height)
				return;

			int Idx = (Height - Y) * (Width) + X;
			RenderPixels[Idx].Set(R, G, B);
		}

		public void UpdateTexture() {
			SDL.SDL_UpdateTexture(RenderTexture, ref RenderTextureRect, (IntPtr)RenderPixels, Width * sizeof(Pixel));
			SDL.SDL_RenderCopy(Renderer, RenderTexture, IntPtr.Zero, IntPtr.Zero);
			SDL.SDL_RenderPresent(Renderer);
		}

		public void UpdateEvents() {
			SDL.SDL_Event E;

			while (SDL.SDL_PollEvent(out E) != 0) {
				if (E.type == SDL.SDL_EventType.SDL_QUIT) {
					SDL.SDL_DestroyRenderer(Renderer);
					SDL.SDL_DestroyWindow(Window);
					IsOpen = false;
				}
			}
		}

		public void Update() {
			UpdateEvents();
			UpdateTexture();

			while (SWatch.ElapsedMilliseconds < (1.0f / 100 * 1000))
				;
			float MS = SWatch.ElapsedMilliseconds;
			SWatch.Restart();
			SDL.SDL_SetWindowTitle(Window, string.Format("SDL2 Window; {0} FPS, {1} ms", 1000 / MS, MS));

		}
	}
}
