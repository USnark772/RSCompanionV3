echo off
setlocal
set APPDIR=C:\\RSDev\\
set PYTHONDIR=%APPDIR%Python\\Python37\\
set PYTHONEXE=%PYTHONDIR%python.exe
set PATH=%APPDIR%asyncCompanion\\For_setup;%APPDIR%asyncCompanion;%PYTHONDIR%python37.zip;%PYTHONDIR%DLLs;%APPDIR%lib;%PYTHONDIR%;%PYTHONDIR%lib\\site-packages;%APPDIR%asyncCompanion\\;%APPDIR%asyncCompanion\\
%PYTHONEXE% %APPDIR%asyncCompanion\\For_setup\\comp_app_setup.py build
pause