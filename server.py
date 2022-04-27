import socket
import RPi.GPIO as GPIO
import time

def lights():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, True)
    time.sleep(1)
    GPIO.output(17, False)

HOST = "raspberrypi5server.local"
PORT = 65432
counter=0
while counter!=10:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = int(conn.recv(1024))
                if data > 22:
                    lights()
                    print(data)
                elif not data:
                    break
                conn.sendall(data)
    counter+=1
    print(counter)
