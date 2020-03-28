import answer as ans
import test
import random
import emoji
import re
import pyperclip
import sys

TRUE_ANSWERS = [
    [
        ('поэма'),
        ('добролюбов'),
        ('крепостничество|крепостное право'),
        ('234'),
        ('пейзаж'),
        ('рифма'),
        ('гражданин'),
        ('олицетворение|метафора'),
        ('анафора'),
        ('аллитерация|звукопись'),
        ('234'),
        ('ямб'),
    ],
]

def test_tmp():
    header = random.choice(ans.PRIVET) + ' ' + random.choice(ans.EMOJI_AFTER_PRIVET) + '\n\n'
    res = ''
    res += header
    res += '\nНачнем с теста.\n'
    print('Тестовая часть. Вставь ответ студента в формате: \n\t1. answer1\n\t...\n\tN. answerN\n\t...')
    # lines = input().split('\n')
    lines = [tuple(elem.strip() for elem in re.split(r'[,;]', re.split(r'\d[.\)]', line)[1])) for line in sys.stdin.readlines()]
    # print(lines)
    # with open('test11.txt', 'r', encoding='utf-8') as f:
    #     lines = [(line.split('.')[1].strip(),) for line in f.read().split('\n')]
    body, score = test.score_test(TRUE_ANSWERS[0], lines)
    max_score = 12
    res += body + '\n'
    res += '\n' + test.TOTALS[1] + str(score) + ' ' + test.add_ball(score)



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
    res += '8.\n' + body1 + TOTALS[0] + str(score1) + ' ' + add_ball(score1) + '\n'
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
            answer = test_tmp()
            print(answer, '\n')
            pyperclip.copy(answer)
        except (KeyboardInterrupt, EOFError):
            print('\nЗавершение работы.')
            break
        except (UnboundLocalError, ValueError):
            print('\nТы ввела что-то не то((, будь внимательней и начни сначала!\n')
            continue