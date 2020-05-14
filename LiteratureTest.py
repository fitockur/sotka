import re
from sys import stdin
from random import choice
from emoji import emojize

class UndefinedTestType(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return '{0}, {1} '.format(self.__class__.__name__, self.message)
        else:
            return '{0} has been raised'.format(self.__class__.__name__)


class UndefinedTask(UndefinedTestType):
    pass


class IncorrectTestScore(UndefinedTestType):
    pass


class IncorrectTestFormat(UndefinedTestType):
    pass


class IncorrectTestNum(UndefinedTestType):
    pass


class LiteratureTest:

    def __init__(self, test_type='exam', task_numbers=None, test_answers=None, hw_num=None):
        if test_type in ('exam', 'test', 'task'):
            self.test_type = test_type
        else:
            raise UndefinedTestType('Наверное такой тип задания еще не поддерживатеся!')

        self.task_numbers = task_numbers if task_numbers is not None else ['8', '9', '15', '16', '17']
        self.path_to_answers = test_answers if test_answers is not None else 'test_answers.txt'
        self.hw_num = hw_num if hw_num is not None else 1
        self.score = 0
        self.max_score = 0
        self.text_body = ''
        

    def score_test(self, wo_smile=True) -> tuple:
        left = self.parse_answers()
        print('\nТест. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
        right = []
        nums = []
        pattern = re.compile(r'\d+[.\) ]')
        score, max_score = 0, 0
        for line in stdin.readlines():
            try:
                dirty_num = pattern.search(line).group()
            except AttributeError:
                raise IncorrectTestFormat('Неверный формат теста!')
            
            nums.append(dirty_num[:-1])
            elems = line.split(dirty_num)[1]
            right_ = tuple(elem.strip() for elem in re.split(r'[,;]', elems))
            max_score += len(right_)
            right.append(right_)
        text_body = '\nНачнем с теста.\n' if self.test_type == 'exam' else '\nТест.\n'
        for i, (keys, values) in enumerate(zip(left, right)):
            text_body += f'{nums[i]}.'
            body_line = []
            for key, value in zip(keys, values):
                if re.search(key, value, flags=2):
                    score += 1
                    comment = '(+)'
                else:
                    comment = f"({key.strip('()').split('|')[0].upper()})"
                body_line.append(value + ' ' + comment)
            text_body += ' ' + '; '.join(body_line) + '\n'
        self.text_body += text_body
        self.text_body += self.total(score, max_score, wo_smile)
        self.score += score
        self.max_score += max_score
    
    def parse_answers(self):
        with open(self.path_to_answers, 'r', encoding='utf-8') as f:
            answers = [tuple(ans.strip() for ans in line.split(';')) for line in f]
        return answers
                
    def score_task(self, task_number, wo_smile=True):
        task = self.get_task(task_number)
        text_body = f'\nЗадание {task_number}.\n'
        print(text_body, end='')
        scores = []
        comments = []
        for i, criteria in enumerate(task['criterias']):
            print(criteria, end=' ')
            score = int(input())
            comments.append(self.add_comment(score, task['max_scores'][i]))
            if score > task['max_scores'][i] or score < 0:
                raise IncorrectTestScore('Ты ввела балл больше максимально возможного!')
            scores.append(score)
        score = sum(scores)
        max_score = sum(task['max_scores'])
        for i, (crit, crit_max, com) in enumerate(zip(scores, 
                                                      task['max_scores'],
                                                      comments
                                                      )):
            text_body += f'K{i + 1}({crit_max})-{crit} '
            if len(com):
                text_body += f'({com})'
            text_body += '\n'
        self.text_body += text_body
        self.text_body += self.total(score, max_score, wo_smile)
        self.score += score
        self.max_score += max_score

    def add_comment(self, score, max_score):
        if score < max_score:
                print('Комментарий: ', end='')
                comment = input()
        else:
            comment = ''
        return comment

    def add_bal(self, score):
        if (score % 100 > 10) and (score % 100 < 20):
            return 'баллов'
        elif score % 10 == 1:
            return 'балл'
        elif score % 10 in (2, 3, 4):
            return 'балла'
        else:
            return 'баллов'

    def total(self, score, max_score, wo_smile=True):
        if score / max_score > 0.75:
            emoji_mark = emojize(choice(self.EMOJI_EXCELLENT), use_aliases=True)
        else:
            emoji_mark = emojize(choice(self.EMOJI_GOOD), use_aliases=True)
        res = f"Итого: {score} {self.add_bal(score)} "
        if not wo_smile:
            res += emoji_mark
        return res + '\n'

    def exam_total(self):
        test_score = self.TO_TEST[self.score]
        if test_score >= 75:
            emoji_mark = emojize(choice(self.EMOJI_EXCELLENT), use_aliases=True) +\
                         ' ' + choice(self.TEXT_EXCELENT)
        else:
            emoji_mark = emojize(choice(self.EMOJI_GOOD), use_aliases=True)
        return f"\nВсего: первичных - {self.score} {self.add_bal(self.score)}, " +\
               f"вторичных - {test_score} {self.add_bal(test_score)}" + emoji_mark
    
    def get_task(self, task_number):
        if task_number in ('8', '15'):
            return self.TASKS['8']
        elif task_number in ('9', '16'):
            return self.TASKS['9']
        elif task_number == '17':
            return self.TASKS['17']
        else:
            raise UndefinedTask('Неизвестное задание!')
    
    def start(self):
        # self.text_body = choice(self.GREETING) + ' ' +\
        #                  emojize(choice(self.EMOJI_AFTER_GREETING), use_aliases=True) + '\n'
        self.text_body = '#звездочка\n'
        if self.test_type == 'exam':
            self.score_test()
            for task_number in self.task_numbers:
                self.score_task(task_number)
            self.text_body += self.exam_total()
        elif self.test_type == 'task':
            self.text_body += f'ДЗ №{self.hw_num}\n'
            for task_number in self.task_numbers:
                self.score_task(task_number, wo_smile=False)
        elif self.test_type == 'test':
            self.text_body += f'ДЗ №{self.hw_num}\n'
            self.score_test(wo_smile=False)
    
    def reset(self):
        self.score = 0
        self.max_score = 0
        self.text_body = ''

    TASKS = {
        '8': {
            'criterias': (
                '1. Соответствие ответа заданию (2 макс.):',
                '2. Привлечение текста произведения для аргументации (2 макс.):',
                '3. Логичность и соблюдение речевых норм (2 макс.):',
            ),
            'max_scores': (2, 2, 2)
        },
        '9': {
            'criterias': (
                '1. Сопоставление первого выбранного произведения с предложенным текстом (2 макс.):',
                '2. Сопоставление второго выбранного произведения с предложенным текстом (2 макс.):',
                '3. Привлечение текста произведения для аргументации (4 макс.):',
                '4. Логичность и соблюдение речевых норм (2 макс.):',
            ),
            'max_scores': (2, 2, 4, 2)
        },
        '17': {
            'criterias': (
                '1. Соответствие сочинения теме и её раскрытие (3 макс.):',
                '2. Привлечение текста произведения для аргументации (3 макс.):',
                '3. Опора на теоретико-литературные понятия (2 макс.):',
                '4. Композиционная цельность и логичность (3 макс.):',
                '5. Соблюдение речевых норм (3 макс.):',
            ),
            'max_scores': (3, 3, 2, 3, 3)
        },
    }

    GREETING = (
        'Привет',
        'Приветики',
        'Приветик'
    )

    EMOJI_AFTER_GREETING = (
        ':yellow_heart:',
        ':blue_heart:',
        ':purple_heart:',
        ':green_heart:',
        ':heartbeat:',
        ':heartpulse:',
        ':two_hearts:',
        ':revolving_hearts:',
        ':cupid:',
        ':sparkling_heart:',
        ':sparkles:',
        ':star:',
        ':star2:',
        ':dizzy:',
    )

    EMOJI_EXCELLENT = (
        ':fire:',
        ':boom:',
        ':heart_eyes_cat:',
        ':scream_cat:',
        ':heart_eyes:',
        ':scream:',
    )

    TEXT_EXCELENT = (
        'Молодец!',
        'Отличная работа!',
        'Так держать!',
        'Отличный результат!',
        'Хорошо справляешься!'
    )

    EMOJI_GOOD = (
        ':cat:',
        ':hatching_chick:',
        ':tulip:',
        ':cherry_blossom:',
        ':relieved:',
        ':relaxed:',
        ':white_check_mark:',
        ':ribbon:',
        ':hearts:',
        ':mortar_board:',
    )

    TO_TEST = {
        1: 3, 2: 5, 3: 7, 4: 9,
        5: 11, 6: 13, 7: 15, 8: 18,
        9: 20, 10: 22, 11: 24, 12: 26,
        13: 28, 14: 30, 15: 32, 16: 34,
        17: 35, 18: 36, 19: 37, 20: 38,
        21: 40, 22: 41, 23: 42, 24: 43,
        25: 44, 26: 45, 27: 47, 28: 48,
        29: 49, 30: 50, 31: 51, 32: 52,
        33: 54, 34: 55, 35: 56, 36: 57,
        37: 58, 38: 59, 39: 61, 40: 62,
        41: 63, 42: 64, 43: 65, 44: 66,
        45: 68, 46: 69, 47: 70, 48: 71,
        49: 72, 50: 73, 51: 77, 52: 80,
        53: 84, 54: 87, 55: 90, 56: 94,
        57: 97, 58: 100
    }


if __name__ == "__main__":
    literature = LiteratureTest(test_type='exam')
    literature.start()
    print(literature.text_body)