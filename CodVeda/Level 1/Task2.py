# -- NUMBER GUESSING GAME --

import random


def guess(x):
    random_number = random.randint(1, x)
    guess = 0
    while guess != random_number:
        guess = int(input(f'Guess a number between 1 and {x}: \n'))
        if guess > random_number:
            print('Oops your number is too high')
        elif guess < random_number:
            print('Oops your number is too low')
        else:
            print('Yay nice try')


def main():
    guess(100)

    play_again = input('Would you like to try again? (yes/no) ')
    while play_again.lower() == 'yes':
        guess(100)
        play_again = input('Would you like to try again? (yes/no) ')

    print('You have done well')


if __name__ == '__main__':
    main()