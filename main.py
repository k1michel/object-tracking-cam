import cv2
import numpy as np
import sys
import time
import serial

cap = cv2.VideoCapture(0)
ser = serial.Serial("/dev/serial0", baudrate=9600)

'''
cap.set(3, 480)
cap.set(4, 320)
'''

codec = 0x47504A4D  # MJPG
cap.set(cv2.CAP_PROP_FPS, 30.0)
cap.set(cv2.CAP_PROP_FOURCC, codec)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
cap.set(cv2.CAP_PROP_AUTOFOCUS,0)

_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
center = int(cols / 2)
position = 90 # degrees
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imwrite('/home/pi/object-tracking-cam/1.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY,100])
    # red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium = int((x + x + w) / 2)
        break
    
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    
    cv2.imshow("Frame", frame)
    
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
    # Move servo motor
    if x_medium < center -30:
        position += 1.5
    elif x_medium > center + 30:
        position -= 1.5
        
    try:
        while True:
            #giro_terminal = input('Indroducir angulo de giro:\n')
            giro_envio = position.encode()
            ser.write(giro_envio)
            ser.flush()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupcion por teclado")
    except ValueError as ve:
        print(ve)
        print("Otra interrupcion")
    finally:
        ser.close()

cap.release()
cv2.destroyAllWindows()
