import random

#hangman.py
def hangman_game(word):
    word = word.lower()
    word_letters = set(word)
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    used_letters = set()
    lives = 6

    while len(word_letters) > 0 and lives > 0:
        print("You have {} lives left".format(lives))
        print("Used letters:", ' '.join(used_letters))
        print("Word: ", end="")
        for letter in word:
            if letter in used_letters:
                print(letter, end=" ")
            else:
                print("_", end=" ")
        print("\n")

        user_letter = input("Enter a letter: ").lower()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives -= 1
        elif user_letter in used_letters:
            print("You have already used this letter")
        else:
            print("Invalid input")

    if lives == 0:
        print("You lost! The word was {}".format(word))
    else:
        print("Congratulations! You guessed the word {}".format(word))

def hangman():
    words = [
        'hangman', 'chairs', 'backpack', 'desk', 'python', 'laptop',
        'computer', 'programming', 'keyboard', 'television', 'guitar',
        'headphones', 'pencil', 'eraser', 'calculator', 'cactus',
        'flower', 'mug', 'table', 'curtain', 'refrigerator', 'stove',
        'microwave', 'bread', 'butter', 'chocolate', 'sandwich',
        'tomato', 'potato', 'carrot', 'pepper', 'lettuce', 'pumpkin',
        'elephant', 'giraffe', 'kangaroo', 'zebra', 'lion', 'tiger',
        'penguin', 'dolphin', 'whale', 'shark', 'octopus', 'jellyfish',
        'bicycle', 'motorcycle', 'airplane', 'helicopter', 'train',
        'subway', 'ship', 'sailboat', 'skateboard', 'rollerblade'
    ]
    hangman_game(random.choice(words))
