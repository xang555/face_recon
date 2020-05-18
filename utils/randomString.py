from random import choice
from string import ascii_lowercase


# random string
def random_some_string(str_len=10):
    letters = ascii_lowercase
    return ''.join(choice(letters) for i in range(str_len))
