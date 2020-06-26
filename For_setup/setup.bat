:: These are comment lines for .bat.
:: Turn off print display in console
@echo off
:: Make any variable assignments temporary such as PATH
setlocal
:: Set APPDIR to your project parent dir
set APPDIR=C:\RSDev\
:: Set PYTHONDIR to your python directory.
set PYTHONDIR=%APPDIR%Python\Python37\
:: Set PYTHONEXE to your python executable.
set PYTHONEXE=%PYTHONDIR%python.exe
:: This sets the required path for this script using APPDIR and PYTHONDIR
set PATH=%APPDIR%asyncCompanion\For_setup;%APPDIR%asyncCompanion;%PYTHONDIR%python37.zip;%PYTHONDIR%DLLs;%APPDIR%lib;%PYTHONDIR%;%PYTHONDIR%lib\site-packages;%APPDIR%asyncCompanion\;%APPDIR%asyncCompanion\
:: This command runs the build process for the app.
%PYTHONEXE% %APPDIR%asyncCompanion\For_setup\comp_app_setup.py build
:: This command pauses at the end of the build process.
pause