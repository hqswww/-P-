# set_data - By: Sakiri - Sat Mar 23 2024
# version: 0.2

import json

def set_data(name,journey,speed,school,time,mode,start_time):
    '''
    保存用户配置
    '''
    user_data={'user_name':name,'school':school,'journey':journey,'speed':speed,'time':time,'times':int(times),'mode':mode,'start_time':start_time}
    with open('user_data.json','w')as f:
        json.dump(user_data,f)

def open_json():
    #打开json
    with open('user_data.json','r',encoding='utf-8') as f:
        load_data=json.load(f)
    return load_data

if __name__=='__main__':
    print(
        '使用须知：\n1，日期将会设置为当前时间，然后向后递减(取决与要创建的图片张数)'
        '\n2，时间设置格式为hour:min(例如18:20)程序将会随机设定分钟前后差值为一小时 例 18:20=17:50~18:50'
        '\n3，路程同理，向后差值0.3km，保留后两位小数'
        '\n4，是否自动决定时间'
        '\n5，如果第一次使用此脚本，需要选择重新创建配置文件')
    print("\033[91m注意!!时间的':'符号必须在英文输入法下输入,不然会报错!!\033[0m")

    modes=input('重新创建信息文件(\033[96m输入d\033[0m) or 只修改某个值(\033[96m输入r\033[0m)')
    while True:
        if modes == "d" or modes == "r":
            break
        else:
            modes=input("\n\033[91m错误的输入，请重新输入有效的选项：\033[0m")

    if modes == 'd':
        #重新创建配置文件
        print("\033[1;35;46m --重新创建配置文件-- \033[0m")
        name=input('输入用户名：')
        journey=input('输入路程：')
        speed=input('输入配速：')
        time=input('输入时间：')
        school=input('输入学校名称(地名)：')
        times=input('创建图片张数：')
        mode=input('是否需要自动计算起点时间(\033[96m输入y or n\033[0m)')

        while True:
            if mode =='y':
                start_time=input('请输入起点时间(年月日，例：2024-01-01)')
                break
            elif mode == 'n':
                start_time=0
                break
            else:
                mode=input("\n\033[91m错误的输入，请重新输入有效的选项：\033[0m")
                continue
        set_data(name,journey,speed,school,time,mode,start_time)
        print('保存用户配置成功 Ciallo~(∠・ω< )⌒☆ 按下任意键退出')

    elif modes == 'r':
        #修改某个数组
        print("\033[1;35;46m --修改一个或多个值-- \033[0m")
        load_data=open_json()
        i=0
        while i == 0:
            print('\n\033[96m当前的数据内容：\033[0m')
            #输出信息内容
            for key,value in dict.items(load_data):
                print(key+':'+str(value))
            #修改内容
            in_key=input('输入需要修改的数据：')
            in_value=input('输入'+in_key+'的新值：')
            load_data[in_key]=in_value
            #保存修改
            with open("user_data.json",'w',encoding='utf-8') as f:
                json.dump(load_data,f,ensure_ascii=False)
            i=input('保存成功,输入\033[91m1\033[0m以退出修改脚本,输入\033[91m0\033[0m则继续修改内容\n')
            i=int(i)
        print('保存用户配置成功 Ciallo~(∠・ω< )⌒☆ 按下任意键退出')