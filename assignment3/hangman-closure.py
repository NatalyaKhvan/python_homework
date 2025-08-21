# Task 4: Closure Practice


def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)
        display = ""
        for char in secret_word:
            if char in guesses:
                display += char
            else:
                display += "_"
        print(display)
        return all(char in guesses for char in secret_word)

    return hangman_closure


secret = input("Enter the secret word: ").lower()

hangman = make_hangman(secret)

hangman_complete = False
while not hangman_complete:
    guess = input("Guess a letter: ").lower()
    if guess.isalpha() and len(guess) == 1:
        hangman_complete = hangman(guess)
    else:
        print("One letter only, please.")
