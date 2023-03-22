from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox
import PIL.Image, PIL.ImageTk
from tkinter import ttk
from tkinter import *
import tkinter as tk
import ctypes as ct
import csv

#f = open('datapath.txt', 'r')
#ชื่อไฟล์ CSV

#f = open('datapath.txt', 'r')
#ชื่อไฟล์ CSV
f = open('datapath.txt', 'r')
#ชื่อไฟล์ CSV
filename = f'dataset/{f.read()}'

#ประกาศตัวแปร
type = ['เกาะ', 'แก่ง', 'ภูเขา', 'ถ้ำ', 'น้ำตก', 'โป่งพุร้อน', 'แหล่งน้ำ',
        'ชายหาด', 'ซากดึกดำบรรพ์', 'ธรณีสัณฐานและภูมิลักษณวรรณา']  # ประเภทของธรรมชาติ
sector_name = ['เหนือ', 'ตะวันออกเฉียงเหนือ', 'กลาง', 'ตะวันตก', 'ใต้', 'ตะวันออก'] #ภาค

#จำนวนแหล่งธรรมชาติ แยกตามภาคและประเภท เป็น dict
nature = {} 
for i in sector_name: nature[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
with open(filename, encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name = row[8]
        if row[8] not in sector_name:
            name = 'ตะวันออกเฉียงเหนือ'
        nature[name][int(row[2])-1] += 1
#จำนวนแหล่งธรรมชาติ แยกตามภาคและประเภท เป็น dict

plt.rcParams['font.family'] = 'tahoma'

root = tk.Tk()
text_font = ('tahoma', 12)
root.option_add('*TCombobox*Listbox.font', text_font) 
root.config(bg='white')
root.title('แหล่งธรรมชาติอันควรอนุรักษ์ของไทย')
photo = PhotoImage(file = 'img/11.png')
root.iconphoto(False, photo)
#ตัวแปรสำหรับกำหนดขนาดหน้าต่าง
screen_width = root.winfo_screenwidth() #ความกว้างจอ
screen_height = root.winfo_screenheight() #ความสูงจอ
w = 1366 #ความกว้างหน้าต่างโปรแกรม
h =  768 #ความสูงหน้าต่างโปรแกรม
x_cordinate = int((screen_width/2) - (w/2)) #ตำแหน่งจอแนวนอน
y_cordinate = int((screen_height/2) - (h/2)) #ตำแหน่งจอแนวตั้ง
#กำหนดขนาดหน้าต่างโปรแกรม และ ตำแหน่งหน้าต่างโปรแกรม
root.geometry("{}x{}+{}+{}".format(w, h, x_cordinate, y_cordinate))

#แสดงข้อมูลธรรมชาติรวมเมื่อกดปุ่ม
def show_nature(bt_name):
    count = 0
    with open(filename, encoding='utf8') as f:
        reader = csv.reader(f)
        #next(reader)
        for row in reader:
            data_val.set(type[int(bt_name)-1])
            if row[2] == bt_name:
                count += 1
    bt_data_val.set(f'มี {count} แห่ง')


#เปลี่ยนข้อมูลเมื่อเลือกภาค แสดงกราฟใหม่
def change_sector(e):
    global pie1
    global nature
    global sector_data_value
    global pie_chart_figure
    explode = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
    
    sector_data_value = nature.get(Combo.get())
    nature_data = []
    for i in range(len(sector_data_value)):
        nature_data.append(f'{type[i]} {sector_data_value[i]} แห่ง')
    pie1.clear()
    pie1.add_subplot(211).pie(sector_data_value, autopct=lambda p: '{:.1f}%'.format(
        round(p)) if p > 0 else '', pctdistance=1.2, startangle=90, explode=explode)
    pie1.legend(nature_data, loc='upper right', bbox_to_anchor=(1.0, 1.006))
    pie_chart_figure = FigureCanvasTkAgg(pie1, root)
    pie_chart_figure.get_tk_widget().grid(row=1, column=2, rowspan=12)
    pie1.canvas.draw()


#ชุดข้อมูล ของ bar chart
sector_data_value = []
all_sector_data = [0,0,0,0,0,0,0,0,0,0]
with open(filename, encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        all_sector_data[int(row[2])-1] += 1

#dropdown menu เลือกภาค
Combo = ttk.Combobox(root, values=sector_name, font=('tahoma  16 '))
Combo.current(0)
Combo.bind("<<ComboboxSelected>>", change_sector)
Combo.grid(row=0, column=2,sticky=NSEW)

#bar chart
bar_color=['steelblue','darkorange','forestgreen','crimson','mediumpurple','rosybrown','pink','grey','olive','cyan']

fig = plt.Figure(figsize=(6, 15), dpi=70)
fig.suptitle('จำนวนแหล่งธรรมชาติในประเทศไทย', fontsize=20)
bar1 = fig.add_subplot(211)
bar1.bar(type, all_sector_data,color=bar_color,edgecolor='black')
bar1.tick_params(axis='both', which='major')
bar1.set_xticklabels(type, rotation=45, ha="right")
bar_chart_figure = FigureCanvasTkAgg(fig, root)
bar_chart_figure.get_tk_widget().grid(row=0, column=0, rowspan=13)

#pie chart
pie1 = plt.Figure(figsize=(6, 15), dpi=70)
change_sector(Combo.get())

#frame ข้อมูล
f1 = Frame(root, width=350, bg="white", highlightbackground="black", highlightthickness=0).grid(row=0, rowspan=30, column=3, sticky=NSEW)
lbl1 = Label(f1, text="แหล่งธรรมชาติทั้งหมด", font=('tahoma  12'),
            anchor="center", bg='white', width=30, height=2).place(x=1000, y=2)

#ไอคอนของปุ่ม
btimg01 = PIL.Image.open('img/01.png')
btimg01 = btimg01.resize((50, 50), PIL.Image.ANTIALIAS)
btimg01 = PIL.ImageTk.PhotoImage(btimg01)

btimg02 = PIL.Image.open('img/02.png')
btimg02 = btimg02.resize((50, 50), PIL.Image.ANTIALIAS)
btimg02 = PIL.ImageTk.PhotoImage(btimg02)

btimg03 = PIL.Image.open('img/03.png')
btimg03 = btimg03.resize((50, 50), PIL.Image.ANTIALIAS)
btimg03 = PIL.ImageTk.PhotoImage(btimg03)

btimg04 = PIL.Image.open('img/04.png')
btimg04 = btimg04.resize((50, 50), PIL.Image.ANTIALIAS)
btimg04 = PIL.ImageTk.PhotoImage(btimg04)

btimg05 = PIL.Image.open('img/05.png')
btimg05 = btimg05.resize((50, 50), PIL.Image.ANTIALIAS)
btimg05 = PIL.ImageTk.PhotoImage(btimg05)

btimg06 = PIL.Image.open('img/06.png')
btimg06 = btimg06.resize((50, 50), PIL.Image.ANTIALIAS)
btimg06 = PIL.ImageTk.PhotoImage(btimg06)

btimg07 = PIL.Image.open('img/07.png')
btimg07 = btimg07.resize((50, 50), PIL.Image.ANTIALIAS)
btimg07 = PIL.ImageTk.PhotoImage(btimg07)

btimg08 = PIL.Image.open('img/08.png')
btimg08 = btimg08.resize((50, 50), PIL.Image.ANTIALIAS)
btimg08 = PIL.ImageTk.PhotoImage(btimg08)

btimg09 = PIL.Image.open('img/09.png')
btimg09 = btimg09.resize((50, 50), PIL.Image.ANTIALIAS)
btimg09 = PIL.ImageTk.PhotoImage(btimg09)

btimg10 = PIL.Image.open('img/10.png')
btimg10 = btimg10.resize((50, 50), PIL.Image.ANTIALIAS)
btimg10 = PIL.ImageTk.PhotoImage(btimg10)

btimg = [btimg01, btimg02, btimg03, btimg04, btimg05, btimg06, btimg07, btimg08, btimg09, btimg10]
#ไอคอนของปุ่ม

#ปุ่ม 8 ปุ่ม ['เกาะ', 'แก่ง', 'ภูเขา', 'ถ้ำ','น้ำตก', 'โป่งพุร้อน', 'แหล่งน้ำ', 'ชายหาด', 'ซากดึกดำบรรพ์', 'ธรณีสัณฐานและภูมิลักษณวรรณา']
for i in range(1, 11):
    bt = Button(f1, text=f" {type[i-1]}", font=('tahoma  12 '), image=btimg[i-1], compound=LEFT, width=257, height=0.25, bg="white", highlightbackground="black"
    , highlightthickness=0, name=str(i), command=lambda i=i: show_nature(str(i))).place(x=1000, y=61*i)
#ปุ่ม

# label แสดงค่าเมื่อกดปุ่ม
bt_data_val = StringVar()
data_val=StringVar()
bt_data_val.set("กดปุ่มเพื่อเลือก")
lbl3= Label(f1, textvariable=data_val, font=('tahoma  18 '), anchor='center', bg="white", width=25).place(x=1015, y=690)
lbl2 = Label(f1, textvariable=bt_data_val, font=('tahoma  18 bold '), anchor='center', bg="white", width=12).place(x=1090, y=720)



root.mainloop()
