# vk-rcon-minecraft
***
# Настройка бота для `LINUX`:
## Подготовка:
Скачиваем модули для python3.10 
- `vkbottle`
- `asyncio` 
- `MCRcon`

## Стартап
1. Открываем файл settings.py.
   - Получаем Access Token вашей группы `VK`.
   - Вставляем полученный токен в строку `token`.
   - Вставляем любой префикс в строку `prefix_cmd`
   - Вводим данные от RCON
   - `rcon_pass` = Пароль rcon
   - `rcon_ip` = Айпи сервера
   - Получаем свой айди и вставляем в строку `owner_id`

2. В главной директории, запускаем `start.sh`
***

## Команды в скором будущем:
| Команда | Описание |
| --- | --- |
| `сервер ип` | Переименовывает запись name с новым значением new_ip |
| `сервер пасс` | Переименовывает запись name с новым значением new_pass |
| `перм с` | Добавляет пермишен на команду группе |
| `перм у` | Удаляет пермишен на команду группе |
| `пермс` | Показывает все группы с их пермишинс |
# НАШЛИ БАГ? [НАПИСАТЬ В ВК](https://vk.me/fixees)
