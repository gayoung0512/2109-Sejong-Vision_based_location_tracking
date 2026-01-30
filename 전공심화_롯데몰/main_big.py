#1. 데이터 읽어오기
import pandas as pd

#상위 다섯개 항목 가져오기
label = pd.read_csv('/content/gdrive/MyDrive/SAI_dog_breed/labels.csv')
sample_submission = pd.read_csv('/content/gdrive/MyDrive/SAI_dog_breed/sample_submission.csv')
label.head()

# (2) 종('breed')에 대한 정보 확인하기(어떤 종류가 있는지, 몇개 있는지)

# label['breed'].value_counts().index
print(len(label['breed'].unique()))
label['breed'].unique()
#(3) id 값에 해당하는 이미지 경로를 'imgpath' 필드에 저장하기

filePath = '/content/gdrive/MyDrive/SAI_dog_breed/train/'
f = lambda x: filePath + x + '.jpg'

label['imgpath'] = label['id'].apply(f)
label.head()
#(4)'imgpath'에 있는 이미지를 읽어서(load_img 활용) array로 변환(img_to_array 활용)하여 'imgArray' 필드에 저장하기
from keras.preprocessing.image import img_to_array,load_img,ImageDataGenerator
img = load_img('/content/gdrive/MyDrive/SAI_dog_breed/train/e7af8f590b4fbdca0779f5e606ef91a1.jpg', target_size = (100, 100))
img = img_to_array(img)
print(img.shape)
ff = lambda x: img_to_array(load_img(x , target_size = (10, 10)))
label['imgArray'] = label['imgpath'].apply(ff)
label['imgArray'][0].shape
#2. 데이터 전처리
#(1) X: 이미지 데이터(array) 정규화하여 할당

X_train= label['imgArray'].values / 255
#(2) Y :정답레이블(breed)을 원핫인코딩 변환
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
a = le.fit_transform(label['breed'])
print(a)
Y_train = np_utils.to_categorical(a)
Y_train[0]
#(3) train, test set 분리하기
from sklearn.model_selection import train_test_split

x_train, x_valid, y_train, y_valid = train_test_split(X_train, Y_train, test_size=0.2, random_state = 5)

#3. 모델 설계
# 컨볼루션 신경망의 설정
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), input_shape=(100, 100, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.25))#과적합을 막기위해 날려버림

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.25))#과적합을 막기위해 날려버림

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.25))#과적합을 막기위해 날려버림

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(120, activation='softmax'))

# 4. 모델 컴파일
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 5.학습
# 모델 최적화 설정
MODEL_DIR = './model/'
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

modelpath="./model/{epoch:02d}-{val_loss:.4f}.hdf5"
checkpointer = ModelCheckpoint(filepath=modelpath,
                               monitor='val_loss', verbose=1,
                               save_best_only=True)
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=10)


# 모델의 실행
history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test),
                    epochs=30, batch_size=200, verbose=0,
                    callbacks=[early_stopping_callback,checkpointer])

#6. 검증
# 테스트 정확도 출력
print("\n Test Accuracy: %.4f" % (model.evaluate(X_test, Y_test)[1]))

# 테스트 셋의 오차
y_vloss = history.history['val_loss']

# 학습셋의 오차
y_loss = history.history['loss']

# 그래프로 표현
x_len = numpy.arange(len(y_loss))
plt.plot(x_len, y_vloss, marker='.', c="red", label='Testset_loss')
plt.plot(x_len, y_loss, marker='.', c="blue", label='Trainset_loss')

# 그래프에 그리드를 주고 레이블을 표시
plt.legend(loc='upper right')
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()