from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import os


def pathFind() :
    imagePath = filedialog.askopenfilenames(parent=root,title='Choose a file')
    ggList.set(imagePath)
    print(imagePath)
    imageList = []
    for p in imagePath :
        imageList.append(cv2.imread(p))
    print(imageList)
    #ggList.set(imageList)
    
    


root = Tk()
root.title('GongGang Helper')

rootTitle = Label(root, text = '공강 계산기')
rootTitle.config(font=('굴림',30,'bold'))
rootTitle.grid(padx = 10, pady = 30, row = 0, column = 0,
               columnspan = 3)

explanation = Label(root, text='시간표 이미지를 선택해 주세요.')
explanation.grid(padx=5, pady=10, row = 1, column = 0, sticky = 'e')

browseBtn = Button(root, text = 'Browse', command=pathFind)
browseBtn.grid(padx=5, pady=10, row = 1, column = 1,
               columnspan = 1, sticky = 'w')




ggList = StringVar()
ggListBox = Listbox(root, width=60, height=20, listvariable=ggList)
ggListBox.grid(padx=20, pady=15, row = 2, column = 0,
               rowspan = 4, columnspan = 2)

root.mainloop()

