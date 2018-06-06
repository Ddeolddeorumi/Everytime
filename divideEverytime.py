import numpy
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
import PIL

img = cv2.imread('everytime1.jpg')


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


##cv2.imshow('image',subimg1x)

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

        

        cv2.imwrite('dvdImg\\{0}\\{1}.png'.format(i,time[j]), subImg) #저장
        
    weekNullTime.append(dayNullTime)

result = numpy.array(weekNullTime).transpose()



    
    


'''
dvdline = [0]*100

dvdline[24] = 1
dvdline[49] = 1
dvdline[74] = 1
dvdline[99] = 1

n = 0
a = []
for i in range(len(dvdline)):
    if dvdline[i] == 1:
        a.append(n)
    n += 1

        
n= -1 

a.append( dvdline[(n+1):].index(1) )

n = sum(a)

a.append( dvdline[(n+1):].index(1) )

n = sum(a)

a.append( dvdline[(n+1):].index(1) )

n = sum(a)
'''
