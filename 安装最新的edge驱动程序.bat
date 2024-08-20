chcp 65001

@echo off

::运行keep.py
echo 运行download.py......
cd /d %~dp0
python ./program/download.py

pause