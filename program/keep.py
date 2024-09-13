# keep.py - By: Sakiri - Tue Mar 12 2024
# version: 0.2

from function import cut_picture,get_weather,get_picture,close_browser,check_data
import os,json,datetime,random
import time as ti

'''
需要实现的功能：
    --1，利用无头浏览器提交keep数据  |done| def get_picture
    --2，使用爬虫获取天气数据，提交到keep图像网页  |done| def get_weather
    --3，提交背景图片  |done| def get_picture
    --4，使用opencv覆盖地区信息  |done| def picture
    --5，创建json文件保存并调用默认用户数据  |done| set_user_data.bat & set_data.py
    --6，确认用户是否需要配置头像并返回其路径  |done| def find_avatar |未经测试的功能|
    --7，开启浏览器无头模式  |done|  function.py
    --8，创建批处理文件建立临时环境变量并在指定目录打开py脚本  |done| setup.bat
    --9，下载图片到指定目录  |done| def get_picture
    --10，自动清理临时图像  |done| keep.py 
    --11，批量修改图片属性的创建日期  |待更新|
'''

if __name__=='__main__':
    #获取用户输入|done|
    print('获取用户输入',end=' ')
    user_data_dict=json.load(open('./data/user_data.json','r',encoding='utf-8'))
    name=user_data_dict['user_name']
    school=user_data_dict['school']
    journey_srt=user_data_dict['journey']
    speed_srt=user_data_dict['speed']
    time=user_data_dict['time']#time='18:20'
    times_srt=user_data_dict['times']
    print("\033[96mdone\033[0m")

    #检查输入是否合法|done|
    print('检查输入是否合法',end=' ')
    journey,speed,times=check_data(journey_srt,speed_srt,times_srt)
    print("\033[96mdone\033[0m")

    #处理日期|done|
    print('处理日期',end=' ')
    mode=user_data_dict['mode']
    run_time=[]
    if mode == 'n':
        temp_date=datetime.datetime.now()
        now_date = temp_date.strftime("%Y%m%d")
        run_time.append(now_date)
        nums=times-1
        while nums > 0:
            run_time.append( (temp_date + datetime.timedelta(days=-int(nums))).strftime("%Y%m%d") )
            nums-=1
    elif mode== 'y':
        start_time=user_data_dict['start_time']
        start_time+=' 00:00:00'
        datetime_time=datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        run_time.append(datetime_time.strftime("%Y%m%d"))
        nums=times-1
        while nums > 0:
            run_time.append( (datetime_time + datetime.timedelta(days=-int(nums))).strftime("%Y%m%d") )
            nums-=1
    print("\033[96mdone\033[0m")

    #处理时间|done|
    print('处理时间',end=' ')
    times=len(run_time)
    time_hour_list=[]
    time_min_list=[]
    while times > 0:
        random_time=random.randint(60*int(time[0:2])+int(time[3:5])-30,60*int(time[0:2])+int(time[3:5])+31)
        time_hour_list.append(random_time//60)
        time_min_list.append(random_time%60)
        times-=1
    time_hour_list_str=[str(i) for i in time_hour_list]
    time_min_list_str=[str(i) for i in time_min_list]
    print("\033[96mdone\033[0m")

    #处理天气 |done|
    print('获取天气',end=' ')
    temperatrue_list=[]
    humidity_list=[]
    times=len(run_time)
    while times > 0 :
        #print(run_time[times],time_hour_list_str[times])
        temperatrue,humidity=get_weather(run_time[times-1],time_hour_list_str[times-1])
        temperatrue_list.append(temperatrue[:-1])
        humidity_list.append(humidity[:-1])
        times-=1
    print("\033[96mdone\033[0m")

    #随机处理配速与路程
    print('处理随机配速与路程',end=' ')
    i=len(run_time)
    journey_list=[]
    speed_list=[]
    while i > 0:
        random_journey=random.randint(100*int(journey),100*int(journey)+51)
        random_journey=random_journey/100
        journey_list.append(random_journey)
        random_speed=random.randint(100*int(speed)-50,100*int(speed)+1)
        random_speed=random_speed/100
        speed_list.append(random_speed)
        i-=1
    journey_list_srt=[str(i) for i in journey_list]
    speed_list_srt=[str(i) for i in speed_list]
    print("\033[96mdone\033[0m")

    #print(name,school,journey_list_srt,speed_list_srt,time_min_list_str,time_hour_list_str,temperatrue_list,humidity_list,run_time)
    #xxx sss ['2.32', '2.39'] ['4.68', '4.97'] ['26', '43'] ['18', '18'] ['24', '26'] ['84', '73'] ['20240324', '20240323']

    #发送到KEEPro
    number_of_processing=len(run_time)
    x=0
    while x < number_of_processing:
        inpt_journey=journey_list_srt[x]
        inpt_speed=speed_list_srt[x]
        inpt_min=time_min_list_str[x]
        inpt_hour=time_hour_list_str[x]
        inpt_temperatrue=temperatrue_list[x]
        inpt_humidity=humidity_list[x]
        inpt_date=run_time[x]
        x+=1
        #print(inpt_date,inpt_journey,inpt_speed,inpt_min,inpt_hour,inpt_temperatrue,inpt_humidity,name,school)
        get_picture(inpt_temperatrue,inpt_humidity,inpt_date,inpt_hour,inpt_min,inpt_speed,school,name,inpt_journey)
        ti.sleep(1)
    
        #修改文件信息
        target_char='keep'
        source_files= os.listdir('./output/')

        # print('修改文件信息',end=' ')
        # for file in source_files:
        #     if file.startswith(target_char):
        #         modify_path='./output/'+file
        #         modifyFileTime(modify_path,int(inpt_date[0:4]),int(inpt_date[4:6]),int(inpt_date[6:8]),int(inpt_hour),int(inpt_min),int(random.randint(1,60)))
        # print("\033[96mdone\033[0m")
        

    #关闭浏览器
    print('关闭浏览器',end=' ')
    close_browser()
    print("\033[96mdone\033[0m")
    print('生成图像阶段结束')

    #替换地区信息
    background_path='./data/loco.jpg'
    for file_name in source_files:
        if file_name.startswith(target_char):#判断字符串是否以指定字符串开头
            img_path='./output/'+file_name
            #new_data=datatime.now().data()
            cut_picture(img_path,background_path,file_name.lstrip(target_char))
            print('成功创建图片：'+file_name.lstrip(target_char))

    for filename in os.listdir('./output/'):
        if target_char in filename:
            os.remove('./output/'+filename)
            print(f'删除临时图像{filename}')
    print("\033[93m程序运行结束，お幸せに。😘\033[0m")
    print('请在output目录下查看生成的图片是否符合预期😊')