@echo off
:: 设置编码为UTF-8
chcp 65001

::将当前目录设置为临时环境变量
set MY_VAR=%CD%
echo 当前目录是：%MY_VAR%

::切换到当前目录
echo 切换到当前目录
cd /d %~dp0

::打开安装说明
echo 打开安装说明
start notepad "%MY_VAR%\installation_instructions.txt" 

::安装装python运行环境
echo 运行python安装程序
python-3.11.8-amd64

:: 升级pip
echo 正在升级pip...
python -m pip install --upgrade pip
echo pip升级完成。

echo 下载需要的库/组件
::pip install
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo 安装完成。

pause
