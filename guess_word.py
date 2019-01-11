import random

status = [] #Current status of guess
def list_joined(status):
    list_joined = "".join(status)
    return list_joined

def full_word(status):
    for letter in status:
        if letter is "*":
            return False
    return True  


def get_word():
    '''Returns random word.'''
    # words = ['Charlie', 'Woodstock', 'Snoopy', 'Lucy', 'Linus',
    #          'Schroeder', 'Patty', 'Sally', 'Marcie',]

    words = ['Tammy', 'Jeana', 'Rose', 'Lucy', 'Slater', 'Toonces']

    return random.choice(words).upper()

def check(word,guesses):
    '''Creates and returns string representation of word
    displaying asterisks for letters not yet guessed.'''
    
    last_guess = guesses[-1]
    matches = 0 #Number of occurences of last_guess in word
    global status
    count = 0
    for letter in word:
        if letter == last_guess:
            matches += 1
            status[count] = last_guess
        count += 1

    if matches == 0:
        print ('Sorry. The word has no "',  last_guess, '"s', sep="")
    elif matches == 1:
        print("The word has ", matches, ' "', last_guess, '"', sep="" )
    else:
        print("The word has ", matches, ' "', last_guess, '"s', sep="")

    return status

def main():
    word = get_word() #the random word
    n = len(word) #the number of letters in the random word
    global status
    for letter in word:
        status.append("*")
    
    guesses = [] #the list of guesses made so far
    guessed = False
    # print('+++++++++  The word contains {} letters.'.format(n))
    joined_list = list_joined(status)
    while not guessed:
        guess = input('Guess a letter or a {}-letter word (of someone who lives here): '.format(n))
        
     
        guess = guess.upper()
        
        if guess in guesses:
            print('You already guessed "', guess, '."', sep="" )
        
        else: 
            guesses.append(guess)

            if len(guess) != n and len(guess) != 1:
                print("Your guess is the wrong length!")

            elif len(guess) == n:
                if guess == word:
                    guessed = True
                else: 
                    print("Wrong! Try again!")
                continue
            else: 
                check(word, guesses)
                if full_word(status):
                    guessed = True
                    break
                joined_list = list_joined(status)
                print(joined_list)

    print('{} is it! It took {} tries.'.format(word, len(guesses)))
    
main()

    #Loop through word checking if each letter is in guesses
    #  If it is, append the letter to status
    #  If it is not, append an asterisk (*) to status
    #Also, each time a letter in word matches the last guess,
    #  increment matches by 1.

    #Write a condition that outputs one of the following when
    #  the user's last guess was "A":
    #   'The word has 2 "A"s.' (where 2 is the number of matches)
    #   'The word has one "A".'
    #   'Sorry. The word has no "A"s.'      



        #Write an if condition to complete this loop.
        #You must set guessed to True if the word is guessed.
        #Things to be looking for:
        #  - Did the user already guess this guess?
        #  - Is the user guessing the whole word?
        #     - If so, is it correct?
        #  - Is the user guessing a single letter?
        #     - If so, you'll need your check() function.
        #  - Is the user's guess invalid (the wrong length)?
        #
        #Also, don't forget to keep track of the valid guesses.