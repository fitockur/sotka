import re
from sys import stdin
from random import choice


class UndefinedTestType(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'UndefinedTestType, {0} '.format(self.message)
        else:
            return 'UndefinedTestType has been raised'


class IncorrectTestScore(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'IncorrectTestScore, {0} '.format(self.message)
        else:
            return 'IncorrectTestScore has been raised'


class LiteratureTest:

    def __init__(self, test_type='exam'):
        if test_type in ('exam', 'test', 'task'):
            self.test_type = test_type
        else:
            raise UndefinedTestType('Наверное такой тип задания еще не поддерживатеся!')

        self.score = 0
        self.max_score = 0
        self.text_body = ''
        self.path_to_answers = 'test_answers.txt'

    def score_test(self) -> tuple:
        left = self.parse_answers()
        print('Тест. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
        right = []
        nums = []
        pattern = re.compile(r'\d+[.\) ]')
        score, max_score = 0, 0
        for line in stdin.readlines():
            dirty_num = pattern.search(line).group()
            nums.append(dirty_num[:-1])
            elems = line.split(dirty_num)[1]
            right_ = tuple(elem.strip() for elem in re.split(r'[,;]', elems))
            max_score += len(right_)
            right.append(right_)
        text_body = 'Начнем с теста.' if self.test_type == 'exam' else 'Тест.'
        text_body += '\n'
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
        return text_body, score, max_score
    
    def parse_answers(self):
        with open(self.path_to_answers, 'r', encoding='utf-8') as f:
            answers = [tuple(ans.strip() for ans in line.split(';')) for line in f]
        return answers
                
    def score_task(self, task_number):
        task = self.TASKS[task_number]
        text_body = f'Задание {task_number}.\n'
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
        return text_body, score, max_score

    def add_comment(self, score, max_score):
        if score < max_score:
                print('Комментарий: ', end='')
                comment = input()
        else:
            comment = ''
        return comment
    
    def start(self):
        header = choice(self.GREETING) + ' ' +\
                 choice(self.EMOJI_AFTER_GREETING) + '\n'
        if self.test_type == 'exam':
            text_body, score, max_score = self.score_test()
            body = text_body


    TASKS = {
        '8': {
            'criterias': (
                '1. Соответствие ответа заданию (2 макс.):',
                '2. Привлечение текста произведения для аргументации (2 макс.):',
                '3. Логичность и соблюдение речевых норм (2 макс.):'
            ),
            'max_scores': (2, 2, 2)
        }
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

    TEXT_EXCELENT = ()
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


if __name__ == "__main__":
    literature = LiteratureTest(test_type='test')
    text_body, score, max_score = literature.score_task('8')
    print(text_body)