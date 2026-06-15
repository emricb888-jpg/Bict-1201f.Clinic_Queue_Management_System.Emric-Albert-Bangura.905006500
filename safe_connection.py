# ask the user to input
signal = float(input("Enter signal strenght: "))
password = input("Enter protocol password: ")
if signal > 50 and password == "admin":
# what happen if connection is true?
    print("Connection Successful")
else:
    # what happen if condition is false?
    print("connection failed")
