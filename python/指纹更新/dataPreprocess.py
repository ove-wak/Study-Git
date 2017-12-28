# -*- coding: UTF-8 -*-
import xlrd,os,time
from pymatbridge import Matlab

sheet = 0 # 单ap训练,定义ap序号

class DataPreprocess:
    def __init__(self):
        file = xlrd.open_workbook('excel/底图.xls')
        table = file.sheets()[sheet]  #通过索引顺序获取工作表
        nrows = table.nrows #行数
        self.ditu = []
        for i in range(1,nrows):
            self.ditu.append(table.row_values(i)[1:])

    # 生成中间数据
    def get_median(self):
        for j in range(1,20):
            file = xlrd.open_workbook('excel/'+str(j)+'.xls')
            table = file.sheets()[sheet]  #通过索引顺序获取工作表
            nrows = table.nrows #行数
            data = []
            for i in range(1,nrows):
                data.append(table.row_values(i)[1:])
            with open('中间数据/'+str(j)+'.txt','wt') as f:
                for y in range(len(data)):
                    for x in range(len(data[0])):
                        if int(data[y][x]) != 0 and int(self.ditu[y][x]) !=0:
                            f.write(str(data[y][x]/self.ditu[y][x] - 1)+" "+str(x)+" "+str(y)+"\n")

    def get_none(self):
        with open('中间数据/none.txt','wt') as f:
            for y in range(13):
                for x in range(10):
                    f.write(str(0)+" "+str(x)+" "+str(y)+"\n")

    def training(self):
        
        mlab = Matlab()
        mlab.start()
        #res = mlab.run_func('C:/Users/ovewa/Desktop/git-storage/OS-ELM-matlab/OSELM_initial_training.m', '中间数据/1.txt',10,'sin',nargout=5)
        # IW, Bias, M, beta, TrainingTime = res['result']
        res = mlab.run_func('C:/Users/ovewa/Desktop/git-storage/OS-ELM-matlab/OSELM_get_value.m','中间数据/all.txt','中间数据/none.txt',10,'sin',19,18)
        result = res['result']
        # print(result)
        y = 0
        data = [[0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0]]

        for x in range(len(result)): 
            data[x%10][y] = int(self.ditu[y][x%10]*(result[x]+1))
            print(data[x%10][y],end=" ")
            if (x+1)%10 == 0:
                print() 
                y=y+1
        mlab.stop()

# 测试环境下运行
if __name__ == "__main__":
    d = DataPreprocess()
    d.training()