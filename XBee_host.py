import serial
import time
import locale
import matplotlib.pyplot as plt
import numpy as np
import threading

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x140\r\n".encode())
char = s.read(3)
print("Set MY 0x140.")
print(char.decode())

s.write("ATDL 0x240\r\n".encode())
char = s.read(3)
print("Set DL 0x240.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write('ATWR\r\n'.encode())
char = s.read(3)
print('Write config.')
print(char.decode())

s.write('ATCN\r\n'.encode())
char = s.read(3)
print('Exit AT mode.')
print(char.decode())

print("start sending RPC")

x=[]
tilt=0
y=''

s.write("/getAcc/run\r".encode())
time.sleep(0.5)
s.write("/getAcc/run\r".encode())
time.sleep(0.5)
line1=s.read(1)

line2=0

def work(a1,a2):
    while 1:
        a1=[]
        a2=[]
        s.write("/getAcc/run\r".encode())
        time.sleep(1)

thread_get = threading.Thread(target = work, args=(line1,line2))
thread_get.start()

while tilt <= 19:
    s.write("/getAcc/run\r".encode())
    line1 = s.readline()
    line2 = s.readline()
    x.append(10*int(line1)+int(line2))
    print(x)
    tilt += 1
    time.sleep(1)

fig, ax = plt.subplots(1, 1)
l1,=ax.plot(i for i in range(20),x)
ax.set_xlabel('timestamp')
ax.set_ylabel('acc value')
plt.show()
s.close()