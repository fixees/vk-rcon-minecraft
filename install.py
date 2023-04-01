from functions import set_owner, set_token, set_prefix, get_owner, get_prefix, get_token, get_replace, set_replace

import os
import time

default_commands = 'pip3 install vkbottle; pip3 install mcrcon; pip3 install ttos-py'


def replacement():
    print('INFO | Проверка библиотек...')
    try:
        import vkbottle
        import mcrcon
        import TtoS

        print('OK | Библиотеки в порядке')
    except Exception as e:
        print(f'ERR | Вы установили не все необходимые библиотеки. \n{e}')
        print('INFO | Автоматическое скачивание...')
        try:
            os.system(default_commands)
            print('OK | Библиотеки в порядке')
        except Exception as e:
            print(f'ERR | Что-то пошло не так! \nОшибка: {e}')

    print('INFO | Установка параметров...')

    token = input('Введите токен группы: ')
    set_token(token)

    owner_id = int(input('Введите id владельца (Пример: 319990365): '))
    set_owner(owner_id)

    if get_prefix() == ".":
        prefix = input('Хотите изменить префикс (По умолчанию "/"): ')
        if prefix in ['Да', '+', 'да', 'yes', 'Yes', 'Y', 'y', 'da', 'lf', 'ДА', 'дА', '++']:
            prefix_ = input('Введите желаемый префикс: ')

            set_prefix(prefix_)

    print('INFO | Установка завершена!')
    set_replace(False)


if get_replace() is True:
    replacement()
    print('INFO | Убедитесь, что Вы в каталоге где находится файл main.py!')
    run_cmd = input('INFO | Введите команду, для запуска main.py : ')

    print('Загрузка...')
    time.sleep(2)

    os.system(run_cmd)
else:
    replace = input('Хотите заменить параметры?: ')

    if replace in ['Да', '+', 'да', 'yes', 'Yes', 'Y', 'y', 'da', 'lf', 'ДА', 'дА', '++']:
        replacement()
    else:
        print('INFO | Убедитесь, что Вы в каталоге где находится файл main.py!')
        run_cmd = input('INFO | Введите команду, для запуска main.py : ')

        print('Загрузка...')
        time.sleep(2)

        os.system(run_cmd)
