import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.axisartist as axisartist
from scipy.interpolate import make_interp_spline
import os
from itertools import islice
from pathlib import Path
import re
import string
import pandas as pd
from scipy.stats.distributions import norm#随机数高斯分布
from scipy.optimize import curve_fit#拟合函数

def ExpFunc(x, L, ADC_0):
    return ADC_0*np.exp(-x/L)

def getmean(initialfile):
    Alldata = np.loadtxt(initialfile)
    # print(Alldata)
    pedestal = Alldata[-1,1]#局域变量被限制了，后续需要考虑改变
    Alldata_cut = Alldata[0:-2]#将最后一行pedestal数据去除
    # print(Alldata_cut)
    # print(pedestal)
    ExcelAlldata_cut = pd.DataFrame(Alldata_cut)#转化为excel文件
    # print(ExcelAlldata_cut)
    ExcelAlldata_cut = ExcelAlldata_cut.groupby(0).mean()#以第一行数据为组取均值
    # print(ExcelAlldata_cut)
    meandata = ExcelAlldata_cut.to_csv('D:\\STUDY-think\\Data\\LAB-AL-EX-data\\meandata\\{}.txt'.format(meandataname),sep='\t')#后续需要保留三位小数#将处理好的excel保存为txt
    # print(meandata)

def ALfit(meandatafile):
    x = []
    y = []
    sigma = []
    fitylist = []
    pedestal = 273
    with open(meandatafile,'r') as f:
        lines = f.readlines()
        linesdata = lines[1:-1]
        # print(linesdata)
    for line in linesdata:
        value = [float(s) for s in line.split()]
        x.append(value[0])
        y.append(value[1])
        sigma.append(value[2])
        # print(x,y,sigma)

    for eachy in y:#获取误差棒数据
        yerr = np.zeros([2,len(y)])
        yerr[0,:] = float((eachy-eachy*(0.9974))/3000)
        yerr[1,:] = float((eachy-eachy*(0.9974))/3000)
        # print(yerr)

    plt.rcParams['font.sans-serif'] = ['simHei']

    fig,ax1 = plt.subplots()
    normy = (np.array(y) - pedestal)/3000#将数据归一化
    # print(normy)
    ax1.set_xlim([0,1])
    ax1.set_ylim([0.85,0.9])
    initial_LvADC = (x[-1]*y[0]-x[0]*y[-1])/(x[-1]-x[0])#初始液位ADC
    estimate_AL = initial_LvADC*(x[-1]-x[0])/(y[0]-y[-1])#预估衰减长度
    # print(estimate_AL,initial_LvADC)

    popt,pcov = curve_fit(ExpFunc,x,y,sigma=sigma,p0=[estimate_AL,initial_LvADC],bounds=([0, 0], [100, 4096]))#拟合函数
    # print(popt,pcov)
    for xvalue in x:#得到拟合ADC的列表
        ADC_xvalue = ExpFunc(xvalue,popt[0],popt[1])
        # print(ADC_xvalue)
        normADC_xvalue = round((ADC_xvalue-pedestal)/3000,3)
        # print(normADC_xvalue)
        fitylist.append(normADC_xvalue)
    # print(fitylist)
    Real_AL = round(popt[0],3)
    s= np.sqrt(np.diag(pcov))
    s= round(sigma[0],3)
    # print(Real_AL,s)

    for realy,fity in zip(y,fitylist):#计算\ka^2
        kafang = (realy-(fity*3000))**2/(fity*3000)  
        kafang += kafang
        finalkafang = round(kafang,3)
        # print(finalkafang)
    kafangbiNDF = round(finalkafang/len(x),3)
    
    ax1.set_xlabel("Liquid level(m)")
    ax1.set_ylabel('Normalization ADC')
    ax1.grid()

    # ax1.plot(x,y,'.', ms=6,color='b',label='Normalization ADC value')#画实际ADC分布点
    ax1.plot(x,normy,'.',ms=6,color='b',label='Normalization ADC value')#画归一化ADC分布点
    ax1.plot(x,fitylist,linewidth=2,color='r',label='fit curve')#画拟合曲线
    ax1.errorbar(x,normy,yerr=yerr[:,:],ecolor='g',marker='s',capsize=3,capthick=1,linestyle='none')#画出误差棒

    fig.legend(loc="upper right")
    plt.annotate('AL:{}'.format(Real_AL)+r'$\pm$'+'{}'.format(s)+'m'+'\n'+r'$\chi^{2}/NDF$'+'={}'.format(kafangbiNDF),xy=(0.7,0.895),bbox=dict(boxstyle='round',fc='0.8'))#设置AL标注

    plt.savefig('D:\STUDY-think\Data\LAB-AL-EX-data\ALfig\\{}.png'.format(figname),dpi=800)#保存图片

    plt.clf()
    return x,y,sigma,fitylist


p1 = Path('D:\\STUDY-think\\Data\\LAB-AL-EX-data\\ADC-data')
p2 = Path('D:\\STUDY-think\\Data\\LAB-AL-EX-data\\meandata')

filelist1 = []
for p1filename in p1.rglob('*.txt'):
    filelist1.append(str(p1filename))
    # print(p1filelist)
    # #把全部文件名字存入列表

for initialfile in filelist1:
    meandataname = initialfile[43:-4]
    # print(meandataname)#获得保存文件的名字
    meandata = getmean(initialfile)
    #调用获取液面数据的平均值函数，保存到另一个文件夹的txt文本

filelist2 = []
for p2filename in p2.rglob('*.txt'):
    filelist2.append(str(p2filename))
    # print(p2filelist)
    #将上一步文件夹中文件的文件名存入列表

for meandatafile in filelist2:
    figname = meandatafile[43:-4]
    # print(figname)
    fig = ALfit(meandatafile)
    #调用拟合函数对数据拟合和画图

