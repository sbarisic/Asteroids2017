@echo off
rmdir /S /Q temp_folder

mkdir temp_folder
mkdir temp_folder\AsteroidsGame\
xcopy /E /Y python_bin temp_folder\AsteroidsGame\

mkdir temp_folder\AsteroidsGame\Asteroids
xcopy /E /Y bin temp_folder\AsteroidsGame\Asteroids\

del temp_folder\AsteroidsGame\Asteroids\data.cfg

echo start AsteroidsGame\pythonw.exe AsteroidsGame\Asteroids\PythonProject.py > temp_folder\Start_Asteroids.bat

del AsteroidsGame.zip
7z a AsteroidsGame.zip .\temp_folder\*
rmdir /S /Q temp_folder