import cv2
import time
import os

import HandTrackingModule as htm

wCam, hCam = 640, 480
img_counter = 0 #сколько фоток сделано

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "C:/Users/Fish\Downloads/drag_and_drop-main/finger_counter-main/fingers" # name of the folder, where there are images of fingers
fingerList = os.listdir(folderPath) # открываем путь к findr 
print(fingerList)
overlayList = []
for imgPath in fingerList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)

pTime = 0
timeFoto = 5

detector = htm.handDetector(detectionCon=0.75)
totalFingers = 0

while True:
    sucess, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if lmList:
        fingersUp = detector.fingersUp()# кроличество поднятых пальцев 
        print(fingersUp)
        #отсчет идет с большого пальца
        if (fingersUp[0] == 0 and fingersUp[1] == 0 and fingersUp[2] == 0 and fingersUp[3] == 0 and fingersUp[4] == 0):
            cv2.putText(img, f'Время до фото: {timeFoto}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            print("Делаю фото")
            while timeFoto < 0:
                
                timeFoto=timeFoto - 1
            #if (time.time()-delta > 5):
                
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, img)
            print("{} written!".format(img_name))
            img_counter += 1
        totalFingers = fingersUp.count(1)

    h, w, c = overlayList[totalFingers].shape
    img[0:h, 0:w] = overlayList[totalFingers]

    cTime = time.time()
    fps = 1/ (cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    
        
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)