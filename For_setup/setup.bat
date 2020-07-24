:: These are comment lines for .bat.
:: This command turns off print display in console
@echo off
:: This command makes any variable assignments temporary for duration of this program
setlocal

:: EDIT THESE VARIABLES AS NEEDED
:: ******************************************
:: Set APPDIR to your project parent dir
set APPDIR=C:\RSDev\
:: Set PYTHONDIR to your python directory.
set PYTHONDIR=%APPDIR%Python\Python37\
:: Set PYTHONEXE to your python executable.
set PYTHONEXE=%PYTHONDIR%python.exe
:: ******************************************

:: This sets the required path for this script using APPDIR and PYTHONDIR
set PATH=%APPDIR%asyncCompanion\For_setup;%APPDIR%asyncCompanion;%PYTHONDIR%python37.zip;%PYTHONDIR%DLLs;%APPDIR%lib;%PYTHONDIR%;%PYTHONDIR%lib\site-packages;%APPDIR%asyncCompanion\;%APPDIR%asyncCompanion\
:: This command runs the build process for the app.
%PYTHONEXE% %APPDIR%asyncCompanion\For_setup\comp_app_setup.py build
:: This command pauses at the end of the build process.
pause