from tkinter import *
from tkinter import filedialog
import os
import numpy
import cv2
import PIL

def divideEverytime(img):

    #열 자르기 index 생성

    dvdline = list(map(int,list(img[0,:,0]<=245)))

    nx = 0
    ax = [0]
    for i in range(len(dvdline)):
        if dvdline[i] == 1:
            ax.append(nx)
        nx += 1
    ax.append(img.shape[1])

    # 행 연속된 거 지우기
    dlt = 0
    for i in range((len(ax)-1)):
        if ax[i] > (ax[i+1]-5):
            ax[i] = 0
        
    ax.sort()
    while ax[1]==0:
        ax.pop(0)

    #행 자르기 index 생성

    dvdline = list(map(int,list(img[:,0,0]<=245)))

    ny = 0
    ay = [0]
    for i in range(len(dvdline)):
        if dvdline[i] == 1:
            ay.append(ny)
        ny += 1
    ay.append(img.shape[0])
    
    # 열 연속된 거 지우기
    dlt = 0
    for i in range((len(ay)-1)):
        if ay[i] > (ay[i+1]-5):
            ay[i] = 0
        
    ay.sort()
    while ay[1]==0:
        ay.pop(0)

    # 자르기
    weekNullTime = [] #공강 5열 행렬

    subImgList = []

    for i in range(len(ax)-1):
        subImg = img[:,ax[i]:ax[i+1]]
        subImgList.append(subImg)
        
    time = list(range(8,24))

    for i in range(1,6):
        img = subImgList[i]

        dayNullTime = [] #공강 1열 행렬  
    
        for j in range(len(ay)-1):
            subImg = img[ay[j]:ay[j+1],:]
        
            nrow = round((subImg.shape[0]-1)/4)
            divide4 = [0,nrow,2*nrow,3*nrow,subImg.shape[0]]
        
        
            for k in range(len(divide4)-1):
                subsubImg = subImg[divide4[k]:divide4[k+1],]
                meanColor = subsubImg.mean()
                if meanColor >= 250:
                    dayNullTime.append(0)
                else:
                    dayNullTime.append(1)

        while len(dayNullTime)<64:
            dayNullTime.append(0)

        weekNullTime.append(dayNullTime)

    result = numpy.array(weekNullTime).transpose()
    result = numpy.delete(result, [0,1,2,3], 0)
    
    return(result)


def tellMeNull(im): #im is the matrix that shows dayNullTime

    if im[0] == 0:
        strt = [0]
    else:
        strt = []
    end=[]
    
    for i in range(len(im)-1):
        if im[i]!=0 and im[i+1]==0:
            strt.append(i+1)
        
        if im[i]==0 and im[i+1]!=0:
            end.append(i+1)

    if im[-1]==0:
        end.append(len(im))

    hour = 9 
    minute = 0 #시작 시간 및 분: 9시 0분

    sT = []
    eT = [] #시간으로 변환

    for i in range(len(strt)):
        sh = None
        sm = None
        sh = hour + strt[i]*15//60
        sm = minute + strt[i]*15%60
        sT.append('{0}시 {1}분'.format(sh,sm))
    
    for i in range(len(end)):
        eh = None
        em = None
        eh = hour + end[i]*15//60
        em = minute + end[i]*15%60
        eT.append('{0}시 {1}분'.format(eh,em))

    result = []
    
    for i in range(len(sT)):
        result.append([ i+1, sT[i], eT[i] ])

    return(result)


def tellMeNullWeek(im,day=['all']):
    
    speaker = []
    date = {0:'월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일'}
    day2 = ['mon', 'tue', 'wed', 'thu', 'fri']
    day1 = []

    if day[0] == 'all':
        day1 = [0,1,2,3,4]
    else:
        for i in range(len(day)):
            if day[i] in day2:
                day1.append( day2.index(day[i].lower()) )
        day1.sort()


    for i in day1:
        imDate = im[:,i]
        tellMe = tellMeNull(imDate)
        for j in range(len(tellMe)):
            thisIsNull = tellMe[j]
            speaker.append( '{0} 당신의 {1}번 째 공강시간은: {2} ~ {3}'.format(date[i],thisIsNull[0],
                                                                       thisIsNull[1],thisIsNull[2]))
    return(speaker)


def tellOurNull(imgList,day=['all']):

    imgListCvt = []

    for i in range(len(imgList)):
        imgListCvt.append( divideEverytime(imgList[i]) )

    lastImg = sum(imgListCvt)
    speaker = tellMeNullWeek(lastImg,day)

    return(speaker)


imageList = []
dayList = ['mon','tue','wed','thu','fri']
def pathFind() :
    global imageList
    imagePath = filedialog.askopenfilenames(parent=root,title='Choose a file')
    for p in imagePath :
        imageList.append(cv2.imread(p))

    if len(dayList) == 0 :
        ggList.set(tuple())
    else :
        ggList.set(tellOurNull(imageList,day=dayList))

def refreshFunc() :
    if len(imageList) == 0 :
        return 0
    if len(dayList) == 0 :
        ggList.set(tuple())
    else :
        ggList.set(tellOurNull(imageList,day=dayList))
    
def monBut() :
    global dayList
    if monB['bg'] == 'sky blue' :
        monB['bg'] = 'red'
        dayList.remove('mon')
    else :
        monB['bg'] = 'sky blue'
        dayList.append('mon')
    
def tueBut() :
    global dayList
    if tueB['bg'] == 'sky blue' :
        tueB['bg'] = 'red'
        dayList.remove('tue')
    else :
        tueB['bg'] = 'sky blue'
        dayList.append('tue')

def wedBut() :
    global dayList
    if wedB['bg'] == 'sky blue' :
        wedB['bg'] = 'red'
        dayList.remove('wed')
    else :
        wedB['bg'] = 'sky blue'
        dayList.append('wed')

def thuBut() :
    global dayList
    if thuB['bg'] == 'sky blue' :
        thuB['bg'] = 'red'
        dayList.remove('thu')
    else :
        thuB['bg'] = 'sky blue'
        dayList.append('thu')

def friBut() :
    global dayList
    if friB['bg'] == 'sky blue' :
        friB['bg'] = 'red'
        dayList.remove('fri')
    else :
        friB['bg'] = 'sky blue'
        dayList.append('fri')
    


root = Tk()
root.title('GongGang Helper')

# Title
rootTitle = Label(root, text = '공강 계산기')
rootTitle.config(font=('굴림',30,'bold'))
rootTitle.grid(padx = 10, pady = 30, row = 0, column = 0,
               columnspan = 2)

# browse frame
browseFrame = Frame(root)
browseFrame.grid(row = 1, column = 0, columnspan = 2)

# Lable
explanation = Label(browseFrame, text='시간표 이미지를 선택해 주세요.')
explanation.grid(padx=5, pady=10, row = 1, column = 0, sticky = 'e')

# Button
browseBtn = Button(browseFrame, text = 'Browse', command=pathFind)
browseBtn.grid(padx=5, pady=10, row = 1, column = 1,
               columnspan = 1, sticky = 'w')

# Button Frame
weekday = Frame(root)
weekday.grid(padx = 5, pady = 3, row = 2, column = 0, columnspan = 2)
# Each button of the Frame
monB = Button(weekday, text = 'Mon', bg = 'sky blue', fg = 'white',
              command = monBut)
monB.grid(padx = 5, pady = 0, row = 0, column = 0)
tueB = Button(weekday, text = 'Tue', bg = 'sky blue', fg = 'white',
              command = tueBut)
tueB.grid(padx = 5, pady = 0, row = 0, column = 1)
wedB = Button(weekday, text = 'Wed', bg = 'sky blue', fg = 'white',
              command = wedBut)
wedB.grid(padx = 5, pady = 0, row = 0, column = 2)
thuB = Button(weekday, text = 'Thu', bg = 'sky blue', fg = 'white',
              command = thuBut)
thuB.grid(padx = 5, pady = 0, row = 0, column = 3)
friB = Button(weekday, text = 'Fri', bg = 'sky blue', fg = 'white',
              command = friBut)
friB.grid(padx = 5, pady = 0, row = 0, column = 4)
refreshB = Button(weekday, text = 'Refresh', bg = 'orange', fg = 'white',
                  command = refreshFunc)
refreshB.grid(padx = 5, pady = 0, row = 0, column = 5)


# List Frame
listframe = Frame(root)
listframe.grid(padx=20, pady=15, row = 3, column = 0,
               rowspan = 4, columnspan = 2)

# Listbox
ggList = StringVar()
ggListBox = Listbox(listframe, width=60, height=20, listvariable=ggList)
ggListBox.pack(side='left', fill = 'y')
# scroll bar
ggscrol = Scrollbar(listframe, orient = "vertical")
ggscrol.config(command=ggListBox.yview)
ggscrol.pack(side='right', fill = 'y')
# Developer
developer = Label(root,
                  text='Developed by HyunJae Lee, Wonsik Shin, SungKyunKwan Univ.')

developer.config(font=('굴림',10))
developer.grid(row = 7, padx = 5, pady = 2, column = 1)

root.mainloop()

