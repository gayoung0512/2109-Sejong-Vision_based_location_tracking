import numpy as np
import cv2
import sys
import os
import pytesseract
from PIL import Image
#필요한 라이브러리

# 영상 불러오기
max = 0
print('카테고리를 골라주세요.\n 1.food(음식점/카페 등)\n 2.fashion(옷/신발 등)\n 3.etc(액세서리/잡화 등)')
num=int(input())
src1 = cv2.imread('./input1/mac1.jpg', cv2.IMREAD_COLOR)
if num==1:
    for i in os.listdir('./dataset/food/'):
        path = './dataset/food/' + i
        src = cv2.imread(path, cv2.IMREAD_COLOR)
        try:
            src = cv2.resize(src, (800, 800))
            src1 = cv2.resize(src1, (800, 800))
        except:
            continue

        if src1 is None or src is None:
            print('Image load failed!')
            sys.exit()

        # 특징점 알고리즘 객체 생성 (KAZE, AKAZE, ORB 등)
        #feature = cv2.KAZE_create()
        #feature = cv2.AKAZE_create()
        #feature = cv2.ORB_create()
        sift = cv2.SIFT_create()

        # 특징점 검출 및 기술자 계산
        kp1, desc1 = sift.detectAndCompute(src1, None)
        kp2, desc2 = sift.detectAndCompute(src, None)

        # 특징점 매칭
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches1 = flann.knnMatch(desc1, desc2, k=2)

        #matcher = cv2.BFMatcher_create()
        #matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING)
        #matches1 = matcher.knnMatch(desc1, desc2, 2) # knnMatch로 특징점 2개 검출
        # 좋은 매칭 결과 선별
        good_matches1 = []
        # ratio=0.25
        for m in matches1:  # matches는 두개의 리스트로 구성
            if m[0].distance / m[1].distance < 0.7:  # 임계점 0.7
                good_matches1.append(m)  # 저장

        #print('# of good_matches:', len(good_matches1))
        if (len(good_matches1) > max):
            image = src
            max = len(good_matches1)
            max_good_matches = good_matches1
            kp_max = kp2
            max_path = path
    cv2.imshow('img', image)
    cv2.imshow('input', src1)
    cv2.waitKey()
    cv2.destroyAllWindows()
elif num==2:
    for i in os.listdir('./dataset/fashion/'):
        path = './dataset/fashion/' + i
        src = cv2.imread(path, cv2.IMREAD_COLOR)
        try:
            src = cv2.resize(src, (800, 800))
            src1 = cv2.resize(src1, (800, 800))
        except:
            continue

        if src1 is None or src is None:
            print('Image load failed!')
            sys.exit()

        # 특징점 알고리즘 객체 생성 (KAZE, AKAZE, ORB 등)
        # feature = cv2.KAZE_create()
        # feature = cv2.AKAZE_create()
        # feature = cv2.ORB_create()
        sift = cv2.SIFT_create()

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
        # ratio=0.25
        for m in matches1:  # matches는 두개의 리스트로 구성
            if m[0].distance / m[1].distance < 0.7:  # 임계점 0.7
                good_matches1.append(m)  # 저장

        # print('# of good_matches:', len(good_matches1))
        if (len(good_matches1) > max):
            image = src
            max = len(good_matches1)
            max_good_matches = good_matches1
            kp_max = kp2
            max_path = path
    cv2.imshow('img', image)
    cv2.imshow('input', src1)
    cv2.waitKey()
    cv2.destroyAllWindows()
elif num==3:
    for i in os.listdir('./dataset/etc/'):
        path = './dataset/etc/' + i
        src = cv2.imread(path, cv2.IMREAD_COLOR)
        try:
            src = cv2.resize(src, (800, 800))
            src1 = cv2.resize(src1, (800, 800))
        except:
            continue

        if src1 is None or src is None:
            print('Image load failed!')
            sys.exit()

        # 특징점 알고리즘 객체 생성 (KAZE, AKAZE, ORB 등)
        # feature = cv2.KAZE_create()
        # feature = cv2.AKAZE_create()
        # feature = cv2.ORB_create()
        sift = cv2.SIFT_create()

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
        # ratio=0.25
        for m in matches1:  # matches는 두개의 리스트로 구성
            if m[0].distance / m[1].distance < 0.7:  # 임계점 0.7
                good_matches1.append(m)  # 저장

        # print('# of good_matches:', len(good_matches1))
        if (len(good_matches1) > max):
            image = src
            max = len(good_matches1)
            max_good_matches = good_matches1
            kp_max = kp2
            max_path = path
    cv2.imshow('img', image)
    cv2.imshow('input', src1)
    cv2.waitKey()
    cv2.destroyAllWindows()


def image_name(img,flag):
    img_copy=img.copy()
    height, width, channel = img.shape

    # 이미지 전처리
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # grayscale
    blur = cv2.GaussianBlur(gray, (3, 3), 0)  # 가우시안 블러 (원본 이미지, 필터 크기, 표준 편차)
    canny = cv2.Canny(blur, 100, 200)  # canny 함수

    # 윤곽선 그리기
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # 상하구조 구성하지 않고 모든 contour 찾기
    contour_result = np.zeros((height, width, channel), dtype=np.uint8)
    # -1 주는 것: 전체 contour 다 찾기
    cv2.drawContours(contour_result, contours=contours, contourIdx=-1, color=(255, 255, 255))
    contour_result = np.zeros((height, width, channel), dtype=np.uint8)
    # 모든 값이 0인 배열 생성

    contours_dict = []
    # 윤곽선의 정보 저장

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)  # contour의 사각형 범위 구하기 ( x,y 좌표 높이 너비 저장)
        cv2.rectangle(contour_result, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)
        # 사각형 그려보기
        contours_dict.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),  # 사각형의 중심 좌표 저장
            'cy': y + (h / 2)  # 사각형의 중심 좌표 저장
        })

    MAX_WIDTH, MAX_HEIGHT = 40, 20  # 최대 너비와 높이
    # MIN_RATIO, MAX_RATIO = 0.45, 1.0# 가로대비 세로 비율의 최소 최대값

    MAX_AREA = 500  # 최대 넓이
    possible_contours = []  # 가능한 값을 다시 저장

    cnt = 0
    for x in contours_dict:  # for문 통해
        area = x['w'] * x['h']  # 넓이 계산
        ratio = x['w'] / x['h']  # 비율 계산

        # 조건들에 맞게 비교
        if area < MAX_AREA \
                and x['w'] < MAX_WIDTH and x['h'] < MAX_HEIGHT:
            # and MIN_RATIO < ratio < MAX_RATIO:
            x['idx'] = cnt
            cnt += 1
            possible_contours.append(x)  # 다시 저장 idx도 같이 저장

    contour_result2 = np.zeros((height, width, channel), dtype=np.uint8)

    for x in possible_contours:
        cv2.rectangle(contour_result2, pt1=(x['x'], x['y']), pt2=(x['x'] + x['w'], x['y'] + x['h']),
                      color=(255, 255, 255),
                      thickness=2)

    contours_map = []
    canny2 = cv2.Canny(contour_result2, 100, 200)
    contours, hierarchy = cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)
        contours_map.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),  # 사각형의 중심 좌표 저장
            'cy': y + (h / 2)  # 사각형의 중심 좌표 저장
        })
        if w < 30 and h < 30:
            continue
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

    for x in contours_map:
        # 이미지 크롭하기
        img_cropped = cv2.getRectSubPix(
            img,
            patchSize=(int(x['w'] + 1), int(x['h'] + 1)),
            center=(int(x['cx']), int(x['cy']))
        )
        text = pytesseract.image_to_string(img_cropped, lang='eng',
                                           config=r'-c preserve_interword_spaces=1 --psm 6 --oem 3 -l kor_lstm+eng+osd --tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"')
        text = text.strip()
        text = text.replace(" ", "")
        text = text.replace(".", "")
        text = text.replace("\n", "")
        text = text.replace(":", "")
        text = text.replace("|", "")
        if text in max_path:
            if len(text) >=3:
                cv2.rectangle(img_copy, (x['x'], x['y']), (x['x'] + x['w'], x['y'] + x['h']), (255, 0, 255), 2)
                print(text)
                flag=1
                break
    return img_copy,flag

flag=0
img = cv2.imread('map_1F.jpg')
image_final,flag=image_name(img,flag)
if(flag==0):
    img = cv2.imread('map_2F.jpg')
    image_final,flag=image_name(img,flag)
cv2.imshow('image_final',image_final)
cv2.waitKey()