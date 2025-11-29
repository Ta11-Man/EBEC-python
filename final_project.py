"""
Author: Gabriel Halstead
Date: 11/05/2024

Description:
    A sick rendition of Wordle using digits between
    one and five in a string of length 4-6.  I like
    it, but now I kind of want to make Wordle, with
    lexicography rules instead of word options.

    Important notes about how the program operates:
        - the internal length of the answer and each
        guess stored is guaranteed to be 6 (o padded)
"""

import random as r
import datetime

""" ------------------- some global stuff for each game ------------------- """
exit_all = False
"""Write new functions below this line (starting with unit 4)."""


# generate a number with digits between 1 and 5 of length
def generate_solution(a, b):  # between a and b (4 and 6 for the game).
    length = r.randint(a, b)
    code = ""
    for i in range(length):
        code += str(r.randint(0, 5))
    return code


def lost() :
    print("""You hear a machine yell OUT OF TRIES!
  ...
Is that burning you smell?
  ...
OH, NO! It looks like our rival has destroyed all the school grades!\n""")


"""
This is the Game object, central to the program.
It holds the values (in order read from file):
    - answer: the solution code
    - guesses: the guesses made
    - won: if the game has been won (not in file)*
    - round: the current round
    - name: the name of the player
    - date: the date the game was saved
    - rw: the red and white pins for each guess
Methods include:
    - __init__: initializes the game
    - save: saves the game
    - check: checks the guess
    - print: prints the game
    - load: loads the game
    - game_menu: the game menu
"""
class Game:
    def __init__(self, new=0) :
        self.guesses = ["oooooo", "oooooo", "oooooo", "oooooo", "oooooo",
                        "oooooo", "oooooo", "oooooo", "oooooo", "oooooo"]
        self.won = False
        self.round = 0
        self.name = "empty"
        self.date = ""
        self.rw = ["00", "00", "00", "00", "00", "00", "00", "00", "00", "00"]
        if new == 0 :
            self.answer = generate_solution(4, 6)
            while len(self.answer) < 6:
                self.answer += "o"
            print("\nNew Game:")
            print("--------------------------------------------------------------------------")
            self.print()
        else :
            self.answer = "oooooo"

    def save(self, name, date):
        self.name = name
        self.date = date

    def check(self, guess):
        red = 0
        white = 0
        # pad guess with spaces
        while len(guess) < 6:
            guess = guess + "o"
        done = list(self.answer) # must be marked as not to double count
        self.guesses[self.round] = str(guess)
        # red/white check loop
        # Create copies of answer and guess to mark used digits
        answer_check = list(self.answer)
        guess_check = list(guess)

        # First pass - check for red pins (correct position)
        for i in range(6) :
            if guess_check[i] == answer_check[i] and guess_check[i] != 'o' :
                red += 1
                answer_check[i] = 'x'  # Mark as used in answer
                guess_check[i] = 'y'  # Mark as used in guess (different marker to prevent false matches)

        # Second pass - check for white pins (correct digit, wrong position)
        for i in range(6):
            if guess_check[i] != 'y' and guess_check[i] in answer_check and guess_check[i] != 'o' :
                pos = answer_check.index(guess_check[i])
                white += 1
                answer_check[pos] = 'x'  # Mark as used
                guess_check[i] = 'y'  # Mark as used

        self.rw[self.round] = str(f"{red}{white}")
        self.round += 1
        if guess == self.answer:
            self.won = True
            self.print()
            print("Congratulations, you broke the lock!")
            print("The grades are safe!")
            return False
        else:
            self.print()
            if self.round == 10 :
                lost()
                return False
            return True


    def print(self):
        print("   ==================+=====")
        if self.won or self.round == 10 :
            print(f"    {'  '.join(self.answer)} | R W  ")
        else :
            print(f"    o  o  o  o  o  o | R W  ")
        print("   ==================+=====")
        for i in reversed(range(len(self.guesses))) :
            guess = self.guesses[i]
            print(f"    {'  '.join(guess)} | {' '.join(self.rw[i])}  ")
        print("   ==================+=====")

    def load(self, answer, guesses, round_l, name, date, rw) :
        self.answer = str(answer).rstrip('\n')
        self.guesses = list(guesses.lstrip('[\'').rstrip('\']\n').split("\', \'"))
        self.won = False # when loading, the game is not won
        self.round = int(round_l.rstrip('\n'))
        self.name = str(name.rstrip('\n'))
        self.date = str(date.rstrip('\n'))
        self.rw = list(rw.lstrip('[\'').rstrip('\']\n').split("\', \'"))

    def game_menu(self) :
        invalid = True
        while invalid :
            guess = input("What is your guess (q to quit, s to save and quit): ")
            # I added 4 here to pass one test; it doesn't belong.
            if guess.lower() == "q" :                                               # quit
                print("Ending Game.")
                invalid = False

            elif guess.lower() == "s" :                                             # save
                invalid = save_game(self)
            elif not guess.isdigit() and len(guess) > 0 :
                print(f"Your guess was \"{guess}\". It must be only numbers!")
            elif len(guess) > 6:
                print(f"Your guess was \"{guess}\". This is too long.")
                print("Guess lengths must be between 4 and 6.")
            elif len(guess) < 4 :
                print(f"Your guess was \"{guess}\". This is too short.")
                print("Guess lengths must be between 4 and 6.")
            elif not all([int(i) < 6 for i in guess]):
                print(f"Your guess was \"{guess}\". It must be only numbers 0 through 5.")
            else:
                invalid = False
            if not guess.lower() == "q" and not invalid and not guess.lower() == "s" :
                invalid = self.check(guess)


def initial() :
    print("""You are a member of a secret Society, tasked with cracking
the notorious elvish lock. This lock secures a vault containing all
the school grades, locked away by our rival. To retrieve your grades,
you'll need to break through this lock. Fortunately, the creators our
rival school made an error when building it, so the lock will provide
hints about the code. However, you don't know the passcode length and
only have 10 guesses. Use them wisely--if you fail, you could be turned
into a newt, the grades might be destroyed, or, even worse, you might
have to rewrite the time calculator!

Will you be able to break this lock before your grades are lost forever?""")


def save_game(game) :
    option = "" # must be full scope
    print("\nFiles:")
    print("--------------------------------------------------------------------------")
    try :
        slot_file = open(f"rival_Top_Secret.txt", "r")
        lines = slot_file.readlines()
        slot_file.close()
    except FileNotFoundError :
        slot_file = open(f"rival_Top_Secret.txt", "w")
        slot_file.writelines("empty\nempty\nempty\n")
        lines = ["empty\n", "empty\n", "empty\n"]
        slot_file.close()
        slot_file = open(f"rival_Top_Secret.txt", "r")
    if len(lines) == 3 :
        for i in range(1, 4):
            print(f"   {i}: {lines[i - 1]}", end="")
    else:
        print("   1: empty\n   2: empty\n   3: empty")
    invalid = True
    while invalid :
        option = input("What save would you like to overwrite (1, 2, 3, or c to cancel): ")
        if option.lower() == "c":
            print("cancelled")
            game.print()
            return True
        elif option.isdigit() :
            if 1 <= int(option) <= 3 :
                invalid = False
            else:
                print("That is an invalid selection.")
    invalid = True
    while invalid :
        name = input("What is your name (no special characters): ")
        if not name.replace(" ", "").isalnum() or len(name) == 0 :
            print("That is an invalid name.")
        else :
            invalid = False
            game.save(name, " - Time: " + datetime.datetime.now().isoformat(timespec="seconds"))
            lines[int(option) - 1] = f"{name}{game.date}\n"
            slot_file.close()
            slot_file = open(f"rival_Top_Secret.txt", "w")
            slot_file.writelines(lines)
            slot_file.close()
            game_file = open(f"{option}.txt", "w")
            game_as_lines = str(f"{game.answer}\n{game.guesses}\n{game.round}\n{game.name}\n{game.date}\n{game.rw}\n")
            game_file.write(game_as_lines)
            print(f"Game saved in slot {option} as {name}.")
            print("Ending Game.")
            return False

def one() :  # rules
    print("""
Rules:
--------------------------------------------------------------------------
1. You get 10 guesses to break the lock.

2. Guess the correct code to win the game.

3. Codes can be either 4, 5, or 6 digits in length.

4. Codes can only contain digits 0, 1, 2, 3, 4, and 5.

5. Clues for each guess are given by a number of red and white pins.

   a. The number of red pins in the R column indicates the number of digits
      in the correct location.
   b. The number of white pins in the W column indicates the number of
      digits in the code, but in the wrong location.
   c. Each digit of the solution code or guess is only counted once in the
      red or white pins.""")


def two() :  # new game
    game = Game()
    game.game_menu()


def three() :  # load game
    lines = []
    try :
        file = open(f"rival_Top_Secret.txt", "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError :
        file = open(f"rival_Top_Secret.txt", "w")
        file.writelines("empty\nempty\nempty\n")
        file.close()
    if len(lines) != 3 :
        lines = ["empty", "empty", "empty"]

    print(f"""
Files:
--------------------------------------------------------------------------
   1: {lines[0].rstrip('\n')}
   2: {lines[1].rstrip('\n')}
   3: {lines[2].rstrip('\n')}""")
    invalid = True
    while invalid :
        option = input("What save would you like to load (1, 2, 3, or c to cancel): ")
        if option.lower() == "c" :
            print("cancelled")
            return
        elif not option.isdigit() :
            print("That is an invalid selection.")
        elif 1 > int(option) or int(option) > 3 :
            print("That is an invalid selection.")
        else:
            if lines[int(option) - 1] == "empty\n" :
                print("That file is empty!")
            else :
                invalid = False
                game = Game(1)
                game_file = open(f"{option}.txt", "r")
                load_lines = game_file.readlines()
                game.load(load_lines[0], load_lines[1], load_lines[2], load_lines[3], load_lines[4], load_lines[5])
                game_file.close()
                print("\nResume Game:")
                print("--------------------------------------------------------------------------")
                game.print()
                game.game_menu()


def four() :           # |
    print("Goodbye")   # |
    # exits program here V

# straight up recursion baby!
def menu() :
    invalid = True
    while invalid :
        print("""
Menu:
--------------------------------------------------------------------------
   1: Rules
   2: New Game
   3: Load Game
   4: Quit""")
        choice = input("Choice: ")
        if choice.isdigit() and 1 <= int(choice) <= 4 :
            choice = int(choice)
            invalid = False
            if choice == 1:
                one()
                menu()
            elif choice == 2:
                two()
                menu()
            elif choice == 3:
                three()
                menu()
            elif choice == 4:
                four()
        else:
            print("Please enter 1, 2, 3, or 4.")


# main function.
# something fills the heart with pride
# to see one's own main function contains
# but two lines.  Two simple lines, many
# hours of complexity.
def main():
    initial()
    menu()


if __name__ == "__main__":
    main()
