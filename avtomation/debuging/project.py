#!pyhton3
# this is projec of debugging session

import random, logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s, - %(levelname)s, - %(message)s"
)
# logging.disable(logging.CRITICAL)


toss = random.randint(0, 1)  # 0 is tails, 1 is heads
logging.debug("the toss is %s" % (toss))

if toss == 1:
    toss = "heads"
else:
    toss = "tails"

guess = ""
logging.debug("value of guess %s" % (guess))
while guess not in ("heads", "tails"):
    print("Gues the coin toss! Enter heads or tails:")
    guess = input()


if toss == "heads":
    print("You got it!")
else:
    print("Nope! Guess again!")
    guess = input()
    if toss == "tails":
        print("You got it!")
    else:
        print("Nope you are realy bad at this game.")
