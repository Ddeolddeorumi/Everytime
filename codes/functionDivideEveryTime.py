import numpy
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
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
            #subImg = cv2.cvtColor(subImg, cv2.COLOR_BGR2GRAY)
        
            nrow = round((subImg.shape[0]-1)/4)
            divide4 = [0,nrow,2*nrow,3*nrow,subImg.shape[0]]
        
        
            for k in range(len(divide4)-1):
                subsubImg = subImg[divide4[k]:divide4[k+1],]
                meanColor = subsubImg.mean()
                if meanColor >= 250:
                    dayNullTime.append(0)
                else:
                    dayNullTime.append(1)

            #cv2.imwrite('dvdImg\\{0}\\{1}.png'.format(i,time[j]), subImg) #저장, 확인용이라 필요 없음

        while len(dayNullTime)<64:
            dayNullTime.append(0)

        weekNullTime.append(dayNullTime)

    result = numpy.array(weekNullTime).transpose()
    result = numpy.delete(result, [0,1,2,3], 0)
    
    return(result)

#img1 = cv2.imread('everytime1.jpg')
#img2 = cv2.imread('everytime2.jpg')

#im1 = divideEverytime(img1)
#im2 = divideEverytime(img2)


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


def tellMeNullWeek(im):
    
    speaker = []
    date = ['월요일', '화요일', '수요일', '목요일', '금요일']

    for i in range(5):
        imDate = im[:,i]
        tellMe = tellMeNull(imDate)
        for j in range(len(tellMe)):
            thisIsNull = tellMe[j]
            speaker.append( '{0} 당신의 {1}번 째 공강시간은: {2} ~ {3}'.format(date[i],thisIsNull[0],
                                                                       thisIsNull[1],thisIsNull[2]))
    return(speaker)


#tellMeNullWeek(im1)
img1 = cv2.imread('everytime1.jpg')
img2 = cv2.imread('everytime2.jpg')
img3 = cv2.imread('everytime3.jpg')
imgList =[img1, img2, img3]

#im1 = divideEverytime(img1)

def tellOurNull(imgList):

    imgListCvt = []

    for i in range(len(imgList)):
        imgListCvt.append( divideEverytime(imgList[i]) )

    lastImg = sum(imgListCvt)
    speaker = tellMeNullWeek(lastImg)

    return(speaker)

for i in tellOurNull(imgList):
    print(i)

#im1 = divideEverytime(img1)
#im2 = divideEverytime(img2)
    

#print("당신의 {0}번 째 공강시간은: {1} ~ {2}".format(i+1, sT[i], eT[i]))
