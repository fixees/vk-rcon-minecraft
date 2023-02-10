from functions import set_owner, set_token, set_prefix, get_owner, get_prefix, get_token, get_replace, set_replace

import os
import time

default_commands = 'pip3.10 install vkbottle && pip3.10 install mcrcon'


def replacement():
    print('INFO | Проверка библиотек...')
    try:
        import vkbottle
        import json
        import mcrcon

        print('OK | Библиотеки в порядке')
    except Exception as e:
        print(f'ERR | Вы установили не все необходимые библиотеки. \n{e}')
        print('INFO | Автоматическое скачивание...')
        try:
            os.system(default_commands)
        except Exception as e:
            print(f'ERR | Что-то пошло не так! \nОшибка: {e}')

    print('INFO | Установка параметров...')

    token = input('Введите токен группы: ')
    set_token(token)

    owner_id = int(input('Введите айди владельца (цифрами-): '))
    set_owner(owner_id)

    if get_prefix() == ".":
        prefix = input('Хотите изменить префикс (По умолчанию префикс имеет значение "."): ')
        if prefix in ['Да', '+', 'да', 'yes', 'Yes', 'Y', 'y', 'da', 'lf', 'ДА', 'дА', '++']:
            prefix_ = input('Введите желаемый префикс: ')

            set_prefix(prefix_)

    print('INFO | Установка завершена!')
    set_replace(False)


if get_replace() is True:
    replacement()
    print('INFO | Убедитесь, что Вы в каталоге где находится файл main.py!')
    print('Загрузка...')
    time.sleep(7) # Сделано специально!!

    # os.system('screen -S BotVK python3.10 main.py')
    os.system('python3.10 main.py')
else:
    replace = input('Хотите заменить параметры?: ')

    if replace in ['Да', '+', 'да', 'yes', 'Yes', 'Y', 'y', 'da', 'lf', 'ДА', 'дА', '++']:
        replacement()
    else:
        print('INFO | Убедитесь, что Вы в каталоге где находится файл main.py!')
        print('Загрузка...')
        time.sleep(7) # Сделано специально!!

        # os.system('screen -S BotVK python3.10 main.py')
        os.system('python3.10 main.py')
