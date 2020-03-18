import answer as ans
import random
import emoji
import re
import pyperclip
import sys

TRUE_ANSWERS = [
    [
        ('эпос',),
        ('роман-эпопея',),
        ('реализм',),
        ('портрет',),
        ('213',),
        ('диалог',),
        ('деталь',),
        ('безухов',),
        ('сравнение',),
        ('413',),
        ('антитеза',),
        ('повтор',),
        ('психологизм',),
        ('деталь',),
        ('композиция',),
        ('шерер',),
        ('312',)
    ],
    [
        ('7', 'вера', 'николай', 'наташа', 'петя', 'соня'),
        ('ипполита', 'анатоля'),
        ('элен', 'элен'),
        ('наташа', 'марья', 'княжна'),
        ('андрей болконский', 'аустрелицем'),
        ('пьер безухов', 'наташ'),
        ('вера',),
        ('анатоль курагин', 'андреем'),
        ('кутузов', 'багратион'),
        ('бородинского', 'анатоль'),
        ('элен',),
        ('согласны', 'андрей'),
        ('подводы',),
        ('анатоля', 'из москвы'),
        ('пети',)
    ],
    [
        ('1869',),
        ('антитеза',),
        ('пьер',),
        ('(образок|иконку)',),
        ('багратион',),
        ('баздеев',),
        ('кутузов',),
        ('каратаев',),
        ('наполеон',),
        ('народ',)
    ]
]

TOTALS = ('Всего: ', 'Итого: ')

TRUE_SCORES = (17, 31, 10,)

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
                comment = f'({key.upper()})'
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
    header = random.choice(ans.PRIVET) + ' ' + random.choice(ans.EMOJI_AFTER_PRIVET) + '\n'
    head1 = '\nЗадание 1\n'
    head2 = '\nЗадание 2\n'
    if (lvl == '1'):
        lvl = int(lvl)
        max_score1 = TRUE_SCORES[lvl - 1]
        max_score2 = TRUE_SCORES[lvl]
        print('Задание 1. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
        # lines = input().split('\n')
        lines = [(line.strip().split('.')[1].strip(),) for line in sys.stdin.readlines()]
        # print(lines)
        # with open('test11.txt', 'r', encoding='utf-8') as f:
        #     lines = [(line.split('.')[1].strip(),) for line in f.read().split('\n')]
        body1, score1 = score_test(TRUE_ANSWERS[lvl - 1], lines)

        print('Задание 2. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
        lines = [tuple(elem.strip() for elem in re.split(r'[,;]', line.strip().split('.')[1])) for line in sys.stdin.readlines()]
        # with open('test12.txt', 'r', encoding='utf-8') as f:
        #     lines = [tuple(elem.strip() for elem in line.split('.')[1].split(';')) for line in f.read().split('\n')]
        body2, score2 = score_test(TRUE_ANSWERS[lvl], lines)

    if (lvl == '2'):
        lvl = int(lvl)
        max_score1 = TRUE_SCORES[lvl]
        print('Задание 1. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
        lines = [(line.strip().split('.')[1].strip(),) for line in sys.stdin.readlines()]
        # with open('test21.txt', 'r', encoding='utf-8') as f:
        #     lines = [(line.split('.')[1].strip(),) for line in f.read().split('\n')]
        body1, score1 = score_test(TRUE_ANSWERS[lvl], lines)

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
    res = ''
    res += header
    res += head1 + body1 + TOTALS[0] + str(score1) + ' ' + add_ball(score1) + '\n'
    res += head2 + body2 + TOTALS[0] + str(score2) + ' ' + add_ball(score2) + '\n'
    score = score1 + score2
    res += '\n' + TOTALS[1] + str(score) + ' ' + add_ball(score)
    max_score = max_score1 + max_score2
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