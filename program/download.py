# download.py - By: Sakiri - Tue Aug 20 2024
# version: 0.2

import requests
from lxml import etree
import os,zipfile,sys,time
import win32com.client
from contextlib import closing

driver_url='https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/?form=MA13LH'

heads={
    "UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
}

browser_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def unzip_file(zip_file_path, extract_to_path):
    #解压文件
    try :
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
    except zipfile.BadZipFile as e:
        print(f'解压包错误！{e}')
        sys.exit(1)

def remove_drivers():
    #删除msedgedriver.exe
    file_path='./program/msedgedriver.exe'
    if os.path.exists(file_path):
        os.remove(file_path)

def get_drivers_version():
    """
    获取目前浏览器驱动程序最新版本
    """
    print('正在解析现最新版本的版本号...\n')
    response=requests.get(url=driver_url,headers=heads).text
    tree=etree.HTML(response)
    driver_list=tree.xpath('//*[@id="main"]/div/div[1]/section[4]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/text()')
    #print(driver_list)#['\n                    127.0.2651.105\n\n                    ']
    return driver_list[0][21:34]

def get_exe_version(exe_path):
    """
    获取本地浏览器版本
    """
    try:
        wmi = win32com.client.GetObject('winmgmts:')
        exe_path = exe_path.replace('\\', '\\\\')
        query = "SELECT * FROM CIM_DataFile WHERE Name='{}'".format(exe_path)
        for file in wmi.ExecQuery(query):
            return file.Version

    except Exception as e:
        print(f"Error: {e}")
        return None

def down_load(file_url, file_path):
    '''
    文件下载器
    '''
    start_time = time.time()  # 文件开始下载时的时间
    with closing(requests.get(file_url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(file_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                speed = data_count / 1024 / (time.time() - start_time)
                print("\r 文件下载进度：%d%%(%d/%d) 文件下载速度：%dKB/s - %s"
                      % (now_jd, data_count, content_size, speed, file_path), end=" ")

def download_drivers(version):
    #下载驱动程序zip
    print(f"\033[96m准备下载版本为-{version}-的驱动程序\033[0m")
    download_url=f'https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip'

    print('正在向服务器发送请求...',end=' ')
    zip_path='./program/msedgedriver.zip'
    down_load(download_url,zip_path)
    print("\033[96mdone!\033[0m")

    print('正在解压缩...',end=' ')
    # 解压缩文件
    unzip_file(zip_path,'./program/')
    print("\033[96mdone\033[0m")

    #检测当前文件夹是否存在msedgedriver.exe
    file_path='./program/msedgedriver.exe'
    if os.path.exists(file_path):
        os.remove('./program/msedgedriver.zip')
        print('\033[92m下载完成！🎉🎉🎉\033[0m')
    else:
        print('\n\033[91m解压缩异常！！\033[0m')
        sys.exit(1)

def compare_version(browser_version,driver_version):
    #比较版本号
    if int(browser_version[:3]) == int(driver_version[:3]):
        print('主版本号相同，更新驱动程序后即可正常使用')
    elif int(browser_version[:3]) < int(driver_version[:3]):
        print('更新后如果仍然出现问题，请更新浏览器至最新版本')
    else :
        print('ERROR!')
        sys.exit(1)

if __name__=='__main__':
    remove_drivers()

    browser_version = get_exe_version(browser_path)
    if browser_version:
        print(f'当前浏览器版本为\033[96m{browser_version}\033[0m')
    else:
        print("获取版本失败，可能的原因可能是当前电脑没有安装Microsoft Edge浏览器或者更改了安装路径")
        sys.exit(1)

    driver_version = get_drivers_version()
    print(f'当前驱动程序的版本为\033[96m{driver_version}\033[0m')

    compare_version(browser_version,driver_version)
    print(driver_version)
    download_drivers(driver_version)