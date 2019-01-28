from flask import Flask, render_template, request, redirect, url_for,  make_response, session
from flask_session.__init__ import Session
from flask.views import MethodView
from tempfile import mkdtemp
import random

app = Flask(__name__)


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/index')
@app.route('/')
def index():
	return render_template("index.html")

# Rock, Paper, Scissors

choices = ['rock', 'paper', 'scissors']

@app.route('/rps')
def rps():
	session.clear()
	session["humanscore"] = 0
	session["aiscore"] = 0
	message="Choose Rock, Paper or Scissors to Start Game"
	return render_template("rps.html", message=message, humanscore=session["humanscore"], aiscore=session["aiscore"])

# session["humanscore"] = 0
# session["aiscore"] = 0

@app.route("/rps/<choice>")
def playrps(choice):

	session["aichoice"] = random.choice(choices)
	print(choice)
	aichoice = session["aichoice"]
	session["humanchoice"] = choice
	print(aichoice)

	if aichoice == choice:
		print("this thing")
		session["message"]="Draw!"

	elif session["aichoice"] == 'rock':
		if choice == "paper":
			session["message"]= "You win!"
			session["humanscore"] +=1
		else:
			session["message"]= "You lose! Try again."
			session["aiscore"]+=1
	
	elif session["aichoice"] == 'paper':
		if choice == "scissors":
			session["message"]= "You win!"
			session['humanscore'] +=1
		else:
			session["message"]= "You lose! Try again."
			session['aiscore']+=1
	
	else:
		if choice == 'rock':
			session["message"] = "You win!"
			session['humanscore']+=1
		else:
			session["message"]= "You lose! Try again."
			session['aiscore']+=1
	
	message=session["message"]
	humanscore=session["humanscore"]
	aiscore=session["aiscore"]
	humanchoice=session["humanchoice"]

	if aiscore > humanscore:
		winning="red"
	else:
		winning="black" 

	# return render_template("rps.html",  aichoice=aichoice, humanchoice=humanchoice)

	return render_template("rps.html", message=message, humanscore=humanscore, aiscore=aiscore, aichoice=aichoice, humanchoice=humanchoice, winning=winning)


# Tic Tac Toe

@app.route("/tictactoe_home")
def tictactoe_home():
		session.clear()
		session["won"] = True
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["turn"] = "X"
		session["message"] = "Start a New Game"

		return render_template("play_tictactoe.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )
 
@app.route("/new_game")
def new_game():
		session.clear()
		session["message"] = "Begin! X goes first."
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["turn"] = "X"
		session["won"] = False
		session["count"] = 0

		board = session["board"]
		return render_template("play_tictactoe.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
	session["board"][row][col] = session["turn"]
	turn = session ["turn"]
	board = session["board"]
	session["message"] = score(row, col)
	if session["message"] == "Draw!":
		return render_template("play_tictactoe.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])

	# Change the turn
	if session["turn"] == "X":
		session["turn"] = "Y"
	else: 
		session["turn"] = "X"
	session["count"] += 1
	print(session["count"])
	return render_template("play_tictactoe.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])


def score(row, col):
		board = session["board"]
		turn = session ["turn"]
		
		if (board[row][0] == board[row][1] == board[row][2] 
			or board[0][col] == board[1][col] == board[2][col]):
			session["won"] = True
			return f"{ turn } wins!"
			
		elif board[1][1] is not None:
			if (board[0][0] == board[1][1] == board[2][2] 
			or board[2][0] == board[1][1] == board[0][2]):
				if board[1][1] == turn:
					session["won"] = True
					return f" {turn } Wins!"
			
			elif session["count"] == 9:
				return "Draw!"
			else:
				return "Try Again!"

		else:
			if turn == "X":
				return "It is Y's turn."
			else:
				return "Your move!"


@app.route("/ai_game")
def ai_game():
		session.clear()
		session["message"] = "New game. Human goes first."
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["scores"] = [[0, 0, 0,], [0, 0, 0], [0, 0, 0]]
		session["turn"] = "X"
		session["won"] = False
		session["count"] = 0

		board = session["board"]
		return render_template("playai_tictactoe.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )


@app.route("/playai/<int:row>/<int:col>")
def playai(row, col):
	
	session["board"][row][col] = session["turn"]

	session["scores"][row][col] = 1
	session["count"] += 1
	session["message"] = score(row, col)
	if session["message"] == "Draw!":
		return render_template("play_tictactoe.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])

	
	session["turn"] = "Y"
	
	row, col = computer_choice()
	session["board"][row][col] = session["turn"]
	session["scores"][row][col] = -3
	session["count"] += 1
	
	session["message"] = score(row, col)
	if session["message"] == "Draw!":
		return render_template("play_tictactoe.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])

	
	session["turn"] = "X" 

	return render_template("playai_tictactoe.html", game=session["board"], message=session["message"], won =session["won"])



def computer_choice():
	board = session["board"]
	scores = session ["scores"]
	turn = session ["turn"]
	corners = (0, 2)
	

	# If player one doesn't choose the center in their first move, choose the center. Otherwise choose a corner. 
	if session["count"] == 1:
		if board[1][1] is None:
			return 1, 1
		else:
			return random.choice(corners), random.choice(corners)
	
	# If there is a chance of playing a winning move, play that first. 
	# Check for horizontal wins. 
	else:
		for i in range(3):
			if sum(scores[i]) == -6:
				for j in range(3):
					if board[i][j] != "Y":
						return i, j

	# Check for vertical wins.
		for j in range(3):
			if (scores[0][j] + scores[1][j] + scores[2][j]) == -6:
				for i in range(3):
					if board[i][j] != "Y":
						return i, j

	# Check for first diagonal win. 
		if scores[0][0] + scores[1][1] + scores[2][2] == -6:
			if board[0][0] != "Y":
				return  0, 0
			else:
				return 2, 2

	# Check for second diagonal win. 
		elif scores[0][2] + scores[1][1] + scores[2][0] == -6:
			if board[0][2] != "Y":
				return 0, 2
			else:
				return 2, 0		

	# If a win isn't an option, check if there is the immediate threat of defeat.
	# Check for horizontal threats. 
		for i in range(3):
			if sum(scores[i]) == 2:
				for j in range(3):
					if board[i][j] != "X":
						return i, j

	# Check for vertical threats.
		for j in range(3):
			if (scores[0][j] + scores[1][j] + scores[2][j]) == 2:
				for i in range(3):
					if board[i][j] != "X":
						return i, j

	# Check for first diagonal threat. 
		if scores[0][0] + scores[1][1] + scores[2][2] == 2:
			if board[0][0] != "X":
				return  0, 0
			else:
				return 2, 2
	
	# Check for second diagonal threat. 
		elif scores[0][2] + scores[1][1] + scores[2][0] == 2:
			if board[0][2] != "X":
				return 0, 2
			else:
				return 2, 0		

	# Else, find an empty spot and take it. 
		else: 
			for i in range(3):
				for j in range(3):
					if board[i][j] != "X" and board[i][j] != "Y":
						return  i, j


# Hangman

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

@app.route('/guesstheword')
def guesstheword():
	global message
	message = 'Press the New Game button to start.'
	return render_template("guesstheword.html", message=message)

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

@app.route('/new_word')
def new_word():
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

	return render_template("new_word.html", joined_list=joined_list, image=image, word=word, n=n, guesses=guesses, message=message,  num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)


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
			lenguess = len(guess)
			print(lenguess)

			if len(guess) != n and len(guess) != 1:
				message=("Your guess is the wrong length!")
				guesses.append(guess)
				joined_list = list_joined(status)
				wrong_list = " ".join(wrong_guesses)
				num_wrong_guesses = len(wrong_list)
				return render_template("new_word.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)

			else: 
				if guess in guesses:
					message = "You already guessed " + guess
					joined_list = list_joined(status)
					wrong_list = " ".join(wrong_guesses)
					num_wrong_guesses = len(wrong_list)
					return render_template("new_word.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)

				else:
					guesses.append(guess)
					if len(guess) == n:
						if guess == word:
							guessed = True
							status=word
							joined_list = list_joined(status)
							wrong_list = " ".join(wrong_guesses)
							num_wrong_guesses = len(wrong_list)
							you_win(joined_list)
							return render_template("win_word.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)

						else: 
							wrong_guesses.append(guess)
							message=("Wrong! Try again!")
							joined_list = list_joined(status)
							wrong_list = " ".join(wrong_guesses)
							num_wrong_guesses = len(wrong_list)
							return render_template("new_word.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)	
					else: 
						check(word, guesses)
						if full_word(status):
							guessed = True
							status=word
							joined_list = list_joined(status)
							wrong_list = " ".join(wrong_guesses)
							num_wrong_guesses = len(wrong_list)
							you_win(joined_list)
							return render_template("win_word.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)
							

		joined_list = list_joined(status)
		wrong_list = " ".join(wrong_guesses)
		num_wrong_guesses = len(wrong_list)
		return render_template("new_word.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)
	joined_list = list_joined(status)
	wrong_list = " ".join(wrong_guesses)
	num_wrong_guesses = len(wrong_list)
	you_win(joined_list)
	return render_template("win_word.html", joined_list=joined_list, image=image, word=word, n=n, message=message, num_wrong_guesses= num_wrong_guesses, wrong_list=wrong_list)

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