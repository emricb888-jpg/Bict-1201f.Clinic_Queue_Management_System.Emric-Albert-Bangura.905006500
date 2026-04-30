user_name = input("What is your name? ")
print("Hello " +user_name+ " Nice to meet you! ")
hobby = input("What is your hobby? ")
print(user_name+ " Love " +hobby+ "! ")
feel = input("How are you feeling today " +user_name+ "? ")
clean_feel = feel.lower()
if feel == "happy":
    print("That is great to here " +user_name)
else:
    print("I hope your day get even better "+user_name)

