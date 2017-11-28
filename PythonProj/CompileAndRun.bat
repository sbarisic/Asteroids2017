@echo off
ipyc PythonProj.py /target:exe /standalone /platform:x64
echo Running
PythonProj.exe
pause