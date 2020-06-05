from LiteratureTest import LiteratureTest, IncorrectTestNum
from pyperclip import copy

if __name__ == "__main__":
    while True:
        try:
            res = []
            test_answers = 'test_plus_task.txt'
            hw_num = 4
            task_numbers = ('15',)
            which = input('\nВыбери уровень сложности: \n\t1) Легкий\n\t2) Сложный\n>> ')
            if which == '1':
                res.append(LiteratureTest(test_type='test', test_answers=test_answers, hw_num=hw_num))
            elif which == '2':
                res.append(LiteratureTest(test_type='test', test_answers=test_answers, hw_num=hw_num))
                res.append(LiteratureTest(test_type='task', task_numbers=task_numbers, hw_num=hw_num))
            else:
                raise IncorrectTestNum
            buff = ''
            for i, lit in enumerate(res):
                lit.start()
                if i:
                    buff += '\n'.join(lit.text_body.split('\n')[2:])
                else:
                    buff += lit.text_body
            copy(buff)
        except KeyboardInterrupt:
            print('\nЗавершение работы...')
            break
        except (IncorrectTestNum, EOFError):
            print('\nТы ввела неверный вариант задания! Попробуй еще раз!')
            continue