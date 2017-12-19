import sys
print("Running on python", sys.version)

import os
import Engine

CHEATS = False

Cfg = Engine.Config()

Engine.WIDTH = Cfg.default("width", 1000)
Engine.HEIGHT = Cfg.default("height", 800)
Engine.CONSOLE_FONT_SIZE = Cfg.default("console_font_size", 22)
Engine.LINEAR_DAMPENING = float(Cfg.default("linear_dampening", 80)) / 100
Engine.ANGULAR_DAMPENING = float(Cfg.default("angular_dampening", 98)) / 100

ShowFPS = Cfg.default("showfps", 0) > 0

Highscore = Cfg.default("highscore", 0)
Money = Cfg.default("money", 0)
Diamonds = Cfg.default("diamonds", 0)
AsteroidMinSpeed = Cfg.default("ast_min_speed", 150)
AsteroidMaxSpeed = Cfg.default("ast_max_speed", 160)

UP_KEYS = [Engine.Keys.UP, Engine.Keys.W]
DOWN_KEYS = [Engine.Keys.DOWN, Engine.Keys.S]
LEFT_KEYS = [Engine.Keys.LEFT, Engine.Keys.A]
RIGHT_KEYS = [Engine.Keys.RIGHT, Engine.Keys.D]
SHOOT_KEYS = [Engine.Keys.SPACE]
PAUSE_KEYS = [Engine.Keys.P, Engine.Keys.PAUSE]

DiamondIcon = Engine.Icon("textures/diamond.png")
HitMarker = Engine.Icon("textures/hit_marker.png", True)
ConsoleBackground = Engine.Icon("textures/con_back.png", scale = 2.0, color = Engine.graphics.Color(255, 255, 255, 200))

HitSound = Engine.Sfx("sounds/hit.wav")
PewSound = Engine.Sfx("sounds/pew.wav")
ExplodeSound = Engine.Sfx("sounds/explode.wav")
MoveSound = Engine.Sfx("sounds/move.wav")
TurnSound = Engine.Sfx("sounds/turn.wav")
Pickup1Sound = Engine.Sfx("sounds/pickup_1.wav")

Entities = []
HitMarkers = []

ConsoleLines = []
TextInput = ""
InInput = False

Wave = 0
Score = 0
Paused = False

ConsoleCommands = {}
def DefineConCommand(*names):
	def Dec(fnc):
		for n in names:
			ConsoleCommands[n] = fnc

		return fnc
	return Dec

def Cheat(func):
	func.Cheat = True
	return func

def IsCheat(func):
	if hasattr(func, "Cheat"):
		return func.Cheat
	return False

@DefineConCommand("clear")
def ConCmd_Clear(line, args, cmd):
	ConsoleLines.clear()

@Cheat
@DefineConCommand("spawn_wave", "spawnwave")
def ConCmd_SpawnWave(line, args, cmd):
	if len(args) == 2:
		for i in range(int(args[1])):
			SpawnWave()
	else:
		SpawnWave()

@DefineConCommand("highscore")
def ConCmd_Highscore(line, args, cmd):
	global Highscore
	Highscore = Cfg.default("highscore", 0)
	ConWrite("Current highscore: {0}".format(Highscore))

@DefineConCommand("quit", "exit")
def ConCmd_Quit(line, args, cmd):
	os._exit(0)

@DefineConCommand("banana")
def ConCmd_Banana(line, args, cmd):
	if len(args) == 2:
		for x in range(int(args[1])):
			ConWrite("Banana")
	else:
		ConWrite("Banana!")

@Cheat
@DefineConCommand("get")
def ConCmd_Get(line, args, cmd):
	if len(args) > 1:
		for i in range(len(args) - 1):
			ConWrite(Cfg.get(args[i + 1], "None"))

@Cheat
@DefineConCommand("del")
def ConCmd_Del(line, args, cmd):
	if len(args) > 1:
		for i in range(len(args) - 1):
			Cfg.remove(args[i + 1])

@Cheat
@DefineConCommand("set")
def ConCmd_Set(line, args, cmd):
	if len(args) != 3:
		ConWrite("Command `set´ expects 3 arguments")
	else:
		Cfg.set(args[1], Engine.from_str(args[2]))
		ConCommand("get {0}".format(args[1]), False)

@Cheat
@DefineConCommand("kill")
def ConCmd_Kill(line, args, cmd):
	if len(args) == 2:
		for i in range(int(args[1])):
			KillPlayer()
	else:
		KillPlayer()

@DefineConCommand("newgame", "new_game")
def ConCmd_NewGame(line, args, cmd):
	NewGame()

@Cheat
@DefineConCommand("debug")
def ConCmd_Debug(line, args, cmd):
	Engine.DEBUG = not Engine.DEBUG
	ConWrite(Engine.DEBUG)

@Cheat
@DefineConCommand("debug_dist")
def ConCmd_DebugDist(line, args, cmd):
	if len(args) == 2:
		Engine.DEBUG_DIST = int(args[1])
		
	ConWrite(Engine.DEBUG_DIST)

@Cheat
@DefineConCommand("noclip")
def ConCmd_Noclip(line, args, cmd):
	Engine.NOCLIP = not Engine.NOCLIP
	ConWrite(Engine.NOCLIP)

@Cheat
@DefineConCommand("remove_asteroids", "removeasteroids")
def ConCmd_RemoveAsteroids(line, args, cmd):
	for e in list(Entities):
		if isinstance(e, Engine.Asteroid):
			RemoveEnts(e)

@DefineConCommand("help")
def ConCmd_Help(line, args, cmd):
	for c in sorted(ConsoleCommands):
		if IsCheat(ConsoleCommands[c]):
			if CHEATS:
				ConWrite(c + " " + ("-" * (30 - len(c))) + "- cheat")
		else:
			ConWrite(c)

@DefineConCommand("echo")
def ConCmd_Echo(line, args, cmd):
	if len(line) > 5:
		ConWrite(line[5:])
	else:
		ConWrite()

@DefineConCommand("fps")
def ConCmd_Fps(line, args, cmd):
	global ShowFPS
	ShowFPS = not ShowFPS
	Cfg.set("showfps", int(ShowFPS))

def PauseGame(dopause):
	global Paused
	Paused = dopause
	return

def RemoveEnts(*Ents):
	for e in Ents:
		if e in Entities:
			Entities.remove(e)
			del e
	
	return
		
def SpawnEnt(e):
	Entities.append(e)
	return

def CreateAsteroid(level, position = None):
	A = Engine.Asteroid(level)

	if position != None:
		A.position = position
	else:
		A.position = Engine.vec_rand((0, 0), (Engine.WIDTH, Engine.HEIGHT))

	A.angular_vel = (4 * Engine.randchance(50, 100)) * Engine.randchoice([-1, 1])
	A.linear_vel = Engine.vec_mul_scalar((0.5 + (level * 0.5)) * Engine.randchance(AsteroidMinSpeed, AsteroidMaxSpeed), Engine.vec_normal(Engine.randint(0, 360)))
	return A

def SpawnWave(w=None):
	global Wave

	if w == None:
		Wave = Wave + 1
	else:
		Wave = w

	for i in range(1 + Wave):
		a = CreateAsteroid(1)
		while Engine.vec_dist(a.position, Rocket.position) < 100:
			a = CreateAsteroid(1)

		SpawnEnt(a)
	return

def ConWrite(txt = ""):
	global ConsoleLines
	txt = str(txt)
	print(txt)

	ConsoleLines.insert(0, txt)
	ConsoleLines = ConsoleLines[:int(Engine.HEIGHT / Engine.CONSOLE_FONT_SIZE) - 1]
	return

def KillPlayer():
	RemoveEnts(Rocket)
	OnPlayerDied()
	return

def ConCommand(cmd, writeCmd = True):
	if len(cmd) == 0:
		CloseConsole()
		return

	if writeCmd:
		ConWrite(">> " + cmd)

	if ";" in cmd:
		for c in cmd.split(";"):
			ConCommand(c, False)
		return

	line = cmd.strip()
	args = line.split(" ")
	cmd = args[0]

	global CHEATS
	if not CHEATS:
		# Secret console command to enable cheats ;)
		CHEATS = Engine.compute_hash_int(line) == 448529426
		if CHEATS:
			return

	if cmd in ConsoleCommands:
		if IsCheat(ConsoleCommands[cmd]) and not CHEATS:
			ConWrite("Cheats are off")
		else:
			ConsoleCommands[cmd](line, args, cmd)
	else:
		ConWrite("Unknown command `{0}´".format(cmd))
	return

def OpenConsole():
	global InInput

	PauseGame(True)
	InInput = True
	return

def CloseConsole():
	global InInput

	InInput = False
	PauseGame(False)
	return

def OnText(unicode):
	global TextInput
	if not InInput:
		return

	if unicode == "\x1b":
		return

	# Basic autocompletion
	if unicode == "\t":
		TextInput = TextInput.strip()
		if len(TextInput) > 0:
			SortedConCommands = sorted(ConsoleCommands, key = len)
			for c in SortedConCommands:
				if c.startswith(TextInput) and c != TextInput:
					TextInput = c
					return
		return

	if unicode == "\b":
		if len(TextInput) > 0:
			TextInput = TextInput[:-1]
	elif unicode == "\r" or unicode == "\n":
		ConCommand(TextInput.strip())
		TextInput = ""
	else:
		TextInput = TextInput + unicode

	return

def OnKey(down, code):
	global Paused

	if InInput:
		return

	PrevTurnAmount = Rocket.TurnAmount
	PrevMoveAmount = Rocket.MoveAmount

	if code in LEFT_KEYS:
		Rocket.TurnAmount = -1 if down else 0
	if code in RIGHT_KEYS:
		Rocket.TurnAmount = 1 if down else 0
	if code in UP_KEYS:
		Rocket.MoveAmount = 1 if down else 0
	if code in DOWN_KEYS:
		Rocket.MoveAmount = -1 if down else 0

	if code in PAUSE_KEYS and down:
		PauseGame(not Paused)
	if code == Engine.Keys.ESCAPE and down:
		OpenConsole()
		
	if PrevMoveAmount == 0 and Rocket.MoveAmount != 0:
		OnMove(True, False)
	elif PrevMoveAmount != 0 and Rocket.MoveAmount == 0:
		OnMove(False, False)

	if PrevTurnAmount == 0 and Rocket.TurnAmount != 0:
		OnMove(True, True)
	elif PrevTurnAmount != 0 and Rocket.TurnAmount == 0:
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

	if Paused:
		return
	if not Rocket in Entities:
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
	global Highscore
	Highscore = Cfg.default("highscore", 0)

	Rocket.Lives = Rocket.Lives - 1
	ExplodeSound.play()

	if Rocket.Lives > 0:
		Rocket.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)
		Rocket.angular_vel = Engine.randint(-40, 40)
		Rocket.linear_vel = (0, 0)

		for e in Entities:
			if Engine.vec_dist(e.position, Rocket.position) < 75:
				RemoveEnts(e)
				HitSound.play()

		SpawnEnt(Rocket)

	elif Rocket.Lives <= 0:
		Rocket.Lives = 0
		if Score > Highscore:
			Highscore = Cfg.set("highscore", Score)

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

	Score = int(Score + (Score * 0.05))
	SpawnWave()

	if Engine.randchance(0, 100) >= 95:
		Rocket.Lives = Rocket.Lives + 1
		Pickup1Sound.play()

	return

# Both update and render are in the same function to cut down on entity
# iteration count
def UpdateAndRender(dt, Window):
	global PrevAsteroidCount
	if not "PrevAsteroidCount" in globals():
		PrevAsteroidCount = -1

	elapsed_sec = GameClock.elapsed_time.seconds

	if not Paused:
		if Rocket.TurnAmount != 0 and abs(Rocket.angular_vel) < 20: # 20 (def), max rocket angular velocity
			Rocket.angular_vel = Rocket.angular_vel + (25 * Rocket.TurnAmount * dt)

		if Rocket.MoveAmount != 0:
			Norm = Engine.vec_mul_scalar(5 * Rocket.MoveAmount * dt, Engine.vec_normal(Engine.to_rad(Rocket.angle - 90)))
			Rocket.linear_vel = Engine.vec_add_vec(Rocket.linear_vel, Norm)

	AsteroidCount = 0

	for e in Entities:
		# Keep count of asteroids
		if isinstance(e, Engine.Asteroid):
			AsteroidCount = AsteroidCount + 1

		if Engine.DEBUG and (Engine.DEBUG_DIST > 0):
			if (Engine.vec_dist(Rocket.position, e.position) < Engine.DEBUG_DIST):
				e.Debug.outline_color = Engine.graphics.Color.GREEN
			else:
				e.Debug.outline_color = Engine.graphics.Color.RED


		if not Paused:
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
							KillPlayer()

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

	if (Rocket.Lives <= 0):
		Engine.drawText(Window, (Engine.WIDTH * 0.25, Engine.HEIGHT * 0.3), 50, "Game Over: " + str(Score) + "\nHighscore: " + str(Highscore))
	else:
		#Engine.drawText(Window, (10, 0), 42, str(Score) + "\n" + ("^" *
		#Rocket.Lives) + "\n$ " + str(Money) + "\n 0")
		#DiamondIcon.draw(Window, (0, 140))

		Engine.drawText(Window, (10, 0), 42, str(Score) + "\n" + ("^" * Rocket.Lives))
		Engine.drawText(Window, (Engine.WIDTH * 0.4, 0), 30, "Wave " + str(Wave))


	if InInput:
		Txt = ">" + TextInput
		if int(GameClock.elapsed_time.seconds * 2) % 2 == 0:
			Txt = Txt + "_"
			
		Offset = -10
		Line = Engine.HEIGHT - (Engine.CONSOLE_FONT_SIZE * 2)

		ConsoleBackground.draw(Window, (0, 0))

		for l in ConsoleLines:
			Engine.drawText(Window, (10, Line + Offset), Engine.CONSOLE_FONT_SIZE, l)
			Line = Line - Engine.CONSOLE_FONT_SIZE

		Engine.drawText(Window, (10, Engine.HEIGHT - Engine.CONSOLE_FONT_SIZE + Offset), Engine.CONSOLE_FONT_SIZE, Txt)

	if ShowFPS and dt != 0:
		Engine.drawText(Window, (Engine.WIDTH - 20 * 5, 0), 20, "{0} FPS".format(round(1.0 / dt, 0)))

	return

def NewGame():
	global Wave
	global Score
	global Rocket
	global Entities
	global GameClock
	global NextShotTime

	Wave = 0
	Score = 0
	NextShotTime = 0

	# Remove all entities
	Entities.clear()

	# Spawn the rocket
	Rocket = Engine.Rocket()
	Rocket.position = (Engine.WIDTH / 2, Engine.HEIGHT / 2)
	Rocket.angular_vel = Engine.randint(-40, 40)
	SpawnEnt(Rocket)

	SpawnWave()
	GameClock = Engine.Clock()
	return

def main():
	global Entities
	global GameClock

	ConWrite("Project by Saša Barišić")
	if not Cfg.antitamper_success:
		ConWrite("Config file was tampered with, resetting to default values :-)")
	ConWrite("Running in " + Engine.getrootdir())

	Window = Engine.createWindow("Asteroids (2017)")

	OpenConsole()
	NewGame()

	Clock = Engine.Clock()
	DeltaTime = 0

	RT = Engine.RT()

	PostShader = Engine.Shader("shaders/post.frag")
	PostShader.setparam("tex", RT.RT.texture)
	PostShader.setparam("width", float(Engine.WIDTH))
	PostShader.setparam("height", float(Engine.HEIGHT))
	#PostShader.setparam("pixelate", float(Engine.WIDTH * 0.86))

	ChromaH = 1.5
	ChromaV = 0.5

	while Window.is_open:
		Engine.handleEvents(Window, OnKey, OnText)

		PostShader.setparam("time", Clock.elapsed_time.seconds)
		PostShader.setparam("chroma_r", (ChromaH, ChromaV))
		PostShader.setparam("chroma_g", (0, 0))
		PostShader.setparam("chroma_b", (-ChromaH, -ChromaV))

		# Draw the game screen to a render target
		RT.clear()
		UpdateAndRender(DeltaTime, RT.RT)
		RT.display()

		# Draw the render target with applied shaders
		Window.clear(Engine.graphics.Color(255, 0, 0))
		PostShader.bind()
		RT.draw(Window)
		PostShader.unbind()
		Window.display()

		while (Clock.elapsed_time.seconds < (1.0 / Engine.TARGET_FPS)):
			pass

		DeltaTime = Clock.restart().seconds

	return 0


if __name__ == "__main__":
	os._exit(main())

''' End of sauce, now fetch me some chips '''