id = int(input("Enter the device ID to send data: "))
if id == 101:
    print("Sending data to printer...")
elif id == 102:
    print("Sending data to Laptop...")
elif id == 103:
    print("Sending data to Server...")
else:
    print("Error: Device Not Found")
