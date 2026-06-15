score = float(input("Enter the score: "))
if score > 100:
    print("The score should be between 0 and 100")
elif score >= 90 and score <= 100:
    print("A")
elif score >= 70 and score <= 89:
    print("B")
elif score >= 60 and score <= 69:
    print("C")
elif score >= 50 and score <= 59:
    print("D")
elif score >= 40 and score <= 49:
    print("E")
else:
    print("F")
