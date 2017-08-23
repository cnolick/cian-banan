# cian-banan
SUCKS CIAN!

для того что бы это заработало надо:
создать файлик config.py
в нем добавить следующие строчки:

import os
basedir = os.path.abspath(os.path.dirname(__file__))
from sqlalchemy import create_engine
engine = create_engine('sqlite:///{}'.format(os.path.join(basedir, 'bot.db')), echo=True, connect_args={'check_same_thread':False})
Где bot.db название базы
url = '%url%' url из циана с фильтрами например:
'https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&foot_min=20&ipoteka=1&is_first_floor=0&maxprice=7500000&metro%5B0%5D=5&metro%5B10%5D=113&metro%5B11%5D=117&metro%5B12%5D=137&metro%5B13%5D=146&metro%5B14%5D=155&metro%5B1%5D=13&metro%5B2%5D=41&metro%5B3%5D=76&metro%5B4%5D=88&metro%5B5%5D=89&metro%5B6%5D=90&metro%5B7%5D=95&metro%5B8%5D=100&metro%5B9%5D=108&minfloorn=6&offer_type=flat&only_foot=2&room2=1&room3=1'
token = '%token%' токен телеграмм бота
abonent = %abonent% сюда добавляем ваш id из телеграма для отправки сообщений id можно получить у бота @userinfobot(можно добавить несколько через запятую)
profit
