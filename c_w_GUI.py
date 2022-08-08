import re
from tkinter import *
from tkinter import filedialog, dialog
import os



def clicked():
    text = idiomType(txt.get())
    lbl.configure(text=text)

def allInChinese(str):
    for i in str:
        if not re.compile(u'[\u4e00-\u9fa5]').search(i):
            return False
    return True

def idiomType(str):
        return '未知类型'

countArr = [0,0,0,0,0,0,0,0,0]

def open_file():
    global file_path
    global file_text
    global countArr
    arr = []
    text1.delete(1.0,END)
    file_path = filedialog.askopenfilenames(title=u'选择文件', filetypes=[('文本文件', '*.jpg')], initialdir=(os.path.expanduser('~user/Desktop/')))
    if file_path is not None:
        f = open(file=file_path, mode='r+', encoding='utf-8')
        for line in f:
            line = line.strip('\n')
            arr.append(line)

        text1.insert('insert', '123')
            
    countArr = [0,0,0,0,0,0,0,0,0]

if __name__ == '__main__':
    window = Tk()
    window.title("相机水印")
    window.geometry("600x400")
    lbl = Label(window, text="输入成语", font=("微软雅黑 Bold", 30))
    lbl.pack()
    txt = Entry(window, width=30)
    txt.pack(pady=10)


    btn = Button(window, text="单个成语判断", width=15, height=1, command=clicked)
    btn.pack()

    btOpen = Button(window, text='文本批量判断', width=15, height=1, command=open_file)
    btOpen.pack()

    text1 = Text(window, width=80, height=12, bg='white', font=('微软雅黑', 11))
    text1.pack()

    window.mainloop()
