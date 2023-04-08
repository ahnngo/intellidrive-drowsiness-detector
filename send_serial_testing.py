import serial
arduino = serial.Serial('/dev/cu.usbserial-0001', baudrate=9600, timeout=1)

def write_read(x):
    b = bytes(x, 'utf-8')
    print(b)
    arduino.write(b)
    print("pass")
    # if it doesn't get anything back in 1 second, then the timeout returns arduino.read()
    data = arduino.read()
    return data

while True:    
    num = input("Enter a number: ") # Taking input from user
    if (num == 'quit'):
        arduino.close()
        break
    value = write_read(num)
    print(value) # printing the value