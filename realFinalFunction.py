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

    for i in range(len(ax)-1):
        subImg = img[:,ax[i]:ax[i+1]]
        cv2.imwrite('dvdImg\subImg{0}.png'.format(i), subImg)

    time = list(range(8,24))

    for i in range(1,6):
        img = cv2.imread('dvdImg\subImg{0}.png'.format(i))

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

def pathFind() :
    imagePath = filedialog.askopenfilenames(parent=root,title='Choose a file')
    imageList = []
    for p in imagePath :
        imageList.append(cv2.imread(p))

    ggList.set(tellOurNull(imageList))
    
    
    


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

