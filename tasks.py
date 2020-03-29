from LiteratureTest import LiteratureTest
from pyperclip import copy

if __name__ == "__main__":
    while True:
        try:
            hw_num = input("\nВведи порядковый номер домашнего задания (ctrl+c для выхода): ")
            task_numbers = input("Введи через пробел номера заданий (8, 9, 15, 16 или 17): ").split()
            literature = LiteratureTest(test_type='task', task_numbers=task_numbers, hw_num=hw_num)
        except KeyboardInterrupt:
            print('\nЗавершение работы...')
            break
        
        while True:
            print('\nЕсли хочешь изменить конфигурацию для проверки, нажми ctrl+c')
            try:
                literature.start()
                copy(literature.text_body)
                literature.reset()
            except KeyboardInterrupt:
                break