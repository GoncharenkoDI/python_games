from keyboard import *

print("натисніть клавішу")
key = ''
while key != 'q':
    key = read_key()
    print(key)