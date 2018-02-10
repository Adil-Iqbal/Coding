import time
import signal
from math import log10, floor

timeout = 20


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

# ------------ Solution Below this Line ------------

len_dict = []


def collatz_generator(n):
    """Generates numbers in the Collatz sequence starting with N. """
    while True:
        yield n
        if n <= 1:
            break
        else:
            if n % 2 == 0:
                n = n / 2
            else:
                n = (3 * n) + 1


def get_collatz_len_of(n):
    """Returns tuple of number N and it's Collatz sequence length."""
    global len_dict
    col_num = collatz_generator(n)
    col_len = 0
    while True:
        try:
            next_num = next(col_num)
            try:
                col_len += len_dict[next_num]
                raise StopIteration
            except IndexError:
                col_len += 1
        except StopIteration:
            len_dict.append(col_len)
            return n, col_len


max_len = (0, 0)
for i in range(1000000):
    data = get_collatz_len_of(i)
    if max_len[1] < data[1]:
        max_len = data

answer = max_len[0]
elapsed = time.time() - start
print("The answer is %s." % answer)
print("Solved in %s seconds." % round_sig(elapsed))
signal.alarm(0)