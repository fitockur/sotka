from LiteratureTest import LiteratureTest, IncorrectTestNum
from pyperclip import copy

if __name__ == "__main__":
    while True:
        try:
            which = input('\nВыбери уровень сложности: \n\t1) Легкий\n\t2) Сложный\n>> ')
            if which == '1':
                test_answers = 'easy_way.txt'
            elif which == '2':
                test_answers = 'hard_way.txt'
            else:
                raise IncorrectTestNum
            literature = LiteratureTest(test_type='test', test_answers=test_answers, hw_num=3)
            literature.start()
            copy(literature.text_body)
            literature.reset()
        except KeyboardInterrupt:
            print('\nЗавершение работы...')
            break
        except (IncorrectTestNum, EOFError):
            print('\nТы ввела неверный вариант задания! Попробуй еще раз!')
            continue