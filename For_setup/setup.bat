echo off
setlocal
set TOPDIR=C:\\RSDev\\
set PYTHONEXE=%TOPDIR%Python\Python37\python.exe
set PATH=%TOPDIR%asyncCompanion\\For_setup;%TOPDIR%asyncCompanion;%TOPDIR%Python\\Python37\\python37.zip;%TOPDIR%Python\\Python37\\DLLs;%TOPDIR%Python\\Python37\\lib;%TOPDIR%Python\\Python37;%TOPDIR%Python\\Python37\\lib\\site-packages;%TOPDIR%asyncCompanion\\;%TOPDIR%asyncCompanion\\
%PYTHONEXE% %TOPDIR%asyncCompanion\\For_setup\\comp_app_setup.py build
pause
exit