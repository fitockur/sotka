from LiteratureTest import LiteratureTest
from pyperclip import copy

if __name__ == "__main__":
    literature = LiteratureTest(test_type='exam')
    while True:
        try:
            literature.start()
            copy(literature.text_body)
            literature.reset()
        except KeyboardInterrupt:
            print('\nЗавершение работы...')
            break
        