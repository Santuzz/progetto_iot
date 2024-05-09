import serial
import time

ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

while True:
    plus_time = 7
    ser.write(b'\xFF')
    ser.write(int.to_bytes(plus_time, length=1, byteorder='little'))
    ser.write(b'\xFE')
    while ser.in_waiting:
        print(ser.readline())
    