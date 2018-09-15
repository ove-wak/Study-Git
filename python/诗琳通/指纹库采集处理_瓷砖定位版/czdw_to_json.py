import os,csv,time,json,numpy

# 通过瓷砖匹配所有位置
def data_with_cz():
    room = ""
    print("四位空间号输入‘00000’结束位置匹配")
    while room != "00000":
        room = input("四位空间号:")
        if room == "00000":
            break
        x_1 = float(input("1号点实际x坐标:")) # 此处的x对应地图的E
        y_1 = float(input("1号点实际y坐标:")) # 此处的y对应地图的N
        x_2 = float(input("2号点实际x坐标:"))
        y_2 = float(input("2号点实际y坐标:"))
        direc_y = input("y方向:") # 输入'+'或者'-'
        files = os.listdir("Wi-Fi_Data/")
        for file in files:
            if room in file:
                room = file
                break
        x = int(room.split("_")[1])
        y = int(room.split("_")[2])
        files = os.listdir("Wi-Fi_Data/"+room)
        if len(files) > x*y:
            print(room+"  error")
            break
        else:
            temp_x = 0.0
            temp_y = 0.0
            direc_x = ""
            dt = 0.0
            if x == 1:# 当MAX_x只有1时，沿y轴直接计算
                for i in range(len(files)):        
                    if i == 0:
                        temp_x = x_1
                        temp_y = y_1
                    elif i == 1:
                        temp_x = x_2
                        temp_y = y_2
                        dt = abs(y_2 - y_1)
                    else:
                        if direc_y == "+":
                            y_t = dt
                        else:
                            y_t = 0 - dt 
                        temp_y = temp_y + y_t
                    file_name = str(i+1).zfill(5)+"_"+str(round(temp_x,3))+"_"+str(round(temp_y,3))+".csv"
                    os.rename("Wi-Fi_Data/"+room+"/"+files[i],"Wi-Fi_Data/"+room+"/"+file_name)
                    os.rename("BT_Data/"+room+"/"+files[i],"BT_Data/"+room+"/"+file_name)
            else:
                for i in range(len(files)): 
                    if i == 0:
                        temp_x = x_1
                        temp_y = y_1
                    elif i == 1:
                        temp_x = x_2
                        temp_y = y_2
                        dt_x = x_2 - x_1
                        dt = abs(dt_x)
                        if dt_x > 0:
                            direc_x = "+"
                        else:
                            direc_x = "-"
                    else:
                        if i % x == 0:
                            if direc_y == "+":
                                x_t = 0
                                y_t = dt
                            else:
                                x_t = 0
                                y_t = 0 - dt
                        else:
                            y_t = 0 
                            if (i//x) % 2 == 0:
                                if direc_x == "+":
                                    x_t = dt
                                else:
                                    x_t = 0 - dt
                            else:
                                if direc_x == "+":
                                    x_t = 0 - dt
                                else:
                                    x_t = dt
                        temp_x = temp_x + x_t
                        temp_y = temp_y + y_t
                    file_name = str(i+1).zfill(5)+"_"+str(round(temp_x,3))+"_"+str(round(temp_y,3))+".csv"
                    os.rename("Wi-Fi_Data/"+room+"/"+files[i],"Wi-Fi_Data/"+room+"/"+file_name)
                    os.rename("BT_Data/"+room+"/"+files[i],"BT_Data/"+room+"/"+file_name)

# 指纹数据转为json格式
def data_to_json(dir_path,building_id):
    data = []
    point_num = 0
    # 获取文件夹列表
    dir_names = [name for name in os.listdir(dir_path)]
    for dir_name in dir_names:
        room_name = dir_name.split("_")[0]
        floor_id = room_name[:2]
        # 显示进度
        print("正在处理 "+room_name + " 下的文件")
        begin_time = time.time()
        file_names  =  [name for name in os.listdir(dir_path+dir_name)]  
        for file_name in file_names:
            file_num = file_name.split("_")[0]
            coo_x = file_name.split("_")[1]
            coo_y = (file_name.split("_")[2])[:-4]
            path = dir_path+dir_name+"/"+file_name
            if os.path.getsize(path):#判断文件是否为空  
                pt = {} 
                pt['Point NO'] = point_num
                pt['PosLon'] = float(coo_x)
                pt['PosLat'] = float(coo_y)
                pt['Building ID'] = building_id
                pt['Floor ID'] = floor_id
                pt['WIFIscan'] = []
                point_num = point_num + 1 
                with open(path, 'rt', encoding='utf-8') as file_read:
                    line_datas = []
                    read = csv.reader(file_read)
                    for i in read:
                        line_datas.append(i)
                    name = line_datas[0][1:]
                    # print(name)
                    mac = line_datas[1][1:]
                    for x in range(2,len(line_datas)):
                        round_num = x - 1
                        line_data = line_datas[x]
                        line_timet = line_data.pop(0)
                        line_time = line_timet[:-3]
                        line_time = time.strftime("%y-%m-%d %H:%M:%S",time.localtime(int(line_time)))
                        if round_num == 1:
                            pt['Date'] = line_time
                        ap = line_data
                        ap_num = 0
                        record = []
                        for i in range(len(ap)):
                            if int(ap[i]) != -200:
                                if name[i] == "null":
                                    name[i] = ""
                                record.append({'AP':ap_num,'BSSID':mac[i],'SSID':name[i],'Level':int(ap[i])})
                                ap_num = ap_num + 1
                        if ap_num != 0:
                            pt['WIFIscan'].append({'Round':round_num,'Date':line_time,'WifiScanInfo':record})
                data.append(pt) 
        end_time = time.time()
        print(room_name + " 下的文件处理完成("+str(int((begin_time-end_time)/1000))+"s)")
    return data

print("程序开始执行.")
data_with_cz()
print("位置和指纹匹配完成.")
building_id = input("请输入建筑名称:")
wifi_path = "Wi-Fi_Data/"
bt_path = "BT_Data/" 
print("wifi指纹正在转为json格式.")
data = data_to_json(wifi_path,building_id)
print("json文件正在保存中,请稍等...")
with open(building_id+'_wifi.json', 'w') as f:
    json.dump(data, f)
print("wifi指纹转为json格式完成.\n\n\n\n\n\n\n\n")
print("蓝牙指纹正在转为json格式.")
data = data_to_json(bt_path,building_id)
print("json文件正在保存中,请稍等...")
with open(building_id+'_bt.json', 'w') as f:
    json.dump(data, f)
print("蓝牙指纹转为json格式完成.")
print("程序执行完毕.")
os.system("pause")