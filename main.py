from core import *
from tools import tests


def main():
    # user = User('')
    # db = DB(user)
    # db.create_base_tables()

    q = Quest('Test Quest 01')
    tests.test_quest_generator(q, 200, 4)


if __name__ == '__main__':
    main()
