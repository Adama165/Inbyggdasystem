import socket
import os
import glob
import time


HOST = "raspberrypi5server.local"
PORT = 65432

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equal_pos = lines[1].find('t=')
	if equal_pos != -1:
		temp_string = lines[1][equal_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c
counter=0
celsius=str(read_temp())
print(celsius)
while counter!=10:
    if read_temp() > 22:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(bytes(celsius, 'utf-8'))
            data = s.recv(1024)
        print(f"Received {data!r}")
    counter+=1
    print(counter)
