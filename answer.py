import emoji
import random
import pyperclip

PRIVET = [
    'Привет',
    'Приветики',
    'Приветик'
]

EMOJI_AFTER_PRIVET = [
    emoji.emojize(':yellow_heart:', use_aliases=True),
    emoji.emojize(':blue_heart:', use_aliases=True),
    emoji.emojize(':purple_heart:', use_aliases=True),
    emoji.emojize(':green_heart:', use_aliases=True),
    emoji.emojize(':heartbeat:', use_aliases=True),
    emoji.emojize(':heartpulse:', use_aliases=True),
    emoji.emojize(':two_hearts:', use_aliases=True),
    emoji.emojize(':revolving_hearts:', use_aliases=True),
    emoji.emojize(':cupid:', use_aliases=True),
    emoji.emojize(':sparkling_heart:', use_aliases=True),
    emoji.emojize(':sparkles:', use_aliases=True),
    emoji.emojize(':star:', use_aliases=True),
    emoji.emojize(':star2:', use_aliases=True),
    emoji.emojize(':dizzy:', use_aliases=True),
]

EMOJI_EXCELLENT = [
    emoji.emojize(':fire:', use_aliases=True),
    emoji.emojize(':boom:', use_aliases=True),
    emoji.emojize(':heart_eyes_cat:', use_aliases=True),
    emoji.emojize(':scream_cat:', use_aliases=True),
    emoji.emojize(':heart_eyes:', use_aliases=True),
    emoji.emojize(':scream:', use_aliases=True),
]

EMOJI_GOOD = [
    emoji.emojize(':cat:', use_aliases=True),
    emoji.emojize(':hatching_chick:', use_aliases=True),
    emoji.emojize(':tulip:', use_aliases=True),
    emoji.emojize(':cherry_blossom:', use_aliases=True),
    emoji.emojize(':relieved:', use_aliases=True),
    emoji.emojize(':relaxed:', use_aliases=True),
    emoji.emojize(':white_check_mark:', use_aliases=True),
    emoji.emojize(':ribbon:', use_aliases=True),
    emoji.emojize(':hearts:', use_aliases=True),
    emoji.emojize(':mortar_board:', use_aliases=True),
]

ENTER_OR_SPACE = ['\n', ' ']

def make_answer():
    print('Введи порядковый номер домашнего задания: ', end='')
    ex_num = int(input())
    print('Выбери задание, которое хочешь оценить:\n\t1) 8',
          '\n\t2) 9\n\t3) 15\n\t4) 16\n\t5) 17\n>>> ', end='')
    task_num = int(input())
    criteria = []
    if task_num == 1 or task_num == 2:
        criteria_max = [2, 2, 2]
        print(f'1. Соответствие ответа заданию ({criteria_max[0]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'2. Привлечение текста произведения для аргументации ({criteria_max[1]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'3. Логичность и соблюдение речевых норм ({criteria_max[2]} макс.): ', end='')
        criteria.append(int(input()))
        
    elif task_num == 3 or task_num == 4:
        criteria_max = [2, 2, 4, 2]
        print(f'1. Сопоставление первого выбранного произведения с предложенным текстом ({criteria_max[0]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'2. Сопоставление второго выбранного произведения с предложенным текстом ({criteria_max[1]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'3. Привлечение текста произведения для аргументации ({criteria_max[2]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'4. Логичность и соблюдение речевых норм ({criteria_max[3]} макс.): ', end='')
        criteria.append(int(input()))
    elif task_num == 5:
        criteria_max = [3, 3, 2, 3, 3]
        print(f'1. Соответствие сочинения теме и её раскрытие ({criteria_max[0]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'2. Привлечение текста произведения для аргументации ({criteria_max[1]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'3. Опора на теоретико-литературные понятия ({criteria_max[2]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'4. Композиционная цельность и логичность ({criteria_max[3]} макс.): ', end='')
        criteria.append(int(input()))
        print(f'5. Соблюдение речевых норм ({criteria_max[3]} макс.): ', end='')
        criteria.append(int(input()))
    else:
        raise ValueError('Wrong Task Number!')

    check(criteria, criteria_max)
    k = sum(criteria)
    k_max = sum(criteria_max)
    emoji_mark = random.choice(EMOJI_EXCELLENT) if k / k_max >= 0.75 else random.choice(EMOJI_GOOD)

    header = random.choice(PRIVET) + ' ' + random.choice(EMOJI_AFTER_PRIVET) +\
             random.choice(ENTER_OR_SPACE) + f'ДЗ № {ex_num}\n'
    
    body = '\n'
    for i, (crit, crit_max) in enumerate(zip(criteria, criteria_max)):
        body += f'K{i + 1}({crit_max})-{crit}\n'
    body += '\n'
    add_ball = ''
    if sum(criteria) in [2, 3, 4]:
        add_ball = 'а'
    else:
        add_ball = 'ов'
    end_body = f"Итого: {sum(criteria)} балл{add_ball} " + emoji_mark

    return header + body + end_body


def check(score, max_score):
    for sc, sc_max in zip(score, max_score):
        if sc > sc_max:
            raise ValueError('Ты ввела балл больше максимального, будь внимательней!')


if __name__ == '__main__':
    answer = make_answer()
    print(answer)
    pyperclip.copy(answer)