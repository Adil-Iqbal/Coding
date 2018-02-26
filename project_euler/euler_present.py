import time
import signal
from math import log10, floor

timeout = 90

def handler(signum, frame):
    """Raise exception if script runs too long."""
    msg = "SCRIPT TIMED OUT!!!\n More than " + str(timeout) + " seconds have elapsed."
    raise Exception(msg)


def round_sig(x, sig=4):
    """Round to significant figures."""
    return round(x, sig-int(floor(log10(abs(x))))-1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(timeout)
start = time.time()

# ------------------------------------------ SOLUTIONS BEGINS ------------------------------------------ #

max_length = 0
best_starting_num = None

# Brute Force Solution with Array
# for num in range(1, 1000001):
# 	collatz_sequence = []
# 	while num > 1:
# 		collatz_sequence.append(num)
# 		if num % 2 == 0:
# 			num //= 2
# 		else:
# 			num = 3 * num + 1
# 	collatz_sequence.append(1)
# 	if len(collatz_sequence) > max_length:
# 		max_length = len(collatz_sequence)
# 		best_starting_num = collatz_sequence[0]

# # Brute Force Solution with Integers only.
# for num in range(1, 1000001):
# 	starting_num = int(num)
# 	collatz_length = 0
# 	while num > 1:
# 		collatz_length += 1
# 		if num % 2 == 0:
# 			num //= 2
# 		else:
# 			num = 3 * num + 1
# 	collatz_length += 1
# 	if collatz_length > max_length:
# 		max_length = collatz_length
# 		best_starting_num = starting_num

# Memoized Algorithm!
stored_lengths = [None]
for num in range(1, 1000001):
	starting_num = int(num)
	collatz_length = 0
	while num > 1:
		if len(stored_lengths)-1 >= num:
			collatz_length = collatz_length + stored_lengths[num]
			break
		else:
			collatz_length += 1
			if num % 2 == 0:
				num //= 2
			else:
				num = 3 * num + 1
	if num == 1:
		collatz_length += 1
	stored_lengths.append(collatz_length)
	if collatz_length > max_length:
		max_length = collatz_length
		best_starting_num = starting_num

elapsed = time.time() - start
print("The answer is %s." % best_starting_num)
print("Solved in %s seconds." % round_sig(elapsed))
signal.alarm(0)
