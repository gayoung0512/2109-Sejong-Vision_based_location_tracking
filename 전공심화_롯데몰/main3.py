from PIL import Image
import pytesseract
import cv2
import numpy as np

image = cv2.imread('map_2F.jpg')
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
#image = Image.open('map_2F.jpg')
#text = pytesseract.image_to_string(image,config=tessdata_dir_config)
img = cv2.imread('map_2F.jpg')
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

height, width, channel = img.shape

#이미지 전처리
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #grayscale
cv2.imwrite('gray.jpg', gray)
cv2.imshow("gray", gray)
cv2.waitKey(0)

blur = cv2.GaussianBlur(gray, (3, 3), 0) #가우시안 블러 (원본 이미지, 필터 크기, 표준 편차)
cv2.imwrite('blur.jpg', blur)
cv2.imshow("blur", blur)
cv2.waitKey(0)

canny = cv2.Canny(blur, 100, 200)#canny 함수
cv2.imwrite('canny.jpg', canny)
cv2.imshow("canny", canny)
cv2.waitKey(0)


# Load image, grayscale, Otsu's threshold
#thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#clean = thresh.copy()

# Remove horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,1))
detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(clean, [c], -1, 0, 3)

# Remove vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,30))
detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(clean, [c], -1, 0, 3)

cnts = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    # Remove diagonal lines
    area = cv2.contourArea(c)
    if area < 100:
        cv2.drawContours(clean, [c], -1, 0, 3)
    # Remove circle objects
    elif area > 1000:
        cv2.drawContours(clean, [c], -1, 0, -1)
    # Remove curve stuff
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    x,y,w,h = cv2.boundingRect(c)
    if len(approx) == 4:
        cv2.rectangle(clean, (x, y), (x + w, y + h), 0, -1)

open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
opening = cv2.morphologyEx(clean, cv2.MORPH_OPEN, open_kernel, iterations=2)
close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,2))
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=4)
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    if area > 500:
        ROI = image[y:y+h, x:x+w]
        ROI = cv2.GaussianBlur(ROI, (3,3), 0)
        data = pytesseract.image_to_string(ROI, lang='eng',config=tessdata_dir_config)
        if data.isalnum():
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
            print(data)

cv2.imshow('image.png', image)
cv2.imshow('clean.png', clean)
cv2.imshow('close.png', close)
cv2.imshow('opening.png', opening)
cv2.waitKey()

#print (text)
#print(text.index('Cueren'))