"""
Usage:

>> python3 eviltetris.py [nrows] [--win || --exp] [ --greedymin || --greedyavg || --ucb ] [breadth] [depth] [nrounds]

breadth must be multiple of ten

"""

import sys
import random
import math
import tetris
import confusedtetris

def divisions(lower_int, upper_int):
	delta = (upper_int - lower_int) / 10
	return([[lower_int + i * delta, lower_int + (i + 1) * delta] for i in range(0, 10)])

def greedy_min(nrows, win_or_exp, breadth, depth, nrounds):

	lower_limit = 0
	upper_limit = 1

	for i in range(depth):
	
		#print(lower_limit, upper_limit)

		div = divisions(lower_limit, upper_limit)
		#print(div)
		scores = {q: 1 for q in range(10)}

		if win_or_exp == "--exp":
			scores = {q : nrows for q in range(10)}

		for interval_no in range(10):
	
			for j in range(int(breadth/10)):
				prob_of_l = random.uniform(div[interval_no][0], div[interval_no][1])
				#print(prob_of_l)
				#print(prob_of_l)
				round_score = confusedtetris.run_one_game(nrows, prob_of_l, win_or_exp, nrounds, "--fast", .05)
				#print(round_score)
				scores[interval_no] = min(scores[interval_no], round_score)
	
			#print(scores)
		best = min(scores, key = scores.get)
	
		lower_limit = div[best][0]
		upper_limit = div[best][1]
	
	return((lower_limit + upper_limit) / 2)

def greedy_avg(nrows, win_or_exp, breadth, depth, nrounds):

	lower_limit = 0
	upper_limit = 1

	for i in range(depth):

		#print(lower_limit, upper_limit)

		div = divisions(lower_limit, upper_limit)
		#print(div)
		scores = {q: 1 for q in range(10)}

		if win_or_exp == "--exp":
			scores = {q : nrows for q in range(10)}

		for interval_no in range(10):
	
			for j in range(int(breadth/10)):
				prob_of_l = random.uniform(div[interval_no][0], div[interval_no][1])
				#print(prob_of_l)
				#print(prob_of_l)
				round_score = confusedtetris.run_one_game(nrows, prob_of_l, win_or_exp, nrounds, "--fast", .01)
				#print(round_score)
				scores[interval_no] += round_score
	
			#print(scores)
		best = min(scores, key = scores.get)
	
		lower_limit = div[best][0]
		upper_limit = div[best][1]
	
	return((lower_limit + upper_limit) / 2)

def value(score, win_or_exp, nrows):
	if win_or_exp == "--win":
		return(1 - score)
	return(nrows - score)

def ucb(nrows, win_or_exp, breadth, depth, nrounds):

	lower_limit = 0
	upper_limit = 1
	
	for i in range(depth):
	
		rewards = {i: 0 for i in range(10)}
		visits = {i: .01 for i in range(10)}
		div = divisions(lower_limit, upper_limit)
	
		for episode in range(1, breadth + 1):
	
			ucbs = {i: rewards[i]/visits[i] + math.sqrt(2 * math.log(episode)/ visits[i]) for i in range(10)}
			interval_no = max(ucbs, key = ucbs.get)
	
			prob_of_l = random.uniform(div[interval_no][0], div[interval_no][1])
			round_score = confusedtetris.run_one_game(nrows, prob_of_l, win_or_exp, nrounds, "--fast", .05)
	
			visits[interval_no] += 1
			rewards[interval_no] += value(round_score, win_or_exp, nrows)
	
		best = max(visits, key = visits.get)
		lower_limit = div[best][0]
		upper_limit = div[best][1]

	#print(lower_limit, upper_limit)
	
	return((lower_limit + upper_limit) / 2)

if __name__ == "__main__":

	if len(sys.argv) < 7:
		print("not enough inputs! usage is the following:")
		print(">> python3 eviltetris.py [nrows] [--greedymin || --greedyavg || --ucb ] [breadth] [depth] [nrounds] ]")
		quit()

	nrows = int(sys.argv[1])
	win_or_exp = sys.argv[2]
	strat = sys.argv[3]
	breadth, depth = int(sys.argv[4]), int(sys.argv[5])
	nrounds = int(sys.argv[6])

	if strat == "--greedymin":
	
		print("optimal value found: " + str(greedy_min(nrows, win_or_exp, breadth, depth, nrounds)))
	
	if strat == "--greedyavg":
	
		print("optimal value found: " + str(greedy_avg(nrows, win_or_exp, breadth, depth, nrounds)))
	
	if strat == "--ucb":

		print("optimal value found: " + str(ucb(nrows, win_or_exp, breadth, depth, nrounds)))
	
		



