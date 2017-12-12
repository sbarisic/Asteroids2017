import os
import Engine

UP_KEYS = [ Engine.Keys.UP, Engine.Keys.W ]
DOWN_KEYS = [ Engine.Keys.DOWN, Engine.Keys.S ]
LEFT_KEYS = [ Engine.Keys.LEFT, Engine.Keys.A ]
RIGHT_KEYS = [ Engine.Keys.RIGHT, Engine.Keys.D ]
SHOOT_KEYS = [ Engine.Keys.SPACE ]

Clock = Engine.Clock()
DeltaTime = 0
TurnAmount = 0
MoveAmount = 0

Window = None

Bullet = Engine.Bullet()
Bullet.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)

Rocket = Engine.Rocket()
Rocket.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)

Rocket.linear_vel = (0, 10)
Rocket.angular_vel = 40

def onKey(down, code):
	global TurnAmount
	global MoveAmount

	if code in LEFT_KEYS:
		TurnAmount = -1 if down else 0
	if code in RIGHT_KEYS:
		TurnAmount = 1 if down else 0
	if code in UP_KEYS:
		MoveAmount = 1 if down else 0
	if code in DOWN_KEYS:
		MoveAmount = -1 if down else 0

	if down and (code in SHOOT_KEYS):
		print("Pew pew!")

	return

def update(dt):
	MaxVel = 20
	TurnVelocity = 25 * TurnAmount * dt
	if TurnAmount != 0 and abs(Rocket.angular_vel) < MaxVel:
		Rocket.angular_vel = Rocket.angular_vel + TurnVelocity

	Rocket.update(dt)
	Bullet.update(dt)

	Bullet.angle = Bullet.angle + 1

	return

def render():
	Window.clear()

	Rocket.draw(Window)
	Bullet.draw(Window)

	Window.display()
	return

def main():
	global Window
	global DeltaTime

	Window = Engine.CreateWindow()

	while Window.is_open:
		Engine.HandleEvents(Window, onKey)
		update(DeltaTime)
		render()

		while (Clock.elapsed_time.seconds < (1.0 / Engine.TARGET_FPS)):
			pass

		DeltaTime = Clock.restart().seconds

	return 0

if __name__ == "__main__":
	os._exit(main())

''' End of sauce, now fetch me some chips '''