import random

def guess_number():
    target_number = random.randint(1, 100)
    attempts = 0

    while attempts < 10:
        guess = int(input("Guess a number between 1 and 100: "))
        attempts += 1

        if guess < target_number:
            print("You guessed lower!")
        elif guess > target_number:
            print("You guessed higher!")
        else:
            print(f"Congratulations! You guessed the number in {attempts} attempts.")
            break
    print(f"Sorry, you've reached the maximum number of attempts. The number was {target_number}.")