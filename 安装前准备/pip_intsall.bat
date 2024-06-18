@echo off
:: 设置编码为UTF-8
chcp 65001

:: 升级pip
echo 正在升级pip...
python -m pip install --upgrade pip
echo pip升级完成。

echo 下载需要的库/组件
::pip install
pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install lxml -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple

echo 安装完成。
:: 暂停批处理文件，以便查看输出结果
pause