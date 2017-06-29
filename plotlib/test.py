#coding=utf-8
import os
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import datetime  

def show_k_pic(code):
    file_name = code + '_hist_d.csv'
    f = os.path.join(os.getcwd(), 'hist_data', 'day', file_name)
    hist_data = DataFrame.from_csv(f)
    # 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式  
    data_list = [] 

    # row has format (index, dataframe.series). So row[1] is the needed series
    for row in hist_data.iterrows():
        row = row[1]
        #print row.date
        #print row[1:5]
        date = row.date
        # 将时间转换为数字  
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d')  
        t = date2num(date_time)  
        open, close, high, low = row[1:5]  
        datas = (t,open,high,low,close)  
        data_list.append(datas)  
    
    # 创建子图  
    fig, ax = plt.subplots()  
    fig.subplots_adjust(bottom=0.2)  
    # 设置X轴刻度为日期时间  
    ax.xaxis_date()  
    plt.xticks(rotation=45)  
    plt.yticks()
    title = "code: " + code
    plt.title(title)  
    plt.xlabel("time")  
    plt.ylabel("price")  
    mpf.candlestick_ohlc(ax,data_list,width=1,colorup='r',colordown='green')  
    plt.grid()
    plt.show()

if __name__ == "__main__":
    show_k_pic('000001')
