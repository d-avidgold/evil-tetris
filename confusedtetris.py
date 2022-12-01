"""
Usage:

>> python3 confustedtetris.py [nrows] [prob of L piece] [--win || --exp] [nrounds] [nsim per game] [--fast epsilon]*

We let the agent play a certain number of rounds: each round is a series of of consecutive "confused tetris" games, in which knowledge from one game carries over to the next.

the --fast tag makes it so that the agent no longer updates the dictionary after every new piece, only doing so once the gap between estimates reaches a certain threshold.

"""

import sys
import random
import tetris

if __name__ == "__main__":

	if len(sys.argv) < 6:
		print("not enough inputs! usage is the following:")
		print(">> python3 confustedtetris.py [nrows] [prob of L piece] [--win || --exp] [ngames] [nsim per game]")
		quit()
	
	nrows = int(sys.argv[1])
	prob = float(sys.argv[2])
	win_or_exp = sys.argv[3]
	
	ngames = int(sys.argv[4])
	nsim = int(sys.argv[5])
	
	speed = "--slow"
	epsilon = 1
	if len(sys.argv) > 6:
		speed = sys.argv[6]
		epsilon = float(sys.argv[7])

	if win_or_exp == "--win":
		print("[benchmark] ideal win chance (@ p = " + str(prob) + "): " + str(tetris.get_win_prob(nrows, prob, win_or_exp)[0]))
	else:
		print("[benchmark] ideal rows filled (@ p = " + str(prob) + "): " + str(tetris.get_win_prob(nrows, prob, win_or_exp)[0]))

def run_one_game(nrows, prob_of_l, win_or_exp, nsim, speed, epsilon):

	nlosses = 0

	number_of_ls = 1
	number_of_longs = 1

	nrows_filled = 0

	estimates = [.5]

	old_estimate = -1

	best_move_dic = tetris.get_win_prob(nrows, .5, win_or_exp)[1]

	for i in range(nsim):

		nrows_filled_this_sim = 0

		#print("simulation #" + str(i))
		board = [0, 0, 0]

		n_pieces = 0

		while board != [nrows, nrows, nrows]:

			#print_board(board)

			obs_prob = number_of_ls / (number_of_ls + number_of_longs)

			if random.random() > prob_of_l:
				number_of_longs += 1
				piece = "I"
			else:
				number_of_ls += 1
				piece = "L"

			obs_prob = number_of_ls / (number_of_ls + number_of_longs)
			if (speed == "--fast" and max(obs_prob - old_estimate, old_estimate - obs_prob) > epsilon) or (speed == "--slow"):
				old_estimate = obs_prob
				best_move_dic = tetris.get_win_prob(nrows, obs_prob, win_or_exp)[1]

			nrows_filled_this_sim = min(board)
			board = best_move_dic[(tuple(board), piece)]

			n_pieces += 1

			if board == None:
				nlosses += 1
				nrows_filled += nrows_filled_this_sim
				break

		if board == [nrows, nrows, nrows]:
			nrows_filled += nrows

		estimates.append(obs_prob)

	# print(estimates)
	# print("final estimate of l: " + str(estimates[-1]))

	if win_or_exp == "--win":
		return(1 - nlosses/nsim)
	else:
		return(nrows_filled/nsim)

def run_many_games(ngames, nrows, prob_of_l, win_or_exp, nsim, speed, epsilon):
	s = 0
	for i in range(ngames):
		s += run_one_game(nrows, prob_of_l, win_or_exp, nsim, speed, epsilon)
	return(s/ngames)

if __name__ == "__main__":
	print(run_many_games(ngames, nrows, prob, win_or_exp, nsim, speed, epsilon))
"""
nlosses = 0

for i in range(nsim):

	number_of_ls = 1
	number_of_longs = 1

	#print("simulation #" + str(i))
	board = [0, 0, 0]

	n_pieces = 0

	while board != [nrows, nrows, nrows]:

		#print_board(board)

		if random.random() > prob:
			number_of_longs += 1
			board = best_move(tuple(board), number_of_ls / (number_of_ls + number_of_longs), "LONG", n_pieces)
		else:
			number_of_ls += 1
			board = best_move(tuple(board), number_of_ls / (number_of_ls + number_of_longs), "L", n_pieces)

		n_pieces += 1

		if board == None:
			nlosses += 1
			break

	#print("learned probability of L: " + str(number_of_ls) + " / " + str(number_of_longs))

print("observed win chance: " + str(1 - nlosses / nsim)) """