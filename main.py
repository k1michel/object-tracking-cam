import cv2
import numpy as np
import sys
import time
#from threading import Thread
import serial

cap = cv2.VideoCapture(0)
ser = serial.Serial("/dev/serial0", baudrate=9600)

#Iniciamos giro camara en 90grados
position_inicial = str(90)
print(position_inicial)
giro_envio = position_inicial.encode()
ser.write(giro_envio)
ser.flush()
time.sleep(2)

# COnfiguracion Imagen camara
codec = 0x47504A4D  # MJPG
cap.set(cv2.CAP_PROP_FPS, 60.0)
cap.set(cv2.CAP_PROP_FOURCC, codec)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2144)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_AUTOFOCUS,0)


# Dividimos en columnas y filas la imagen
_, frame = cap.read()
rows, cols, _ = frame.shape
#Calculamos el medio actual y el medio de la imagen mediante las columnas
x_medium = int(cols / 2)
center = int(cols / 2)
position = 90 # grados

'''
def enviar_arduino(map_position):   
    try:
        position_toStr = str(round(map_position))
        print(position_toStr)
        giro_envio = position_toStr.encode()
        ser.write(giro_envio)
        ser.flush()
        time.sleep(1)
    except (serial.serialutil.SerialException):
        print('serial opened is error...')

    except (serial.serialutil.PortNotOpenError):
        print('serial closed is error...')
    except KeyboardInterrupt:
        print("\nInterrupcion por teclado")
        ser.close()
        cap.release()
        cv2.destroyAllWindows()
'''


while True:
    _, frame = cap.read()
    bgr_frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imwrite('/home/pi/object-tracking-cam/frame_1.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY,100])
    #cv2.imwrite('/home/pi/object-tracking-cam/bgr_frame_1.jpg', bgr_frame,[cv2.IMWRITE_JPEG_QUALITY,100])
    #cv2.imwrite('/home/pi/object-tracking-cam/hsv_frame_1.jpg', hsv_frame,[cv2.IMWRITE_JPEG_QUALITY,100])
        
    amarilloBajo = np.array([20, 100, 20], np.uint8)
    amarilloAlto = np.array([32, 255, 255], np.uint8)
    maskamarillo = cv2.inRange(hsv_frame, amarilloBajo, amarilloAlto)
    maskamarillovisual = cv2.bitwise_and(frame, frame, mask= maskamarillo)
    #cv2.imwrite('/home/pi/object-tracking-cam/maskamarillo_1.jpg', maskamarillo,[cv2.IMWRITE_JPEG_QUALITY,100])
    cv2.imwrite('/home/pi/object-tracking-cam/maskamarillovisual_1.jpg', maskamarillovisual,[cv2.IMWRITE_JPEG_QUALITY,100])
    contours ,_ = cv2.findContours(maskamarillo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
            
        x_medium = int((x + x + w) / 2)
        break
        
    #cv2.line(frame, (x_medium, 0), (x_medium, 2144), (0, 255, 0), 2)
    '''
    cv2.imshow("Frame", frame)
    cv2.imshow("HSV Frame", hsv_frame)
    cv2.imshow("MaskRED", maskRed)
    cv2.imshow('maskRedvis', maskRedvis)
    '''
        
    # Move servo motor

    
    #if (position < 265) and (position >5):
    if x_medium < center -30:
        position += 3
    elif x_medium > center + 30:    
        position -= 3
    #map_position = (posicion_giro - 0) * (180 - 0) // (270 - 0) + 0    
    #enviar = enviar_arduino(map_position)

    try:
        position_toStr = str(round(position))
        print(position_toStr)
        giro_envio = position_toStr.encode()
        ser.write(giro_envio)
        ser.flush()
        time.sleep(0.1)
    except (serial.serialutil.SerialException):
        print('serial opened is error...')

    except (serial.serialutil.PortNotOpenError):
        print('serial closed is error...')
    except KeyboardInterrupt:
        print("\nInterrupcion por teclado")
        ser.close()
        cap.release()
        cv2.destroyAllWindows()
    time.sleep(1)
    
'''
if __name__ == "__main__":  
    chequeo = Thread(target=enviar_arduino, daemon=True)
    chequeo.start()
'''




