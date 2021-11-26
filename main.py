from core import *
from tools import tests


def main():
    # user = User('')
    # db = DB(user)
    # db.create_base_tables()

    n = Network()
    tests.test_quest_generator(n, 200, 4)


if __name__ == '__main__':
    main()
