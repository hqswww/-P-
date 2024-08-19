# function - By: Sakiri - Wed Mar 20 2024
# version: 0.2

import requests
from lxml import etree
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time,os,sys
# import win32file, pywintypes
# import datetime

keep_pro='https://tool.joytion.cn/keep/'
save_path=os.getcwd()+r'\output'
#初始化Edge设置
options=webdriver.EdgeOptions()
options.add_argument("--disable-notifications")  # 禁用通知
options.add_argument('--headless')  #无头模式
options.add_argument('--disable-gpu')  #禁用gpu
options.add_experimental_option("prefs", {
    "download.default_directory": save_path,  # 设置默认下载路径
    "download.prompt_for_download": False,  # 禁用下载前询问
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
#初始化浏览器,访问KEEpPro
try:
    bro=webdriver.Edge(options=options)
except:
    print('\n\033[91medge浏览器的版本与此脚本的驱动程序不兼容！\033[0m')
    sys.exit(1)

def cut_picture(bg,img,name):
    '''
    bg:背景图片
    img:要覆盖的图片
    name:保存的名字
    '''
    background = Image.open(bg)
    overlay = Image.open(img)
    position = (0, 1637)  # x和y是覆盖图像在背景图像上的坐标
    background.paste(overlay, position, overlay)
    background.save(r'./output/'+name)

def get_weather(date,time):
    '''
    获取指定时间的温度和湿度
    date:传入纯数字日期 --'20240320'
    time:传入时间(小时) --'18'
    '''
    weather_url=f'https://www.tianqishi.com/shaoguan/{date}.html'
    heads={"UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    #获取页面数据
    response=requests.get(url=weather_url,headers=heads).text
    tree=etree.HTML(response)
    #温度
    temperature=tree.xpath(f'//*[@id="content"]/div[1]/table[2]/tr[{time}]/td[2]/text()')
    #湿度
    humidity=tree.xpath(f'//*[@id="content"]/div[1]/table[2]/tr[{time}]/td[7]/text()')
    return temperature[0] , humidity[0]

def get_picture(temperature,humidity,date,hour,min,journey,school,name,miles):
    '''
    获取图片
    '''
    bro.get(keep_pro)
    print('等待',bro.current_url)
    bro.implicitly_wait(1.5)
    time.sleep(2.5)
    #传入学校名称
    print ("\033[92m传入学校名称\033[0m",end=' ')
    school_name=bro.find_element(By.XPATH,value='//*[@id="inpt_keep_title"]')
    school_name.clear()
    school_name.send_keys(school)
    WebDriverWait(bro,'5')
    print("\033[96mdone\033[0m")
    #传入步数与配速
    print ( "\033[92m传入步数与配速\033[0m",end=' ')
    inpt_miles=bro.find_element(By.XPATH,value='//*[@id="inpt_miles"]')
    inpt_miles.clear()
    inpt_miles.send_keys(miles)
    inpt_speeds=bro.find_element(By.XPATH,value='//*[@id="inpt_speeds"]')
    inpt_speeds.clear()
    inpt_speeds.send_keys(journey)
    WebDriverWait(bro,'5')
    print("\033[96mdone\033[0m")
    #传入温度和湿度
    print ( "\033[92m传入温度和湿度\033[0m",end=' ')
    inpt_temperature=bro.find_element(By.XPATH,value='//*[@id="inpt_temperature"]')
    inpt_temperature.clear()
    inpt_temperature.send_keys(temperature)
    inpt_humidity=bro.find_element(By.XPATH,value='//*[@id="inpt_humidity"]')
    inpt_humidity.clear()
    inpt_humidity.send_keys(humidity)
    WebDriverWait(bro,'5')
    print("\033[96mdone\033[0m")
    #传入日期
    print ( "\033[92m传入日期与时间\033[0m",end=' ')
    inpt_year=bro.find_element(By.XPATH,value='//*[@id="inpt_year"]')
    inpt_year.clear()
    inpt_year.send_keys(date[0:4])
    inpt_month=bro.find_element(By.XPATH,value='//*[@id="inpt_month"]')
    inpt_month.clear()
    inpt_month.send_keys(date[4:6])
    inpt_day=bro.find_element(By.XPATH,value='//*[@id="inpt_day"]')
    inpt_day.clear()
    inpt_day.send_keys(date[6:8])
    inpt_min=bro.find_element(By.XPATH,value='//*[@id="inpt_min"]')
    inpt_min.clear()
    inpt_min.send_keys(min)
    inpt_hour=bro.find_element(By.XPATH,value='//*[@id="inpt_hour"]')
    inpt_hour.clear()
    inpt_hour.send_keys(hour)
    WebDriverWait(bro,'5')
    print("\033[96mdone\033[0m")
    #传入背景图像
    print ( "\033[92m传入背景图像\033[0m",end=' ')
    inpt_bgimg=bro.find_element(by=By.XPATH,value='//*[@id="inpt_bgimg"]')
    inpt_bgimg.send_keys(os.getcwd()+r'\data\keep_backgound.png')
    bro.implicitly_wait(0.5)
    WebDriverWait(bro,'5')
    print("\033[96mdone\033[0m")
    #传入用户名
    print ( "\033[92m传入用户名\033[0m",end=' ')
    user_name=bro.find_element(By.XPATH,value='//*[@id="inpt_username"]')
    user_name.clear()
    user_name.send_keys(name)
    WebDriverWait(bro,'5')
    print("\033[96mdone\033[0m")
    #选择随机路径
    print ( "\033[92m选择随机路径\033[0m",end=' ')
    time.sleep(1)
    inpt_draw=bro.find_element(by=By.XPATH,value='//*[@id="main-div"]/div[2]/ul/div[5]/li[3]/button')
    inpt_draw.click()
    time.sleep(0.5)
    #触发js事件--随机绘图
    bro.execute_script("Json2Draw('https://tool.joytion.cn/generate-track/')")
    time.sleep(1)
    WebDriverWait(bro,'5')
    #yesbot=bro.find_element(by=By.XPATH,value='//*[@id="drawpic_overlay"]/div/div[3]/button[3]')
    #yesbot.click()
    bro.execute_script('drawpic_yesbtn_onClick()')
    WebDriverWait(bro,'5')
    time.sleep(1)
    print("\033[96mdone\033[0m")
    #传入头像文件
    path,avatar_bool=find_avatar('avatar')
    if avatar_bool:
        inpt_avatar=bro.find_element(by=By.XPATH,value='//*[@id="inpt_portrait"]')
        inpt_avatar.send_keys(path)
        WebDriverWait(bro,'5')
    #下载图片到指定位置
    bro.implicitly_wait(0.5)
    #触发js事件--下载图片
    bro.execute_script('Download(Download1)')
    # download_button=bro.find_element(by=By.XPATH,value='//*[@id="main-div"]/div[2]/ul/button')
    # download_button.click()
    time.sleep(1)
    print('保存成功，等待执行cut_picture')
        
    
def find_avatar(need_find_name):
    '''
    检测是否存在图像文件，并返回其路径和状态
    '''
    for root , dirs , files in os.walk('./data'):
        for file in files:
            file_name,ext=os.path.splitext(file)
            if file_name == need_find_name:
                return os.path.join(root,file),True
    return '没有找到需要更改的头像文件，跳过inpt_avatar',False

def close_browser():
    bro.close()

def check_data(journey,speed,times):
    '''
    检查输入的字段是否合法，将浮点数转化为整数
    '''
    #str to float
    journey_float=float(journey)
    speed_float=float(speed)
    times_float=float(times)
    #float to int
    int_journey=int(journey_float)
    int_speed=int(speed_float)
    int_times=int(times_float)

    return int_journey,int_speed,int_times

# def modifyFileTime(file_path,year,month,day,hour,min,second):
#     '''
#     file_path:图片地址
#     create_modify_time:格式：2021-10-01 12:00:00
#     '''
#     #打开要修改的文件
#     handle = win32file.CreateFile(file_path, win32file.GENERIC_WRITE,
#                                 win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
#                                 None, win32file.OPEN_EXISTING,
#                                 win32file.FILE_ATTRIBUTE_NORMAL, None)

#     # 设置文件的创建时间和修改时间
#     dt=datetime.datetime(year, month, day, hour, min, second)
#     date_time = pywintypes.Time(dt)
#     win32file.SetFileTime(handle, date_time, date_time, None)

    # 关闭文件句柄
    handle.close()