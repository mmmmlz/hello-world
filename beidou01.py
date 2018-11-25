
from tkinter import *
from tkinter import filedialog 
import re
import time as t


root = Tk()
root.geometry('730x260+500+200')
root.title('北斗定位位置解析')
root.iconbitmap('Icon.ico')
def search():
    fileName=filedialog.askopenfilename()

    file_name.set(fileName)
def searching(event):
    information.set('处理中。。。')
def pick():
    pass
def location():
    filename = file_name.get()

    filename=filename[2:-3]

    GGA_line = 'GBGGA'
    information.set('处理完成')
    t.sleep(1.5)
    with open(filename, encoding='UTF-8') as f_read:
        for gga in f_read:
            if GGA_line in gga:
                break
        print(gga)
        list_gga = gga.split(',')
        # 时间
        time_info = list_gga[0]
        time_info = time_info.split()[0]
        time.set(time_info)
        # 纬度
        wd_info1 = list_gga[2]
        wd_info2 = list_gga[3]
        wd_info = wd_info1 +'-'+ wd_info2
        weidu.set(wd_info)
        # 经度
        jd_info1 = list_gga[4]
        jd_info2 = list_gga[5]
        jd_info = jd_info1 + '-'+ jd_info2
        jindu.set(jd_info)
        # 海拔高度
        gd_info1 = list_gga[9]
        gd_info2 = list_gga[10]
        gd_info = gd_info1 + '-' + gd_info2
        gaodu.set(gd_info)
        print(list_gga)






file_name = StringVar()
file_name.set('')
lb1 = Listbox(root,listvariable=file_name,height=1,width=30)
lb1.grid(row=0, column=0)
bt1 = Button(root, text="打开位置信息文件", width=20, command=search)
bt1.bind('<Button-1>')
bt1.grid(row=0, column=1)

bt2 = Button(root, text="开始定位", width=10, command=location)
bt2.bind('<Button-1>', searching)
bt2.grid(row=1, column=1)

information = StringVar()
information.set(' ')
info = Label(root,textvariable=information).grid(row=1, column=2, sticky=W)
# 时间
time = StringVar()
time.set('')
lb1 = Listbox(root,listvariable=time,height=1)
lb1.grid(row=2, column=0)

information1 = StringVar()
information1.set('定位时间')
info = Label(root,textvariable=information1).grid(row=2, column=1, sticky=W)
# 纬度
weidu = StringVar()
weidu.set('')
lb1 = Listbox(root,listvariable=weidu,height=1)
lb1.grid(row=3, column=0)

information2 = StringVar()
information2.set('纬度')
info = Label(root,textvariable=information2).grid(row=3, column=1, sticky=W)
# 经度
jindu = StringVar()
jindu.set('')
lb1 = Listbox(root,listvariable=jindu,height=1)
lb1.grid(row=4, column=0)

information3 = StringVar()
information3.set('经度')
info = Label(root,textvariable=information3).grid(row=4, column=1, sticky=W)

# 高度
gaodu = StringVar()
gaodu.set('')
lb1 = Listbox(root,listvariable=gaodu,height=1)
lb1.grid(row=5, column=0)

information4 = StringVar()
information4.set('海拔')
info = Label(root,textvariable=information4).grid(row=5, column=1, sticky=W)


mainloop()
