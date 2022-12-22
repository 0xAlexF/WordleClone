from tkinter import *
import random
import requests

g_board = []																									#	5x6 Grid of labels	
g_keyBoardButtons = []				
g_guessCol = 0														
g_guessMin = 0																									#	Lowest possible col value (Prevent deleting into negatives and another row)
g_guessCount = 0																								#	Number of letters for current word (i.e. Users guessing -> T O P X X = 2)
g_answer = ""	
g_gameOver = False
g_selectWord = True
g_gameOverFrame = None
g_gameOverLabel = None

def UpdateKey(char, color):
	global g_keyBoardButtons
	for k in g_keyBoardButtons:
		if  k["text"] == char:
			k["relief"] = SUNKEN
			if k["bg"] == "#FFBA01" and color == "#008000": k["bg"] = color
			if k["bg"] == "#008000" or k["bg"] == "#FFBA01": return
			k["bg"] = color
			
def TestLetter(letter, testWord):
	global g_guessCol
	global g_board
	global g_guessMin

	index = 5
	counter = g_guessCol
	while counter > g_guessMin:
		counter -= 1
		index -= 1
		if letter == g_board[counter]["text"]:																	#	Found letter in answer
			if g_board[counter]["bg"] == "#008000" or g_board[counter]["bg"] == "#FFBA01": continue				#	If there is multiple of the same letters skip if already found/highlighted
			if testWord[index] ==  g_board[counter]["text"]:													#	Letter in same place as answer
				g_board[counter]["bg"] = "#008000"
				UpdateKey(g_board[counter]["text"], "#008000")
			else:																								#	Letter in different place than answer
				g_board[counter]["bg"] = "#FFBA01"																
				UpdateKey(g_board[counter]["text"], "#FFBA01")
			return
		else:																									#	Letter not found in answer
			UpdateKey(g_board[counter]["text"], "#111111")
			if g_board[counter]["bg"] == "#008000" or g_board[counter]["bg"] == "#FFBA01": continue				#	Letter found in previous iterator dont change to dark color		
			g_board[counter]["bg"] =  "#111111"
		
def CheckWord():
	global g_guessCol
	global g_board
	global g_answer
	global g_gameOver
	global g_guessCol
	global g_gameOverFrame
	global g_gameOverLabel

	ans = g_answer
	guess = g_board[g_guessCol - 5]["text"] + g_board[g_guessCol - 4]["text"] + \
		    g_board[g_guessCol - 3]["text"] + g_board[g_guessCol - 2]["text"] + \
		    g_board[g_guessCol - 1]["text"]
	url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + guess
	req = requests.get(url)
	res = req.json()
	for key in res:																								#	If word not found first key in dictionary is "title"
		if key == "title": return False
		break
	for letter in ans:																							#	Check if letters are in answer
		TestLetter(letter, ans)

	if guess == ans:																							#	Game over condition guessed word
		g_gameOverLabel["text"] = "Correct Answer!"
		g_gameOverLabel["fg"] = "#008000"
		g_gameOverFrame.pack(expand=True)
		g_gameOverFrame.place(relx = 0.5, rely = 0.4, anchor="center")
		g_gameOver = True
	if g_guessCol == 30:																						#	Game over condition used up # of tries
		g_gameOverLabel["fg"] = "#FF0000"
		g_gameOverLabel["text"] = "Correct Answer: \n" + g_answer
		g_gameOverFrame.pack(expand=True)
		g_gameOverFrame.place(relx = 0.5, rely = 0.4, anchor="center")
		g_gameOver = True
	return True
			
def AddLetter(letter):
	global g_guessCol
	global g_guessCount
	global g_board
	global g_guessMin
	global g_gameOver
	global g_gameOverFrame
	global g_gameOverLabel
	global g_answer

	if g_gameOver: return

	if letter == "Enter":																						#	Check if it is a valid word
		if g_guessCount == 5:																							
			if not CheckWord(): return																						
			g_guessMin = g_guessCol
			g_guessCount = 0
		return

	if letter == "DEL":							
		g_guessCol -= 1 
		g_guessCount -= 1
		if g_guessCol < g_guessMin:																				#	Ensures correct index and deletion from correct row 
			g_guessCol = g_guessMin 
			g_guessCount = 0
		g_board[g_guessCol]["text"] = ""
		return
	if g_guessCount > 4: return					

	g_board[g_guessCol]["text"] = letter		
	g_guessCol += 1
	g_guessCount += 1

def SetupBoard(arry, fr):
	r = 0
	c = 0
	index = 0
	while r < 6:
		while c < 5:
			arry.append(Label( fr, text=" ", padx=20, pady=10, width=1, height=1, font=("Arial 40 bold"), bg="#333333", fg="white"))
			arry[index].grid(column=c, row=r, pady=3, padx=3)	
			index += 1
			c += 1
		c = 0
		r += 1

def SetupKeyBoard(arry, fr):
	topLetters 		=	 ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
	middleLetters   =  	 ["A", "S", "D", "F", "G", "H", "J", "K"]
	bottomLetters   =  	 ["Enter", "L", "Z", "X", "C", "V", "B", "N", "M", "DEL"]
	col = 0
	letterIndex = 0	
	i = 0;
	while col < len(topLetters):
		arry.append(Button(fr, text=topLetters[letterIndex], padx=17, pady=20, width=1, height=1, font=("Arial 13 bold"), bg="#333333", fg="white", 
					command=lambda l=topLetters[letterIndex]: AddLetter(l)))
		arry[i].grid(column=col, row=0, pady=2, padx=2)	
		col += 1
		i += 1
		letterIndex += 1

	col = 1
	letterIndex = 0
	while col < len(middleLetters) + 1:
		arry.append(Button(fr, text=middleLetters[letterIndex], padx=17, pady=20, width=1, height=1, font=("Arial 13 bold"), bg="#333333", fg="white",
					command=lambda l=middleLetters[letterIndex]: AddLetter(l)))
		arry[i].grid(column=col, row=1, pady=2, padx=2)	
		col += 1
		i += 1
		letterIndex += 1

	col = 0
	letterIndex= 0
	while col < len(bottomLetters):
		arry.append(Button(fr, text=bottomLetters[letterIndex], padx=17, pady=20, width=1, height=1, font=("Arial 13 bold"), bg="#333333", fg="white",
					command=lambda l=bottomLetters[letterIndex]: AddLetter(l)))
		arry[i].grid(column=col, row=2, pady=2, padx=2)	
		col += 1
		i += 1
		letterIndex += 1

def GetRandomWord():
	global g_answer
	global g_selectWord

	dic = open("words.txt", "r")
	num = random.randint(0, 2499)
	for x in range(num):
		g_answer = dic.readline()
	g_selectWord = False
	g_answer = g_answer.upper()
	g_answer = g_answer.strip()
	dic.close()
	#print(g_answer)

def NewGame():
	global g_gameOver
	global g_guessCol												
	global g_guessMin																							
	global g_guessCount
	global g_gameOverFrame
	global g_board
	global g_keyBoardButtons

	g_gameOver = False
	g_guessCol = 0
	g_guessMin = 0
	g_guessCount = 0
	g_gameOverFrame.place(relx = 0, rely = -1, anchor="center")
	GetRandomWord()

	for b in g_board:
		b["text"] = ""
		b["bg"] = "#333333"

	for k in g_keyBoardButtons:
		k["bg"] = "#333333"
		k["relief"] = RAISED

def main():
	global g_gameOver
	global g_selectWord
	global g_gameOverFrame
	global g_gameOverLabel

	if g_selectWord:
		GetRandomWord()

	WIDTH = 600
	HEIGHT = 900
	window = Tk()
	window.title("Wordle Clone")
	window.geometry(str(WIDTH) + 'x' + str(HEIGHT))
	window.configure(bg = "#141517")

	title = Label(window, text="Wordle", font=("Arial 40 bold"), bg="#141517", fg="white")
	title.place(relx = 0.5, rely = 0.06, anchor="center")

	boardFrame = Frame(window, bg="#141517")
	SetupBoard(g_board, boardFrame)

	keyBoardFrame = Frame(window, bg="#141517")
	SetupKeyBoard(g_keyBoardButtons,keyBoardFrame)

	g_gameOverFrame = Frame(window, bg="#141517")

	g_gameOverLabel = Label(g_gameOverFrame, text="", padx=100, pady=30, width=1, height=1, font=("Arial 20 bold"), bg="#141517", fg="#008000")
	g_gameOverLabel.grid(column=0, row=0, padx=10, pady=17)	
	playAgainB = Button(g_gameOverFrame, text="Play Again?", padx=50, pady=10, width=1, height=1, font=("Arial 10 bold"), bg="#008000", fg="white",command=NewGame)
	playAgainB.grid(column=0, row=1, pady=5)	
	
	keyBoardFrame.pack(expand=True)
	keyBoardFrame.place(relx = 0.5, rely = 0.85, anchor="center")

	boardFrame.pack(expand=True)
	boardFrame.place(relx = 0.5, rely = 0.4, anchor="center")
		
	window.mainloop()

if __name__ == "__main__":
	main()
	
		
		
