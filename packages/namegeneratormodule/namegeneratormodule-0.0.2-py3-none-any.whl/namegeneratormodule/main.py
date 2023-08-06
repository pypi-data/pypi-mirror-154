from random import choice
from database import get_first_name, get_last_name

class Name:
    def __init__(self):
        pass 

    def __call__(self, nationality='default'):
        return f"{get_first_name()} {get_last_name()}"


if __name__ == "__main__":
    pass