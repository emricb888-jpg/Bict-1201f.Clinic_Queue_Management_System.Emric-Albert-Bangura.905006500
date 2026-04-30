# Function 1: To display a welcome message (Requirement: Modularity)
def welcome_message():
    print("--- Freetown Clinic Queue Management System ---")
    print("SDG 3: Good Health and Well-being")


# Function 2: To format and print the patient record
def display_patient(count, name, reason):
    print(f"Queue No: {count} | Patient: {name} | Reason: {reason}")


# Main Program Logic
welcome_message()

patient_queue = []
running = True

# Requirement: Iteration (Loops)
while running:
    print("\nOptions: 1. Add Patient  2. View Queue  3. Exit")
    choice = input("Select an option: ")

    # Requirement: Decision Structures (if, elif, else)
    if choice == "1":
        # Requirement: Input & Data Types (Strings)
        name = input("Enter Patient Name: ")
        reason = input("Enter Reason for Visit: ")

        # Storing data in a list
        patient_queue.append({"name": name, "reason": reason})
        print("Patient added successfully!")

    elif choice == "2":
        print("\n--- Current Patient Queue ---")
        if not patient_queue:
            print("The queue is currently empty.")
        else:
            count = 1
            for patient in patient_queue:
                display_patient(count, patient['name'], patient['reason'])
                count += 1

    elif choice == "3":
        print("Closing system... Goodbye!")
        running = False  # Stops the loop

    else:
        print("Invalid choice. Please try again.")