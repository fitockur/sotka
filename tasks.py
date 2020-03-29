from LiteratureTest import LiteratureTest
from pyperclip import copy

if __name__ == "__main__":
    task_numbers = input("Введи через пробел номера заданий (8, 9, 15, 16 или 17): ").split()
    literature = LiteratureTest(test_type='task', task_numbers=task_numbers)
    while True:
        print('\nЕсли хочешь завершить процес, нажми ctrl+c')
        try:
            literature.start()
            copy(literature.text_body)
            literature.reset()
        except KeyboardInterrupt:
            print('\nЗавершение работы...')
            break
        