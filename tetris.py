"""
Usage: 

>> python3 tetris.py [nrows] [prob of L piece] [--win || --exp] [--simulate nsim]?

"""

import sys
import random

if __name__ == "__main__":

	if len(sys.argv) < 4:
		print("not enough inputs! usage is the following:")
		print(">> python3 confustedtetris.py [nrows] [prob of L piece] [--win || --exp] [ngames] [nsim per game]")
		quit()

	nrows = int(sys.argv[1])
	prob = float(sys.argv[2])
	win_or_exp = sys.argv[3]

def add_long(board):
	# returns all possible configurations after adding a long tile

	ls = []
	if board[0] == board[1] and board[1] == board[2]:
		ls.append([i + 1 for i in board])

	ls.append([board[0] + 3, board[1], board[2]])
	ls.append([board[0], board[1] + 3, board[2]])
	ls.append([board[0], board[1], board[2] + 3])

	return(ls)

def add_l(board):
	ls = []

	# first two statements: can we drop it with the pointy bit facing down?
	# last statement: can we drop it flat?

	if board[0] + 1 == board[1]:
		ls.append([board[0] + 2, board[1] + 1, board[2]])
	elif board[0] == board[1] + 1:
		ls.append([board[0] + 1, board[1] + 2, board[2]])
	elif board[0] == board[1]:
		ls.append([board[0] + 1, board[1] + 2, board[2]])
		ls.append([board[0] + 2, board[1] + 1, board[2]])

	if board[1] + 1 == board[2]:
		ls.append([board[0], board[1] + 2, board[2] + 1])
	elif board[1] == board[2] + 1:
		ls.append([board[0], board[1] + 1, board[2] + 2])
	elif board[1] == board[2]:
		ls.append([board[0], board[1] + 2, board[2] + 1])
		ls.append([board[0], board[1] + 1, board[2] + 2])

	return(ls)

def print_board(board):
	bottom_up = []
	for i in range(max(board)):
		str = ""
		if board[0] > i:
			str += "x"
		else: str += "."
		if board[1] > i:
			str += "x"
		else: str += "."
		if board[2] > i:
			str += "x"
		else: str += "."

		bottom_up.append(str)

	print()
	print("board: ")
	print()
	while bottom_up:
		print(bottom_up.pop())

	print()
	return()

def all_boards_with_n_pieces(n, max_height):
	ls = []
	for first_col in range(min(max_height, 3 * n) + 1):
		remaining_blocks = 3 * n - first_col
		for second_col in range(min(max_height, remaining_blocks) + 1):
			third_col = remaining_blocks - second_col
			if third_col <= max_height:
				ls.append([first_col, second_col, third_col])

	return(ls)

def get_win_prob(nrows, prob_of_l, win_or_exp):

	n_pieces = nrows - 1
	
	if win_or_exp == "--win":
		values = {(nrows, nrows, nrows): 1, (nrows, nrows, nrows): 1}
	else:
		values = {(nrows, nrows, nrows): nrows, (nrows, nrows, nrows): nrows}

	best_moves = {((nrows, nrows, nrows), "L"): None, ((nrows, nrows, nrows), "I"): None}
	
	while n_pieces >= 0:
	
		for board in all_boards_with_n_pieces(n_pieces, nrows):
			
			if win_or_exp == "--win":
				max_vals = {"I": 0, "L": 0}
			else:
				max_vals = {"I": min(board), "L": min(board)}

			for piece in ["L", "I"]:
				
				if piece == "I":
					boards = add_long(board)
				else:
					boards = add_l(board)

				max_val = 0
				if win_or_exp == "--exp":
					max_val = min(board)
				best_move = None

				for i in boards:
					if tuple(i) in values and values[tuple(i)] > max_val:
						max_val = values[tuple(i)]
						best_move = i
		
				best_moves[(tuple(board), piece)] = best_move
				max_vals[piece] = max_val

			#print(board)
			#print(max_vals)
			values[tuple(board)] = prob_of_l * max_vals["L"] + (1 - prob_of_l) * max_vals["I"]
	
		n_pieces -= 1

	#print(values)
	#print(best_moves)

	return(values[(0, 0, 0)], best_moves)

if __name__ == "__main__":
	if win_or_exp == "--win":
		print("theoretical win chance (@ p = " + str(prob) + "): " + str(get_win_prob(nrows, prob, win_or_exp)[0]))
	else:
		print("expected rows filled (@ p = " + str(prob) + "): " + str(get_win_prob(nrows, prob, win_or_exp)[0]))

if len(sys.argv) > 4 and __name__ == "__main__":
	
	nsim = int(sys.argv[5])

	print("running simulations...")

	nlosses = 0
	nrows_filled = 0

	dic = get_win_prob(nrows, prob, win_or_exp)[1]

	for i in range(nsim):

		nrows_filled_this_sim = 0

		#print("simulation #" + str(i))
		board = [0, 0, 0]

		while board != [nrows, nrows, nrows]:
			#print_board(board)
			if random.random() > prob:
				piece = "I"
			else:
				piece = "L"
			
			nrows_filled_this_sim = min(board)
			board = dic[(tuple(board), piece)]
	
			if board == None:
				nlosses += 1
				nrows_filled += nrows_filled_this_sim
				break

		if board == [nrows, nrows, nrows]:
			nrows_filled += nrows

	if win_or_exp == "--win": 
		print("observed win chance: " + str(1 - nlosses / nsim))
	else: 
		print("avg. rows filled: " + str(nrows_filled / nsim))