
import numpy
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
import PIL

img = cv2.imread('everytime1.jpg')
'''
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = numpy.ones((1,1), numpy.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY,11,2)

cv2.imwrite('everytime1thres.png', img)

img = cv2.imread('everytime1thres.png')
'''
result = pytesseract.image_to_string(img, lang='kor')

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.imshow('image',img)

l = result.split(sep='\n')


for i in range(len(l)):
    print('--------------------------------------------')
    print(l[i])

#font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.putText(img, 'OpenCV', (10,500), font, 4, (0, 0, 0), 2)
