import csv

time = []#时间戳列表
wifi_content = []#wifi列表
time_diff = []#时间差列表
time_diff_add = []#时间差位置列表
filename = "4"
filefolder = "Samsung/"
wifi_mac = []
with open('raw_data/b'+filename+'_t.csv') as f: 
    f_csv = csv.reader(f)
    #headers = next(f_csv) #新数据从第一行开始 
    for row in f_csv:
        time_diff.append(int(row[0]) - 2000)#前后延长两秒
        time_diff.append(int(row[1]) + 2000)

with open(filefolder + filename+'.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    wifi_mac = headers[1:] 
    for row in f_csv:
        if row[0] != '':
            time.append(int(row[0]))
        else:
            time.append(-1)
        wifi_content.append(row[1:])

diff = 0
len_time = len(time)
len_time_diff = len(time_diff)
for x in range(len_time):
        while diff < len_time_diff and time[x] > time_diff[diff]:
                time_diff_add.append(x)
                diff = diff + 1
while len(time_diff_add) < len_time_diff:
    time_diff_add.append(-1)

for x in range(len(wifi_content)):
    for y in range(len(wifi_content[0])):
        if wifi_content[x][y] == "":
            wifi_content[x][y] = -95
        else:
            wifi_content[x][y] = int(wifi_content[x][y])
wifi_change = []
for x in range(0,len(time_diff_add),2):
    if time_diff_add[x+1] == -1 or time_diff_add[x+1] == 0:
        wifi_change.append(-1)
        wifi_change.append(-1)
    elif time_diff_add[x] == time_diff_add[x+1]:
        wifi_change.append(wifi_content[time_diff_add[x] - 1])
        wifi_change.append(wifi_content[time_diff_add[x+1]])
    else:
        wifi_change.append(wifi_content[time_diff_add[x]])
        wifi_change.append(wifi_content[time_diff_add[x+1]])
wifi_change_new = []
for y in range(0,len(wifi_change),2):
    temp = 0
    if wifi_change[y] == -1:
        wifi_change_new.append(-1)
    else:
        wifi_change_new.append([])
        for x in range(len(wifi_change[y])):
            if abs(wifi_change[y][x] - wifi_change[y+1][x]) > 10:
                if wifi_change[y][x] > -75 or wifi_change[y+1][x] > -75:
                    wifi_change_new[int(y/2)].append([wifi_change[y][x],wifi_change[y+1][x],wifi_mac[x]]) 
wifi_change_new_sort = []
for x in wifi_change_new:
    if x == -1:
        wifi_change_new_sort.append(-1)
        wifi_change_new_sort.append(-1)
        wifi_change_new_sort.append(-1) 
    else:
        wifi_change_new_sort.append([])
        wifi_change_new_sort.append([])
        wifi_change_new_sort.append([])
        x.sort(reverse=True)
        for y in x:
            wifi_change_new_sort[len(wifi_change_new_sort)-3].append(y[2])
            wifi_change_new_sort[len(wifi_change_new_sort)-2].append(y[0])
            wifi_change_new_sort[len(wifi_change_new_sort)-1].append(y[1])
#print(wifi_change_new_sort)

with open(filefolder + 'wifi_'+filename+'.csv','w', newline='') as f:##如果不加newline,存的文件里每隔一行会多一个空行
    f_csv = csv.writer(f)
    f_csv.writerow([['time'],['wifi_change']])#如果直接传入字符串的话,该方法会把每个字符作为单个列表元素来处理
    num = 1
    for x in range(int(len(time_diff)/2)):
        if wifi_change_new_sort[3*x] == -1:
            f_csv.writerow([num] + [wifi_change_new_sort[3*x]])
            num = num + 1
            f_csv.writerow([str(time_diff[2*x])] + [wifi_change_new_sort[3*x+1]])
            f_csv.writerow([str(time_diff[2*x+1])] + [wifi_change_new_sort[3*x+2]])
        else:
            f_csv.writerow([num] + wifi_change_new_sort[3*x])
            num = num + 1
            f_csv.writerow([str(time_diff[2*x])] + wifi_change_new_sort[3*x+1])
            f_csv.writerow([str(time_diff[2*x+1])] + wifi_change_new_sort[3*x+2])

    f_csv.writerow(['注释:-1表示无法判断;-95的值是对空值的标准化;每两行为一组数据,同一组内去除了相差不大于10的值,去除了信号一直微弱(-75为标准)的值,并对剩下的值排序.时间前后延长两秒'])
