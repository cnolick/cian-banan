import os
basedir = os.path.abspath(os.path.dirname(__file__))

from sqlalchemy import create_engine
engine = create_engine('sqlite:///{}'.format(os.path.join(basedir, 'bot.db')), echo=True, connect_args={'check_same_thread':False})



#####CIAN BLOCK ####

url = ''

#####TELEGRAM BLOCK ####

token = ''
abonent = ''