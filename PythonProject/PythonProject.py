import os
import Engine

Window = None

def update():
	return

def render():
	Window.clear()

	Window.display()
	return

def main():
	global Window
	Window = Engine.CreateWindow()

	while Window.is_open:
		Engine.HandleEvents(Window)
		update()
		render()

	return 0

if __name__ == "__main__":
	os._exit(main())

''' End of sauce, now fetch me some chips '''