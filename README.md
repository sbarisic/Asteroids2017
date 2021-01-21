# Asteroids (2017)

A small project to practice python

[>> DOWNLOAD NOW <<](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/AsteroidsGame.zip)

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
* Anti tampering system for the config file
* Random asteroid shape generation
* Circle-Circle collision detection
* Sound effects
* Shaders

# Screenshots

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/a.png "A")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/b.png "B")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/c.png "C")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/k.png "K")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/d.png "D")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/e.png "E")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/f.png "F")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/g.png "G")

![alt text](https://raw.githubusercontent.com/sbarisic/Asteroids2017/master/screenshots/h.png "H")

# TO-DO

* ~~Shaders, make it look funky~~
* Some kind of power-up system
* Online leatherboards/~~highscores~~
* Load/store key bindings in a file?
* Eye candy, eye candy, eye candy
* Ear candy?
