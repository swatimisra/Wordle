"""Wordle Game"""
# Name 1: Sanjitha Venkata
# EID 1: sv28325

# Name 2: Swati Misra
# EID 2: SM83264
import sys
import random
# ANSI escape codes for text color
# These must be used by wrapping it around a single character string
# for the test cases to work.
# For example, you if you have:
# string = "s"
# and you want to color it as correct, you would do
#
# colored_string = CORRECT_COLOR + string + RESET
#
# If you wanted to do it when a letter is in the wrong spot, you would do
#
# colored_string = WRONG_SPOT_COLOR + string + RESET
#
# If you wanted to do it when a letter is not in the word, you would do
#
# colored_string = NOT_IN_WORD_COLOR + string + RESET
#
# printing it out onto the terminal will now
# cause it to be color coded.

CORRECT_COLOR = "\033[1;92m"
WRONG_SPOT_COLOR = "\033[1;93m"
NOT_IN_WORD_COLOR = "\033[1;97m"
RESET_COLOR = "\033[0m"

# If you are colorblind for yellow and green, please use these colors instead.
# Uncomment the two lines below. Commenting in and out can be done by
# highlighting the  lines you care about and using:
# on a windows/linux laptop: ctrl + /
# on a mac laptop: cmd + /

# CORRECT_COLOR = "\033[1;91m"
# WRONG_SPOT_COLOR = "\033[1;94m"


# Labels to each attempt number. Offset by 1 using "" so that the attempt number
# correctly indexes into the list so that the operation doesn't need a -1 every time
ATTEMPT_NUMBER = ["", "6th", "5th", "4th", "3rd", "2nd", "1st"]

# The total number of letters allowed
NUM_LETTERS = 5

# Use this string when an error occurs
INVALID_INPUT = "Bad input detected. Please try again."


# DO NOT change this function
def print_explanation():
    """Prints the 'how to play' instructions on the official website"""
    print("Welcome to Command Line Wordle!")
    print()

    print(
        "".join([NOT_IN_WORD_COLOR + letter + RESET_COLOR for letter in "How To Play"])
    )
    print("Guess the secret word in 6 tries.")
    print("Each guess must be a valid 5-letter word.")
    print("The color of the letters will change to show")
    print("how close your guess was.")
    print()

    print("Examples:")
    print(CORRECT_COLOR + "w" + RESET_COLOR, end="")
    print("".join([NOT_IN_WORD_COLOR + letter + RESET_COLOR for letter in "eary"]))
    print(NOT_IN_WORD_COLOR + "w" + RESET_COLOR, end=" ")
    print("is in the word and in the correct spot.")

    print(NOT_IN_WORD_COLOR + "p" + RESET_COLOR, end="")
    print(WRONG_SPOT_COLOR + "i" + RESET_COLOR, end="")
    print("".join([NOT_IN_WORD_COLOR + letter + RESET_COLOR for letter in "lls"]))
    print(NOT_IN_WORD_COLOR + "i" + RESET_COLOR, end=" ")
    print("is in the word but in the wrong spot.")

    print("".join([NOT_IN_WORD_COLOR + letter + RESET_COLOR for letter in "vague"]))
    print(NOT_IN_WORD_COLOR + "u" + RESET_COLOR, end=" ")
    print("is not in the word in any spot.")
    print()


def prepare_game():
    """Sets game up"""
    # This is another way to use open by using the special keywords with __ as __:
    # These two lines of code below are equivalent to:
    # valid_nonsecret_words = open("valid_words.txt", "r", encoding="ascii")
    #   valid_words = {word.rstrip("\n") for word in valid_nonsecret_words.readlines()}
    # valid_nonsecret_words.close()
    # It also specifies "ascii" as its representation (encoding) since its required by pylint.

    with open("valid_guesses.txt", "r", encoding="ascii") as valid_nonsecret_words:
        # Sets also have set comprehension just like list comprehension
        valid_words = {word.rstrip("\n") for word in valid_nonsecret_words.readlines()}
    with open("secret_words.txt", "r", encoding="ascii") as valid_secret_words:
        # Sets also have set comprehension just like list comprehension
        secret_words = [word.rstrip("\n") for word in valid_secret_words.readlines()]
    
    secret_word=None
    if len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            seednum=int(sys.argv[1])
            random.seed(seednum)
            secret_word = random.choice(secret_words)
        elif(sys.argv[1].isalpha() and sys.argv[1].islower()) and len(sys.argv[1])==NUM_LETTERS:
            secret_word = sys.argv[1]
    elif len(sys.argv)==1:
        secret_word = random.choice(secret_words)
    else:
        secret_word=None
        return None

    return secret_word, valid_words

# TODO: Modify this function
def get_feedback(secret_word, guessed_word):
    """Colors according to correct/incorrect/within word"""
    feedback = [None] * len(secret_word)

    secret_word_dict={}
    #guessed_word_dict={}

    for letter in secret_word:
        secret_word_dict[letter] = secret_word_dict.get(letter,0)+1
    # for letter in guessed_word:
    #     guessed_word_dict[letter] = guessed_word_dict.get(letter,0)+1

    #old code
    # for i in range(NUM_LETTERS):
    
    #     if guessed_word[i] == secret_word[i]:
    #         feedback[i]= CORRECT_COLOR + guessed_word[i] + RESET_COLOR
    #     elif guessed_word[i] in secret_word and secret_word_dict[guessed_word[i]]>0 \
    #         and guessed_word_dict[guessed_word[i]]>0:
    #         feedback[i] = WRONG_SPOT_COLOR + guessed_word[i] + RESET_COLOR
    #         secret_word_dict[guessed_word[i]]-=1
    #         guessed_word_dict[guessed_word[i]]-=1
    #     else:
    #         feedback[i] = NOT_IN_WORD_COLOR + guessed_word[i] + RESET_COLOR


    # Changed code
    for i in range(NUM_LETTERS):
        if guessed_word[i] == secret_word[i]:
            feedback[i] = CORRECT_COLOR + guessed_word[i] + RESET_COLOR
            secret_word_dict[secret_word[i]]-=1
             
    for i in range(NUM_LETTERS):
        if guessed_word[i] in secret_word and secret_word_dict[guessed_word[i]] > 0:
            feedback[i] = WRONG_SPOT_COLOR + guessed_word[i] + RESET_COLOR
            secret_word_dict[guessed_word[i]]-=1

    for i in range(NUM_LETTERS):
        if guessed_word[i] not in secret_word:
            feedback[i] = NOT_IN_WORD_COLOR + guessed_word[i] + RESET_COLOR
        if feedback[i] is None:
            feedback[i] = NOT_IN_WORD_COLOR + guessed_word[i] + RESET_COLOR


    return "".join(feedback)

# TODO: Modify this function
def main():
    """Main method"""


    with open("valid_guesses.txt", "r", encoding="ascii") as valid_nonsecret_words:
        # Sets also have set comprehension just like list comprehension
        valid_words = {word.rstrip("\n") for word in valid_nonsecret_words.readlines()}


    valid = prepare_game() #contains secret word and full list of valid guesses

    secret_word, valid_guesses = valid

    if secret_word is None:
        print(INVALID_INPUT)
        return

    print_explanation()

    formatted_secret_word = "".join(
        [CORRECT_COLOR + c + RESET_COLOR for c in secret_word]
    )

    

    attempts = 6
    while attempts > 0:
        prompt = "Enter your " + ATTEMPT_NUMBER[attempts] + " guess: "
        guess = input(prompt)

        if not sys.stdin.isatty():
            print(guess)
        feedback = get_feedback(secret_word, guess)
        print(" " * (len(prompt) - 1), feedback)

        if feedback == formatted_secret_word:
            print("Congratulations! ", end="")
            print("You guessed the word '" + formatted_secret_word + "' correctly.")
            break

        if guess not in valid_words or guess.islower() is False or guess.isalpha() is False and len(guess)<NUM_LETTERS:
            attempts+=1
            print(INVALID_INPUT)
        attempts -= 1


    if attempts == 0 and feedback!=formatted_secret_word:
        print("Sorry, you've run out of attempts. The correct word was ", end="")
        print("'" + formatted_secret_word + "'.")


# DO NOT change these lines
if __name__ == "__main__":
    main()
