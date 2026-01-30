import numpy as np
import cv2
import sys
import os
# 영상 불러오기
max = 0
for i in os.listdir('./dataset/'):
    path = './dataset/' + i

    src = cv2.imread(path, cv2.IMREAD_COLOR)
    src1 = cv2.imread('./input/dic1.jpg', cv2.IMREAD_COLOR)
    src=cv2.resize(src,(800,800))
    src1=cv2.resize(src1,(800,800))

    if src1 is None or src is None:
        print('Image load failed!')
        sys.exit()

    # 특징점 알고리즘 객체 생성 (KAZE, AKAZE, ORB 등)
    #feature = cv2.KAZE_create()
    #feature = cv2.AKAZE_create()
    #feature = cv2.ORB_create()
    sift=cv2.SIFT_create()

    # 특징점 검출 및 기술자 계산
    kp1, desc1 = sift.detectAndCompute(src1, None)
    kp2, desc2 = sift.detectAndCompute(src, None)

    # 특징점 매칭
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches1 = flann.knnMatch(desc1, desc2, k=2)

    # matcher = cv2.BFMatcher_create()
   # matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING)
   # matches1 = matcher.knnMatch(desc1, desc2, 2) # knnMatch로 특징점 2개 검출
    # 좋은 매칭 결과 선별
    good_matches1 = []
    #ratio=0.25
    for m in matches1: # matches는 두개의 리스트로 구성
        if m[0].distance / m[1].distance <0.7: # 임계점 0.7
            good_matches1.append(m) # 저장

    print('# of good_matches:', len(good_matches1))
    if(len(good_matches1)>max):
        image=src
        max=len(good_matches1)
        max_good_matches=good_matches1
        kp_max=kp2
        max_path=path
    # 특징점 매칭 결과 영상 생성
   # dst1 = cv2.drawMatches(image, kp_max, src1, kp1, max_good_matches, None)


# 특징점 매칭 결과 영상 생성
#dst1 = cv2.drawMatches(image, kp_max, src1, kp1, max_good_matches, None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


#cv2.imshow('dst', dst1)
#cv2.waitKey()
#cv2.destroyAllWindows()


cv2.imshow('img', image)
cv2.imshow('input', src1)
cv2.waitKey()
cv2.destroyAllWindows()


print(max_path)
if 'AI' in max_path:
    map = cv2.imread('./map/map_AI.png')
    cv2.imshow('map',map)
    cv2.waitKey()
    cv2.destroyAllWindows()
elif 'gwang' in max_path:
    map = cv2.imread('./map/map_gwang.png')
    cv2.imshow('map', map)
    cv2.waitKey()
    cv2.destroyAllWindows()
elif 'gun' in max_path:
    map = cv2.imread('./map/map_gun.png')
    cv2.imshow('map', map)
    cv2.waitKey()
    cv2.destroyAllWindows()
elif 'hak' in max_path:
    map = cv2.imread('./map/map_hak.png')
    cv2.imshow('map', map)
    cv2.waitKey()
    cv2.destroyAllWindows()
elif 'woo' in max_path:
    map = cv2.imread('./map/map_woo.png')
    cv2.imshow('map', map)
    cv2.waitKey()
    cv2.destroyAllWindows()
elif 'chu' in max_path:
    map = cv2.imread('./map/map_chu.png')
    cv2.imshow('map', map)
    cv2.waitKey()
    cv2.destroyAllWindows()