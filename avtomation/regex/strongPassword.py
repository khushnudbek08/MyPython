import re


def passwor_cheeker(password):
    is_eight = re.search(r".{8,}", password)
    is_big = re.search(r"(?=.*[A-Z])", password)
    is_small = re.search(r"(?=.*[a-z])", password)
    is_num = re.search(r"(?=.*[0-9])", password)
    if is_eight and is_big and is_small and is_num:
        print("password is strong!")
    else:
        print("password is not strong!")


password1 = input(
    "plice include at least one capital, \none lowercase and one digit. \nplace include at least 8 caracters: \n>>>"
)

passwor_cheeker(password1)
