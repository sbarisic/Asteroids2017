import os
import Engine

UP_KEYS = [Engine.Keys.UP, Engine.Keys.W]
DOWN_KEYS = [Engine.Keys.DOWN, Engine.Keys.S]
LEFT_KEYS = [Engine.Keys.LEFT, Engine.Keys.A]
RIGHT_KEYS = [Engine.Keys.RIGHT, Engine.Keys.D]
SHOOT_KEYS = [Engine.Keys.SPACE]

DiamondIcon = Engine.Icon("textures/diamond.png")
HitMarker = Engine.Icon("textures/hit_marker.png", True)

HitSound = Engine.Sfx("sounds/hit.wav")
PewSound = Engine.Sfx("sounds/pew.wav")
ExplodeSound = Engine.Sfx("sounds/explode.wav")
MoveSound = Engine.Sfx("sounds/move.wav")
TurnSound = Engine.Sfx("sounds/turn.wav")
Pickup1Sound = Engine.Sfx("sounds/pickup_1.wav")

Entities = []
HitMarkers = []

Wave = 0
Money = 0
Diamonds = 0
Lives = 4
Score = 0
PrevAsteroidCount = -1
TurnAmount = 0
MoveAmount = 0
PlayerSpawned = False
NextShotTime = 0

def RemoveEnts(*Ents):
	global PlayerSpawned

	for e in Ents:
		if e in Entities:
			if isinstance(e, Engine.Rocket):
				PlayerSpawned = False

			Entities.remove(e)
			del e
	
	return
		
def SpawnEnt(e):
	global PlayerSpawned

	if isinstance(e, Engine.Rocket):
		PlayerSpawned = True

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

def SpawnWave():
	global Wave
	Wave = Wave + 1

	for i in range(1 + Wave):
		a = CreateAsteroid(1)
		while Engine.vec_dist(a.position, Rocket.position) < 200:
			a = CreateAsteroid(1)

		SpawnEnt(a)
	return

def OnKey(down, code):
	global TurnAmount
	global MoveAmount

	PrevTurnAmount = TurnAmount
	PrevMoveAmount = MoveAmount

	if code in LEFT_KEYS:
		TurnAmount = -1 if down else 0
	if code in RIGHT_KEYS:
		TurnAmount = 1 if down else 0
	if code in UP_KEYS:
		MoveAmount = 1 if down else 0
	if code in DOWN_KEYS:
		MoveAmount = -1 if down else 0
		
	if PrevMoveAmount == 0 and MoveAmount != 0:
		OnMove(True, False)
	elif PrevMoveAmount != 0 and MoveAmount == 0:
		OnMove(False, False)

	if PrevTurnAmount == 0 and TurnAmount != 0:
		OnMove(True, True)
	elif PrevTurnAmount != 0 and TurnAmount == 0:
		OnMove(False, True)

	if down and (code in SHOOT_KEYS):
		OnShoot()

	return

def OnMove(begin, turn):
	# These are actually annoying, lmao

	'''
	if begin and not turn:
		MoveSound.begin_play()
	elif not begin and not turn:
		MoveSound.end_play()

	if begin and turn:
		TurnSound.begin_play()
	elif not begin and turn:
		TurnSound.end_play()
	'''

	return

def OnShoot():
	global NextShotTime

	if not PlayerSpawned:
		return

	if NextShotTime - GameClock.elapsed_time.seconds > 0:
		return
	NextShotTime = GameClock.elapsed_time.seconds + 0.25

	Bullet = Engine.Bullet()
	Bullet.angle = Rocket.angle
	Bullet.position = Rocket.position
	Bullet.end_life = GameClock.elapsed_time.seconds + 1.5
	Bullet.linear_vel = Engine.vec_mul_scalar(6, Engine.vec_normal(Engine.to_rad(Bullet.angle - 90)))

	PewSound.play()
	SpawnEnt(Bullet)
	return

def OnPlayerDied():
	global Lives
	Lives = Lives - 1
	ExplodeSound.play()

	if Lives > 0:
		Rocket.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)
		Rocket.angular_vel = Engine.randint(-40, 40)
		Rocket.linear_vel = (0, 0)
		SpawnEnt(Rocket)

	elif Lives < 0:
		Lives = 0

	return

def OnScore(score):
	global Score
	global Money

	Score = Score + score

	if Engine.randchance(0, 100) > 0.8:
		Money = Money + int(score / 10)

	return

def OnAllAsteroidsDestroyed():
	global Score
	global Lives

	Score = int(Score + (Score * 0.05))
	SpawnWave()

	if Engine.randchance(0, 100) > 95:
		Lives = Lives + 1
		Pickup1Sound.play()

	return

# Both update and render are in the same function to cut down on entity
# iteration count
def UpdateAndRender(dt):
	global PrevAsteroidCount
	elapsed_sec = GameClock.elapsed_time.seconds

	if TurnAmount != 0 and abs(Rocket.angular_vel) < 20: # 20 (def), max rocket angular velocity
		Rocket.angular_vel = Rocket.angular_vel + (25 * TurnAmount * dt)

	if MoveAmount != 0:
		Norm = Engine.vec_mul_scalar(5 * MoveAmount * dt, Engine.vec_normal(Engine.to_rad(Rocket.angle - 90)))
		Rocket.linear_vel = Engine.vec_add_vec(Rocket.linear_vel, Norm)

	AsteroidCount = 0

	for e in Entities:
		# Keep count of asteroids
		if isinstance(e, Engine.Asteroid):
			AsteroidCount = AsteroidCount + 1

		for e2 in Entities:
			if e != e2:
				if isinstance(e, Engine.Asteroid) and isinstance(e2, Engine.Bullet):
					if Engine.collides(e, e2):
						if e.level < 3:
							for i in range(e.level + 1):
								SpawnEnt(CreateAsteroid(e.level + 1, e.position))

						HitMarkers.append((e2.position[0], e2.position[1], elapsed_sec + 0.3))
						HitSound.play()

						RemoveEnts(e, e2)
						OnScore(e.score) # On score event

				elif isinstance(e, Engine.Asteroid) and isinstance(e2, Engine.Rocket):
					if Engine.collides(e, e2):
						RemoveEnts(e2)
						OnPlayerDied() # On player died event

		e.update(dt)
		e.draw(Window)

		if isinstance(e, Engine.Bullet):
			if e.end_life <= GameClock.elapsed_time.seconds:
				RemoveEnts(e)

	# On all asteroids destroyed event
	if (PrevAsteroidCount != 0 and AsteroidCount == 0):
		OnAllAsteroidsDestroyed()

	PrevAsteroidCount = AsteroidCount

	for m in HitMarkers:
		if m[2] < elapsed_sec:
			HitMarkers.remove(m)
			pass

		HitMarker.draw(Window, (m[0], m[1]))


	# GUI

	if (Lives <= 0):
		Engine.drawText(Window, (Engine.WIDTH * 0.25, Engine.HEIGHT * 0.3), 50, " Game Over: " + str(Score))
	else:
		Engine.drawText(Window, (10, 0), 42, str(Score) + "\n" + ("^" * Lives) + "\n$ " + str(Money) + "\n  0")
		Engine.drawText(Window, (Engine.WIDTH * 0.4, 0), 30, "Wave " + str(Wave))
		DiamondIcon.draw(Window, (0, 140))


	return

def main():
	global Window
	global Rocket
	global Entities
	global GameClock

	print("Running in", Engine.getrootdir())
	Window = Engine.createWindow("Asteroids (2017)")

	# Spawn the rocket
	Rocket = Engine.Rocket()
	Rocket.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)
	Rocket.angular_vel = Engine.randint(-40, 40)
	SpawnEnt(Rocket)

	SpawnWave()

	GameClock = Engine.Clock()
	Clock = Engine.Clock()
	DeltaTime = 0

	while Window.is_open:
		Engine.handleEvents(Window, OnKey)

		Window.clear()
		UpdateAndRender(DeltaTime)
		Window.display()

		while (Clock.elapsed_time.seconds < (1.0 / Engine.TARGET_FPS)):
			pass

		DeltaTime = Clock.restart().seconds

	return 0

if __name__ == "__main__":
	os._exit(main())

''' End of sauce, now fetch me some chips '''