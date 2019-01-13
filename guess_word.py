# import random
# import puzzleimg
# from get_word import get_random_word
# from puzzleimg import get_image


# import cgitb
# cgitb.enable()

# status = [] #Current status of guess

# def word_length(word):
#     return len(word)

# def list_joined(status):
#     list_joined = "".join(status)
#     return list_joined

# def full_word(status):
#     for letter in status:
#         if letter is "*":
#             return False
#     return True  

# def check(word,guesses):
#     last_guess = guesses[-1]
#     matches = 0 #Number of occurences of last_guess in word
#     global status
#     count = 0
#     for letter in word:
#         if letter == last_guess:
#             matches += 1
#             status[count] = last_guess
#         count += 1

#     if matches == 0:
#         print ('Sorry. The word has no "',  last_guess, '"s', sep="")
#     elif matches == 1:
#         print("The word has ", matches, ' "', last_guess, '"', sep="" )
#     else:
#         print("The word has ", matches, ' "', last_guess, '"s', sep="")

#     return status

# def main():
#     image = get_image() # the random image
#     word = get_random_word() # the random word
#     n = word_length(word) #the number of letters in the random word
#     global status
#     for letter in word:
#         status.append("*")

#     guesses = [] #the list of guesses made so far
#     guessed = False
#     joined_list = list_joined(status)
#     while not guessed:
#         guess = input('Guess a letter or a {}-letter word (of someone who lives here): '.format(n))
#         guess = guess.upper()
#         if guess in guesses:
#             print('You already guessed "', guess, '."', sep="" )
        
#         else: 
#             guesses.append(guess)

#             if len(guess) != n and len(guess) != 1:
#                 print("Your guess is the wrong length!")

#             elif len(guess) == n:
#                 if guess == word:
#                     guessed = True
#                 else: 
#                     print("Wrong! Try again!")
#                 continue
#             else: 
#                 check(word, guesses)
#                 if full_word(status):
#                     guessed = True
#                     break
#                 joined_list = list_joined(status)
#                 print(joined_list)

#     print('{} is it! It took {} tries.'.format(word, len(guesses)))
    
# main()