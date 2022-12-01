import sys
import random

nrows = int(sys.argv[1])
prob = float(sys.argv[2])

if len(sys.argv) > 5:
	nsim = int(sys.argv[3])

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

def get_exp_rows(prob_of_l):

	n_pieces = nrows - 1
	
	expectations = {(nrows, nrows, nrows): nrows}
	best_moves_long = {(nrows, nrows, nrows) : None}
	best_moves_l = {(nrows, nrows, nrows) : None}
	

	while n_pieces >= 0:
	
		for board in all_boards_with_n_pieces(n_pieces, nrows):
			#print("ay")
			long_board = add_long(board)
			l_board = add_l(board)
	
			max_long_exp = min(board)
			max_l_exp = min(board)
	
			best_long_move = board
			best_l_move = board
	
			for i in long_board:
				if tuple(i) in expectations and expectations[tuple(i)] > max_long_exp:
					best_long_move = i
					max_long_exp = min(i)
					
	
			for i in l_board:
				if tuple(i) in expectations and expectations[tuple(i)] > max_l_exp:
					best_l_move = i
					max_l_exp = min(i)
	
			expectations[tuple(board)] = min(board)

			stend = " " + str(best_l_move) + " " + str(expectations[tuple(best_l_move)]) + " " + str(best_long_move) + " " + str(expectations[tuple(best_long_move)])

			expectations[tuple(board)] = prob_of_l * expectations[tuple(best_l_move)] + (1 - prob_of_l) * expectations[tuple(best_long_move)]

			#print(str(board) + " " + str(expectations[tuple(board)]) + stend)

			best_moves_long[tuple(board)] = best_long_move
			best_moves_l[tuple(board)] = best_l_move
	
		n_pieces -= 1

	#print(expectations)
	return(expectations[(0, 0, 0)])

print("expected rows filled (p = " + str(prob) + "): " + str(get_exp_rows(prob)))

"""
min_prob = 1
for i in range(0, 101):
	prob = i / 100	
	win_prob = get_win_prob(prob)
	if win_prob < min_prob:
		min_prob = win_prob
		best = prob
	print("theoretical win chance (p = " + str(prob) + "): " + str(win_prob))
print(best)

"""
if len(sys.argv) < 4:
	quit()
	
nsim = int(sys.argv[3])

print("running simulations...")

tot_rows = 0

for i in range(nsim):

	#print("simulation #" + str(i))
	board = [0, 0, 0]
	row_count = 0
	while board != [nrows, nrows, nrows]:
		row_count = min(row_count, min(board))
		#print_board(board)
		if random.random() > prob:
			board = best_moves_long[tuple(board)]
		else:
			board = best_moves_l[tuple(board)]

		if board == None:
			
			break

	tot_rows += row_count





print("observed win chance: " + str(tot_rows / nsim))