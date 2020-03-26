import answer as ans
import random
import emoji
import re
import pyperclip
import sys

TRUE_ANSWERS = [
    [
        ('гоголь', 'мертвые души', 'отец чичикова'),
        ('гоголь', 'мертвые души', 'автор'),
        ('гоголь', 'мертвые души', 'автор'),
        ('островский', 'гроза', 'катерина'),
        ('островский', 'гроза', 'кулигин'),
        ('островский', 'гроза', 'катерина'),
        ('островский', 'гроза', 'дикой'),
        ('тургенев', 'отцы и дети', 'базаров'),
        ('тургенев', 'отцы и дети', '(николай петрович кирсанов)'),
        ('гончаров', 'обломов', 'обломов'),
        ('гончаров', 'обломов', 'штольц'),
        ('некрасов', 'кому на руси жить хорошо', 'странники'),
        ('толстой', 'война и мир', '(андрей|болконский)'),
        ('толстой', 'война и мир', 'марья болконская'),
        ('толстой', 'война и мир', 'автор'),
        ('некрасов', 'кому на руси жить хорошо', 'безымянный мужик'),
        ('гончаров', 'обломов', 'автор'),
        ('островский', 'гроза', 'варвара'),
        ('гоголь', 'мертвые души', 'автор'),
        ('тургенев', 'отцы и дети', 'базаров')
    ],
]

TOTALS = ('Всего: ', 'Итого: ')

def score_test(left, right):
    # import pdb; pdb.set_trace()
    score = 0
    body = ''
    for i, (keys, values) in enumerate(zip(left, right)):
        body += f'{i + 1}.'
        body_line = []
        for key, value in zip(keys, values):
            if re.search(key, value, flags=2):
                score += 1
                comment = '(+)'
            else:
                comment = f"({key.strip('()').split('|')[0].upper()})"
            body_line.append(value + ' ' + comment)
        body += ' ' + '; '.join(body_line) + '\n'
    return body, score

def add_ball(score):
    ball = 'балл'
    res = score % 10
    if res in [2, 3, 4]:
        ball += 'а'
    elif res == 1:
        if score // 10 < 2:
            ball += 'ов'
    else:
        ball += 'ов'
    return ball

def test_tmp(lvl):
    header = random.choice(ans.PRIVET) + ' ' + random.choice(ans.EMOJI_AFTER_PRIVET) + '\n\n'
    res = ''
    res += header
    if (lvl == '1'):
        lvl = int(lvl)
        print('Задание 1. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
        # lines = input().split('\n')
        lines = [tuple(elem.strip() for elem in re.split(r'[,;]', re.split(r'\d[.\)]', line)[1])) for line in sys.stdin.readlines()]
        # print(lines)
        # with open('test11.txt', 'r', encoding='utf-8') as f:
        #     lines = [(line.split('.')[1].strip(),) for line in f.read().split('\n')]
        body, score = score_test(TRUE_ANSWERS[lvl - 1], lines)
        max_score = 60
        res += body + '\n'
        res += '\n' + TOTALS[1] + str(score) + ' ' + add_ball(score)

    if (lvl == '2'):
        head1 = '\nЗадание 1\n'
        head2 = '\nЗадание 2\n'
        max_score1 = 60
        print('Задание 1. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
        lines = [tuple(elem.strip() for elem in re.split(r'[,;]', re.split(r'\d[.\)]', line)[1])) for line in sys.stdin.readlines()]
        # with open('test21.txt', 'r', encoding='utf-8') as f:
        #     lines = [(line.split('.')[1].strip(),) for line in f.read().split('\n')]
        body1, score1 = score_test(TRUE_ANSWERS[0], lines)
        

        print('Задание 2.')
        criteria = []
        comments = []
        criteria_max = [2, 2, 4, 2]
        print(f'1. Сопоставление первого выбранного произведения с предложенным текстом ({criteria_max[0]} макс.): ', end='')
        criteria.append(int(input()))
        ans.add_comment(criteria[0], criteria_max[0], comments)
        print(f'2. Сопоставление второго выбранного произведения с предложенным текстом ({criteria_max[1]} макс.): ', end='')
        criteria.append(int(input()))
        ans.add_comment(criteria[1], criteria_max[1], comments)
        print(f'3. Привлечение текста произведения для аргументации ({criteria_max[2]} макс.): ', end='')
        criteria.append(int(input()))
        ans.add_comment(criteria[2], criteria_max[2], comments)
        print(f'4. Логичность и соблюдение речевых норм ({criteria_max[3]} макс.): ', end='')
        criteria.append(int(input()))
        ans.add_comment(criteria[3], criteria_max[3], comments)
        ans.check(criteria, criteria_max)
        score2 = sum(criteria)
        max_score2 = sum(criteria_max)
        body2 = ''
        for i, (crit, crit_max, com) in enumerate(zip(criteria, 
                                                      criteria_max,
                                                      comments)):
            body2 += f'K{i + 1}({crit_max})-{crit} '
            if len(com):
                body2 += f'({com})'
            body2 += '\n'
        res += head1 + body1 + TOTALS[0] + str(score1) + ' ' + add_ball(score1) + '\n'
        res += head2 + body2 + TOTALS[0] + str(score2) + ' ' + add_ball(score2) + '\n'
        score = score1 + score2
        max_score = max_score1 + max_score2
        res += '\n' + TOTALS[1] + str(score) + ' ' + add_ball(score)
    
    emoji_mark = random.choice(ans.EMOJI_EXCELLENT) + ' ' +\
                 random.choice(ans.TEXT_EXCELENT) if score / max_score >= 0.75 else random.choice(ans.EMOJI_GOOD)
    res += emoji_mark
    return(res)

if __name__ == '__main__':
    while True:
        try:
            answer = test_tmp(input('Выбери уровень сложности (1-легкий, 2-сложный): '))
            print(answer, '\n')
            pyperclip.copy(answer)
        except (KeyboardInterrupt, EOFError):
            print('\nЗавершение работы.')
            break
        except (UnboundLocalError, ValueError):
            print('\nТы ввела что-то не то((, будь внимательней и начни сначала!\n')
            continue