from core import *
from tools.debug import debug_quest_generator


def main():

    q = Quest('Test Quest 01')
    debug_quest_generator(q, 200, 4)


if __name__ == '__main__':
    main()
