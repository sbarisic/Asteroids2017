# Asteroids (2017)

A small project to practice python

# Features

* In-game console
* Console commands which are defined with attributes
```python
@DefineConCommand("banana")
def ConCmd_Banana(line, args, cmd):
	if len(args) == 2:
		for x in range(int(args[1])):
			ConWrite("Banana")
	else:
ConWrite("Banana!")
```
* Cheats
* Highscores
* Waves of asteroids
* Simple space physics/movement simulation
* Config file to store settings
* Anti tampering of the config file