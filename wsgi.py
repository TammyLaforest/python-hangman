from flask import Flask, render_template, request, redirect
from flask.views import MethodView
import random

app = Flask(__name__)

status = [] #Current status of guess
guesses = [] #the list of guesses made so far
wrong_guesses = []

word = ""
n = len(word)

num_wrong_guesses = len(wrong_guesses)
guessed = False
image = ()
message = ""


def list_joined(status):
    list_joined = "".join(status)
    return list_joined


@app.route('/')
def index():
	global message
	message = 'Press the New Game button to start.'
	return render_template("index.html", message=message)


def get_image():
	cat1 = 'static/media/cat1.jpg'
	cat2 = 'static/media/cat2.jpg'
	cat3 = 'static/media/cat3.jpg'
	cat4 = 'static/media/cat4.jpg'
	cat5 = 'static/media/cat5.jpg'
	cat6 = 'static/media/cat6.jpg'
	cat7 = 'static/media/cat7.jpg'
	images = [cat1, cat2, cat3, cat4, cat5, cat6, cat7]
	return random.choice(images)


def get_random_word():
	words = ['HISS', 'MEOW', 'PURR', 'CUDDLE', 'SLEEPY', 'KITTY', 'CAT', 'KITTEN', 'CLAWS', 'TAIL', 'FURRY', 'FUR', 'PAWS', 'LITTER', 'PET', 'CALICO', 'TABBY', 'CATNIP', 'FELINE', 'POUNCE']
	return random.choice(words)


@app.route('/new_game')
def new_game():
	global status, guesses, wrong_guesses, num_wrong_guesses, guessed, image, message, word, n 
	# Reset globals for new game
	guessed = False
	status =[]
	guesses = []
	wrong_guesses = []
	image = get_image() 
	word = get_random_word()
	n = len(word)
	
	message = "Your game has started!"
	for letter in word:
		status.append("*")
	joined_list = list_joined(status)
	wrong_list = " ".join(wrong_guesses)
	num_wrong_guesses = len(wrong_list)

	return render_template("new_game.html", joined_list=joined_list, image=image, word=word, n=n, guesses=guesses, message=message,  num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)


def full_word(status):
    for letter in status:
        if letter is "*":
            return False
    return True  




@app.route('/guess', methods=['POST'])
def guess_a_word():
	global guessed, guesses, message, joined_list, n, word, wrong_guesses, status

	while not guessed:
		if request.method == "POST":
			text = request.form['user_input']
			guess = text.upper()
			
			if guess in guesses:
				message = "You already guessed " + guess
			else: 
				guesses.append(guess)
				joined_list = list_joined(status)

				if len(guess) != n and len(guess) != 1:
					message=("Your guess is the wrong length!")

				elif len(guess) == n:
					if guess == word:
						status=word
						joined_list = list_joined(status)
						wrong_list = " ".join(wrong_guesses)
						num_wrong_guesses = len(wrong_list)
						guessed = True
						you_win(joined_list)
						return render_template("win.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)

					else: 
						wrong_guesses.append(guess)
						message=("Wrong! Try again!")
						continue
				else: 
					check(word, guesses)
					if full_word(status):
						status=word
						joined_list = list_joined(status)
						wrong_list = " ".join(wrong_guesses)
						num_wrong_guesses = len(wrong_list)
						guessed = True
						you_win(joined_list)
						return render_template("win.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)
			joined_list = list_joined(status)
			wrong_list = " ".join(wrong_guesses)
			num_wrong_guesses = len(wrong_list)
			return render_template("new_game.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)


def check(word,guesses):
	global status, message
	last_guess = guesses[-1]
	matches = 0 # Number of occurences of last_guess in word
	count = 0
	for letter in word:
		if letter == last_guess:
			matches += 1
			status[count] = last_guess
		count += 1

	if matches == 0:
		wrong_guesses.append(last_guess)
		message='Sorry. The word has no ' + last_guess + 's'
	elif matches == 1:
		message='The word has ' + str(matches) + " " + last_guess 
	else:
		message='The word has ' + str(matches) + " " + last_guess+'s'
	return status


@app.route('/win')
def you_win(joined_list):
	global message
	message=('{} is it! It took {} tries.'.format(word, len(guesses)))

if __name__ == '__main__':
	app.run()