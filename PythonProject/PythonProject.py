import os
import Engine

UP_KEYS = [Engine.Keys.UP, Engine.Keys.W]
DOWN_KEYS = [Engine.Keys.DOWN, Engine.Keys.S]
LEFT_KEYS = [Engine.Keys.LEFT, Engine.Keys.A]
RIGHT_KEYS = [Engine.Keys.RIGHT, Engine.Keys.D]
SHOOT_KEYS = [Engine.Keys.SPACE]

Score = 0
PrevAsteroidCount = -1
TurnAmount = 0
MoveAmount = 0

def RemoveEnts(*Ents):
	for e in Ents:
		if e in Entities:
			Entities.remove(e)
			del e
	
	return
		
def SpawnEnt(e):
	Entities.append(e)
	return

def CreateAsteroid(level, position=None):
	A = Engine.Asteroid(level)

	if position != None:
		A.position = position
	else:
		A.position = Engine.vec_rand((0, 0), (Engine.WIDTH, Engine.HEIGHT))

	A.angular_vel = (4 * Engine.randchance(50, 100)) * Engine.randchoice([-1, 1])
	A.linear_vel = Engine.vec_mul_scalar((0.5 + (level * 0.5)) * Engine.randchance(90, 110), Engine.vec_normal(Engine.randint(0, 360)))
	return A

def OnKey(down, code):
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
		OnShoot()

	return

def OnShoot():
	Bullet = Engine.Bullet()
	Bullet.angle = Rocket.angle
	Bullet.position = Rocket.position
	Bullet.end_life = GameClock.elapsed_time.seconds + 1.5
	Bullet.linear_vel = Engine.vec_mul_scalar(6, Engine.vec_normal(Engine.to_rad(Bullet.angle - 90)))
	SpawnEnt(Bullet)
	return

def OnPlayerDied():
	print("You died! {0} pts".format(Score))
	return

def OnScore(score):
	global Score

	Score = Score + score
	print(Score)
	return

def OnAllAsteroidsDestroyed():
	print("You win! {0} pts".format(Score))
	return

def Update(dt):
	global PrevAsteroidCount

	if TurnAmount != 0 and abs(Rocket.angular_vel) < 20: # 20 (def), max rocket angular velocity
		Rocket.angular_vel = Rocket.angular_vel + (25 * TurnAmount * dt)

	if MoveAmount != 0:
		Norm = Engine.vec_mul_scalar(5 * MoveAmount * dt, Engine.vec_normal(Engine.to_rad(Rocket.angle - 90)))
		Rocket.linear_vel = Engine.vec_add_vec(Rocket.linear_vel, Norm)

	AsteroidCount = 0

	for e in Entities:
		if isinstance(e, Engine.Asteroid):
			AsteroidCount = AsteroidCount + 1

		for e2 in Entities:
			if e != e2:
				if isinstance(e, Engine.Bullet) and isinstance(e2, Engine.Asteroid) and Engine.collides(e, e2):
					if e2.level < 3:
						for i in range(e2.level + 1):
							SpawnEnt(CreateAsteroid(e2.level + 1, e2.position))

					RemoveEnts(e, e2)
					OnScore(e2.score)

				elif isinstance(e, Engine.Asteroid) and isinstance(e2, Engine.Rocket) and Engine.collides(e, e2):
					RemoveEnts(e2)
					OnPlayerDied()

		e.update(dt)

		if isinstance(e, Engine.Bullet):
			if e.end_life <= GameClock.elapsed_time.seconds:
				RemoveEnts(e)

	if (PrevAsteroidCount != 0 and AsteroidCount == 0):
		OnAllAsteroidsDestroyed()

	PrevAsteroidCount = AsteroidCount
	return

def Render():
	Window.clear()

	for e in Entities:
	    e.draw(Window)

	Window.display()
	return

def main():
	global Window
	global Rocket
	global Entities
	global GameClock

	print("Running in", Engine.getrootdir())
	Window = Engine.CreateWindow()
	Entities = []

	# Spawn the rocket
	Rocket = Engine.Rocket()
	Rocket.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)
	Rocket.angular_vel = Engine.randint(-40, 40)
	SpawnEnt(Rocket)

	# Spawn asteroids
	for i in range(5):
		SpawnEnt(CreateAsteroid(1))

	GameClock = Engine.Clock()
	Clock = Engine.Clock()
	DeltaTime = 0

	while Window.is_open:
		Engine.HandleEvents(Window, OnKey)
		Update(DeltaTime)
		Render()

		while (Clock.elapsed_time.seconds < (1.0 / Engine.TARGET_FPS)):
			pass

		DeltaTime = Clock.restart().seconds

	return 0

if __name__ == "__main__":
	os._exit(main())

''' End of sauce, now fetch me some chips '''