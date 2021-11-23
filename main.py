from core import *
from tools import tests


def main():
    # user = User('slovomir')
    # db = DB(user)
    # db.create_base_tables()
    q_01 = Question()
    q_01.text = 'Вы очнулись в темной комнате...'
    q_01_a_01 = Answer()
    q_01_a_01.text = 'Включить свет'
    q_01_a_02 = Answer()
    q_01_a_02.text = 'Ощупать пол'
    q_01.out_ports.add(q_01_a_01)
    q_01.out_ports.add(q_01_a_02)
    q_02 = Question()
    q_02.text = 'Вас ослепил яркий свет!'
    q_02_a_01 = Answer()
    q_02_a_01.text = "Упасть в обморок"
    q_01_a_01.out_ports.add(q_02)
    q_02.out_ports.add(q_02_a_01)
    q_02_a_01.out_ports.add(q_01)
    q_03 = Question()
    q_03.text = 'Вы нащупали выключатель'
    q_03_a_01 = Answer()
    q_03_a_01.text = "Включить свет..."
    q_01_a_02.out_ports.add(q_03)
    q_03.out_ports.add(q_03_a_01)
    q_03_a_01.out_ports.add(q_02)
    q_01.is_start = True
    q_02_a_01.is_end = True

    q_01.get_tree()

    tests.test_quest_generator(100, 4)


if __name__ == '__main__':
    main()
