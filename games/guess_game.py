import random

def guess_number():
    target_number = random.randint(1, 100)
    guessed_correctly = False
    for attempts in range(10, 0, -1):
        print(f"{attempts} attempts left")
        while True:
            try:
                guess = int(input("Guess a number between 1 and 100: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        if guess == target_number:
            print(f"Congratulations! You guessed the number in {10 - attempts} attempts.")
            guessed_correctly = True
            break
        elif guess < target_number:
            print("You guessed lower!")
        else:
            print("You guessed higher!")
    
    if guessed_correctly == False:
        print(f"Sorry, you've reached the maximum number of attempts. The number was {target_number}.")