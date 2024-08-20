::更改字符编码为UTF-8
chcp 65001

@echo off

::将当前目录设置为临时环境变量
set MY_VAR=%CD%
echo 当前目录是：%MY_VAR%

::运行keep.py
echo 运行keep.py......
::echo 为了脚本执行性能，请定时清理output下的图像()
echo (如果长时间无法继续运行，请尝试下载相应的edge浏览器驱动，并覆盖旧驱动)
cd /d %~dp0
python ./program/keep.py

pause