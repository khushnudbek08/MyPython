#! python3
#  here we will see logging
import logging

logging.basicConfig(
    filename="factorialLog.txt",
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname)s - %(message)s",
)


def factorial(n):
    logging.debug("Start of factorial(%s%%)" % (n))
    total = 1
    for i in range(1, n + 1):
        total *= i
        logging.debug("i is " + str(i) + ", total is " + str(total))
    logging.debug("End of factorial(%s%%)" % (n))
    return total


print(factorial(50))
logging.debug("End of programing")
