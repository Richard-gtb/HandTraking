from pyfirmata import Arduino, util
import cv2
import mediapipe as mp
import time

uno = Arduino('COM3')
video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils
posicao = 1

while True: 
    check, img = video.read()
    time.sleep(0.03)
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h, w,_ = img.shape
    pontos = []
    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img,points,hand.HAND_CONNECTIONS)
            for id,cord in enumerate(points.landmark):
                cx,cy = int(cord.x*w), int(cord.y*h)
                #cv2.putText(img,str(id),(cx,cy+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
                pontos.append((cx,cy))

        dedos = [8,12,16,20]
        contador = 0
        if points: 
            if pontos[4][0] > pontos[2][0]:
                contador += 1
            for x in dedos:
                if pontos[x][1] < pontos[x-2][1]:
                    contador += 1
        
        #Definindo parada do motor
        if contador == "":
            uno.digital[8].write(1)
            uno.digital[7].write(0)
        if contador == 0:
            uno.digital[8].write(1)
            uno.digital[7].write(0)

        
        #Definindo ida para a posição 1
        if contador == 1:
            if posicao == 1:
                posicao = 1
            if posicao == 2:
                uno.digital[8].write(0)
                uno.digital[7].write(0)
                time.sleep(0.04)
                uno.digital[8].write(1)
                uno.digital[7].write(0)
            if posicao == 3:
                uno.digital[8].write(0)
                uno.digital[7].write(0)
                time.sleep(0.08)
                uno.digital[8].write(1)
                uno.digital[7].write(0)
            posicao = 1 

        #Definindo ida para a posição 2  
        if contador == 2:
            if posicao == 2:
                posicao = 2
            if posicao == 1:
                uno.digital[8].write(1)
                uno.digital[7].write(1)
                time.sleep(0.04)
                uno.digital[8].write(1)
                uno.digital[7].write(0)
            if posicao == 3:
                uno.digital[8].write(0)
                uno.digital[7].write(0)
                time.sleep(0.04)
                uno.digital[8].write(1)
                uno.digital[7].write(0)
            posicao = 2

        #Definindo ida para a posição 3
        if contador == 3:
            if posicao == 3:
                posicao = 3
            if posicao == 2:
                uno.digital[8].write(1)
                uno.digital[7].write(1)
                time.sleep(0.04)
                uno.digital[8].write(1)
                uno.digital[7].write(0)
            if posicao == 1:
                uno.digital[8].write(1)
                uno.digital[7].write(1)
                time.sleep(0.08)
                uno.digital[8].write(1)
                uno.digital[7].write(0)
            posicao = 3

        print(contador)            
    cv2.imshow("Image",img)
    cv2.waitKey(1)  