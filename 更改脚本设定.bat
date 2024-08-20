::更改字符编码为UTF-8

@REM 代码页 描述

@REM 65001   UTF-8代码页

@REM 950繁体中文

@REM 936简体中文默认的GBK

@REM 437 MS-DOS美国英语

@REM 但是通过CHCP设置编码是治标不治本的

@REM 想永久的更改cmd编码值需要修改注册表

chcp 65001

@echo off

::运行keep.py
echo 运行set_data.py......
cd /d %~dp0
python ./program/set_data.py

pause