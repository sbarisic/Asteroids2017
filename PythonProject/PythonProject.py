import os
import Engine

UP_KEYS = [ Engine.Keys.UP, Engine.Keys.W ]
DOWN_KEYS = [ Engine.Keys.DOWN, Engine.Keys.S ]
LEFT_KEYS = [ Engine.Keys.LEFT, Engine.Keys.A ]
RIGHT_KEYS = [ Engine.Keys.RIGHT, Engine.Keys.D ]
SHOOT_KEYS = [ Engine.Keys.SPACE ]

GameClock = Engine.Clock()
Clock = Engine.Clock()
DeltaTime = 0
TurnAmount = 0
MoveAmount = 0

Window = None

Entities = []

Rocket = Engine.Rocket()
Rocket.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)
Rocket.linear_vel = (0, 10)
Rocket.angular_vel = 40
Entities.append(Rocket)

for i in range(10):
	Asteroid = Engine.Asteroid()
	Asteroid.position = Engine.vec_rand((0, 0), (Engine.WIDTH, Engine.HEIGHT))
	Asteroid.angular_vel = Engine.randint(-2, 2)
	Entities.append(Asteroid)

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
		Bullet = Engine.Bullet()
		Bullet.angle = Rocket.angle
		Bullet.position = Rocket.position
		Bullet.end_life = GameClock.elapsed_time.seconds + 3
		Bullet.linear_vel = Engine.vec_mul_scalar(6, Engine.vec_normal(Engine.to_rad(Bullet.angle - 90)))
		Entities.append(Bullet)

	return

def update(dt):
	MaxVel = 20
	TurnVelocity = 25 * TurnAmount * dt
	if TurnAmount != 0 and abs(Rocket.angular_vel) < MaxVel:
		Rocket.angular_vel = Rocket.angular_vel + TurnVelocity

	for e in Entities:
		e.update(dt)

		if isinstance(e, Engine.Bullet):
			if e.end_life <= GameClock.elapsed_time.seconds:
				Entities.remove(e)
	return

def render():
	Window.clear()

	for e in Entities:
	    e.draw(Window)

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