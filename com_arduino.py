import sys
import time
import serial


ser = serial.Serial("/dev/serial0", baudrate=9600)

try:
    while True:
        giro_terminal = input('Indroducir angulo de giro:\n')
        giro_envio = giro_terminal.encode()
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