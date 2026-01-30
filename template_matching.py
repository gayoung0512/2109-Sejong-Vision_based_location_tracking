import numpy as np
import cv2
import sys
import os
# 영상 불러오기
max = 0

for i in os.listdir('./dataset/'):
    path = './dataset/' + i

    src = cv2.imread(path, cv2.IMREAD_COLOR)
    src1 = cv2.imread('./input/bigbear1.jpg',cv2.IMREAD_GRAYSCALE)
    src= cv2.resize(src,(800,800))
    src1 = cv2.resize(src1, (800, 800))
    if src1 is None or src is None:
        print('Image load failed!')
        sys.exit()

    # 특징점 알고리즘 객체 생성 (KAZE, AKAZE, ORB 등)
    # feature = cv2.KAZE_create()
    #feature = cv2.AKAZE_create()
    feature = cv2.ORB_create()

    # 특징점 검출 및 기술자 계산
    kp1, desc1 = feature.detectAndCompute(src1, None)
    kp2, desc2 = feature.detectAndCompute(src, None)

    # 특징점 매칭
    # matcher = cv2.BFMatcher_create()
    matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING)
    matches1 = matcher.knnMatch(desc1, desc2, 2) # knnMatch로 특징점 2개 검출

    # 좋은 매칭 결과 선별
    good_matches1 = []
    for m in matches1: # matches는 두개의 리스트로 구성
        if m[0].distance / m[1].distance < 0.7: # 임계점 0.7
            good_matches1.append(m[0]) # 저장

    print('# of good_matches:', len(good_matches1))
    if(len(good_matches1)>max):
        image=src
        max=len(good_matches1)
        max_good_matches = good_matches1
        kp3=kp2
        max_path=path
    # 특징점 매칭 결과 영상 생성
    dst1 = cv2.drawMatches(image, kp3, src1, kp1, max_good_matches, None)
    #print(i)

if 'AI' in max_path:
    map = cv2.imread('./map/map_AI.png')
    text = "대양 AI 센터"
    org = (50, 100)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(map, text, org, font, 1, (255, 0, 0), 2)
    cv2.imshow('map',map)
elif 'gwang' in max_path:
    map = cv2.imread('./map/map_gwang.png')
    cv2.imshow('map', map)
elif 'gun' in max_path:
    map = cv2.imread('./map/map_gun.png')
    cv2.imshow('map', map)
elif 'hak' in max_path:
    map = cv2.imread('./map/map_hak.png')
    cv2.imshow('map', map)
elif 'woo' in max_path:
    map = cv2.imread('./map/map_woo.png')
    cv2.imshow('map', map)
elif 'chu' in max_path:
    map = cv2.imread('./map/map_chu.png')
    cv2.imshow('map', map)

cv2.imshow('dst',dst1)
cv2.imshow('img_matched', image)
cv2.waitKey()
cv2.destroyAllWindows()