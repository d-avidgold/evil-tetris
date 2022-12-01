"""
For my final project, I've written three different agents to play (and complicate) a simplified version of the game of Tetris.

The first agent, outlined in tetris.py, and used throughout all the others, uses Dynamic Programming to find the optimal move in tetris, aiming to either maximize the probability 
	of filling the board OR the total number of rows filled.

The second agent, outlined in confusedtetris.py, utilizes the first to find the optimal move, but begins without knowledge of the probability of each piece falling. It updates
	its beliefs throughout the game, and is able to carry some knowledge between different games, only resetting once a new "round" has begun.

The third agent, outlined in eviltetris.py, aims to find an optimal value of p (the probability in percentage of dropping a long block), such that the second agent has minimal
	probability of winning/expected lines filled. It does so either by considering plays of the game as a set of Multi-Armed Bandits - one for each interval of the 
	form [10x, 10x + 10] - and choosing the best machine either greedily or via the Upper Confidence Bound, then zooming in, looking at intervals of the form [x, x + 1], and 
	repeating this process.

Three examples of these scripts functionality are outlined below, each can be retrieved by calling the following:

>> python3 test_tetris [test_no] [nrows] [flags]* 									** NOTE: using odd sized boards gives unintersting outputs due to parity **


The first test will determine the probability of winning and the expected number of rows filled for all integer percentage valued p, given the number of rows of the board.

The second test will play 100 rounds of 100 games for each p in {0, 10, 20, ..., 100}, aiming to maximize wins/rows filled, given the number of rows on the board. If the --fast
	flag is specified, it will do so with the "fast" capability of the agent, choosing to only recalculate the best move dictionary once the estimate has changed far enough.

The third test will aim to find the optimal percentage value (to only two digits) by all three methods, running 1000 iterations each time. This process is 
	repeated 10 times for each strategy (assuming we're aiming to maximize wins, not rows) to see if it is consistent. Example outputs are as below:

>> python3 test_tetris 1 10
	probabilities of win:
	1.0
	0.9085363845901511
	0.8324160330492929
	...

	expected rows filled:
	10.0
	9.826228410497041
	9.681659274372127
	...

>> python3 test_tetris 2 10 --fast
	observed probabilities of win:
	1.0
	0.5608
	0.5003999999999997
	...

	observed expected rows filled:
	10.0
	9.160599999999999
	9.067299999999996
	9.0207
	...

>> python3 test_tetris 3 6 					** WARNING: takes a LONG time, increasing board size will only make it longer. **
	greedy [min] optima:
	...
	avg: 0.47800000000000004

	greedy [avg] optima:
	...
	avg: 0.5870000000000001

	ucb optima:
	...
	avg: 0.568


Some notes on the results:

	The final test gives pretty wildly varying results, especially for the greedy min test. Greedy avg and UCB is slightly more centered, and seems to agree with what was 
	found in test 2, with somewhere between 50-60 percent being ideal. I'm pretty content with this as an answer! Not what I was expecting - was really thinking that it would
	be way further off from 50%. 

	Would love to take this further in the future: def would like to know how this optimum scales with board size. Also, when I started on this project, I noticed that the
	probability of winning as the board size increases (with p set at .5) seems to converge to around .4444613 or something like that - pretty close to my lucky numbers
	so I'd love to know what this actually is.

	Other obvious modifications include: increasing width of board, adding in Markov

"""

import sys
import random
import math
import tetris
import confusedtetris
import eviltetris

nrows = int(sys.argv[2])
speed = "--slow"

if sys.argv[1] == "1":
	print("probabilities of win:")
	for p in range(0, 101):
		print(tetris.get_win_prob(nrows, p/100, "--win")[0])
	print()
	print("expected rows filled:")
	for p in range(0, 101):
		print(tetris.get_win_prob(nrows, p/100, "--exp")[0])
	print()

if sys.argv[1] == "2":
	if len(sys.argv) > 3:
		speed = sys.argv[3]
	print("observed probabilities of win:")
	for p in range(0, 11):
		print(confusedtetris.run_many_games(100, nrows, p / 10, "--win", 100, speed, .05))
	print()
	print("observed expected rows filled:")
	for p in range(0, 11):
		print(confusedtetris.run_many_games(100, nrows, p / 10, "--exp", 100, speed, .05))
	print()

if sys.argv[1] == "3":
	print("greedy [min] optima:")
	l = []
	for i in range(10):
		l.append(eviltetris.greedy_min(nrows, "--win", 1000, 2, 30))
		print(l[-1])

	print("avg: " + str(sum(l)/10))
	print()

	print("greedy [avg] optima:")
	l = []
	for i in range(10):
		l.append(eviltetris.greedy_avg(nrows, "--win", 1000, 2, 30))
		print(l[-1])

	print("avg: " + str(sum(l)/10))
	print()

	print("ucb optima:")
	l = []
	for i in range(10):
		l.append(eviltetris.ucb(nrows, "--win", 1000, 2, 30))
		print(l[-1])

	print("avg: " + str(sum(l)/10))
