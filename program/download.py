# download - By: Sakiri - Tue Aug 20 2024
# version: 0.1

import requests
from lxml import etree
import os,zipfile,sys

def unzip_file(zip_file_path, extract_to_path):
    #解压文件
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)

#检测当前文件夹是否存在msedgedriver.exe
file_path='./program/msedgedriver.exe'
if os.path.exists(file_path):
    os.remove(file_path)

driver_url='https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/?form=MA13LH'

heads={
    "UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
}

print('正在解析现最新版本的版本号...',end=' ')
response=requests.get(url=driver_url,headers=heads).text
tree=etree.HTML(response)
driver_list=tree.xpath('//*[@id="main"]/div/div[1]/section[4]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/text()')
#print(driver_list)#['\n                    127.0.2651.105\n\n                    ']
version=driver_list[0][21:35]
print(f"\033[96mdone! \n准备下载版本为-{version}-的驱动程序\033[0m")
download_url=f'https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip'

print('正在向服务器发送请求...',end=' ')
driver=requests.get(download_url,heads).content
zip_path='./program/msedgedriver.zip'
with open(zip_path,'wb') as f:
    f.write(driver)
print("\033[96mdone!\033[0m")

print('正在解压缩...',end=' ')
# 解压缩文件
unzip_file(zip_path,'./program/')
print("\033[96mdone\033[0m")

#检测当前文件夹是否存在msedgedriver.exe
file_path='./program/msedgedriver.exe'
if os.path.exists(file_path):
    os.remove('./program/msedgedriver.zip')
else:
    print('\n\033[91m下载异常，请检查网络环境\033[0m')
    sys.exit(1)

print('\033[92m下载完成！🎉🎉🎉\033[0m')