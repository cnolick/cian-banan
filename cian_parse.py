import requests
from lxml import html, etree
import config
from bs4 import BeautifulSoup
from controler import workerWithObject, workerWithRequest
import re
import telepot
import time

TOKEN = config.token  # get token from command-line

bot = telepot.Bot(TOKEN)

def send_msg(text, abonents):
    if len(str(abonents)) == 8 :
        bot.sendMessage(abonents, text)
    else:
        for i in abonents:
            bot.sendMessage(i, text)



def parsin_uri_and_insert(uri, count):
   status = workerWithRequest.check_uri(uri)
   print(status)
   if status == False:
       workerWithRequest.insert(uri)
       send_msg('Добавленна новая ссылка для отслеживания', config.abonent)
   status = workerWithRequest.check_uri(uri)
   if status.count_objects != count.split(' ')[0] or status.count_objects == None:
       send_msg('Колличество объектов изменено! Теперь в отслеживаемой ссылке {} объектов'.format(count.split(' ')[0]), config.abonent)
       workerWithRequest.update(status.id, count.split(' ')[0])
   return status.id




def parsing_object_and_insert(id, object):
    for i in object:
        if object[i] != {}:
            obj = workerWithObject.check_object(object[i]['link'])
            if obj == False:
                workerWithObject.insert_object(id,
                                               object[i]['link'],
                                               object[i]['cost'],
                                               object[i]['meter'],
                                               object[i]['floor'],
                                               None)
                send_msg('Добавлен новый обьект!!!', config.abonent)
                send_msg('Обьект: '
                         'Ссылка: {}\n'
                         'Цена: {}\n'
                         'м²: {}\n'
                         'Этаж:{}\n'.format(object[i]['link'],
                                               object[i]['cost'],
                                               object[i]['meter'],
                                               object[i]['floor'],), config.abonent)
            obj = workerWithObject.check_object(object[i]['link'])
            if workerWithObject.diff_object(object[i]['link'],
                                               object[i]['cost'],
                                               object[i]['meter'],
                                               object[i]['floor'],
                                               None) == False:
                workerWithObject.update_object(object[i]['link'],
                                               object[i]['cost'],
                                               object[i]['meter'],
                                               object[i]['floor'],
                                               object[i]['photo'],
                                               obj.id)
                send_msg('Объект изменился!', config.abonent)
                send_msg('Обьект: '
                         'Ссылка: {}\n'
                         'Цена: {}\n'
                         'м²: {}\n'
                         'Этаж:{}\n'.format(object[i]['link'],
                                            object[i]['cost'],
                                            object[i]['meter'],
                                            object[i]['floor'], ), config.abonent)



class cian_search:
    def __init__(self, url):
        self.r = requests.get(url)
        if self.r.status_code != 200:
            exit(1)
        self.tree = html.fromstring(self.r.text)
    def count_object(self):
        for elem in self.tree.xpath('//*[@id="frontend-serp"]/div/div[3]/div[1]'):
            a = etree.tostring(elem, pretty_print=True)
            a = BeautifulSoup(a, "html.parser")
            return str(a).split('>')[1][:-5]
    def objects(self):
        json = {}
        for i in range(40):
            json[i] = {}
            for elem in self.tree.xpath('//*[@id="frontend-serp"]/div/div[4]/div[{}]/div/div[2]/div[2]/a'.format(i)):
                a = etree.tostring(elem, pretty_print=True)
                a = BeautifulSoup(a, "html.parser")
                link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(a))[0]
                #print(link)
                json[i]['link'] = link

            for elem in self.tree.xpath('//*[@id="frontend-serp"]/div/div[4]/div[{}]/'
                                        'div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]'.format(i)):
                a = etree.tostring(elem, pretty_print=True)
                a = BeautifulSoup(a, "html.parser")
                cost = re.findall('>.*<', str(a))[0][1:-1]
                json[i]['cost'] = cost.split(' ')[0]

            for elem in self.tree.xpath('//*[@id="frontend-serp"]/div/div[4]/div[{}]/div/'
                                        'div[2]/div[1]/div[1]/div[1]/div[4]/div/div[1]'.format(i)):
                a = etree.tostring(elem, pretty_print=True)
                a = BeautifulSoup(a, "html.parser")
                meter = re.findall('>.*<', str(a))[0][1:-1]
                json[i]['meter'] = meter.split(' ')[0]
            #
            for elem in self.tree.xpath(
                    '//*[@id="frontend-serp"]/div/div[4]/div[{}]/div/'
                    'div[2]/div[1]/div[1]/div[1]/div[5]/div/div[1]'.format(
                            i)):
                a = etree.tostring(elem, pretty_print=True)
                a = BeautifulSoup(a, "html.parser")
                floor = re.findall('>.*<', str(a))[0][1:-1]
                json[i]['floor'] = floor.split(' ')[0]
            #
            for elem in self.tree.xpath(
                    '//*[@id="frontend-serp"]/div/div[4]/div[{}]/div/div[1]/div/div[1]/div/div/div/img'.format(
                            i)):
                a = etree.tostring(elem, pretty_print=True)
                a = BeautifulSoup(a, "html.parser")
                photoUrl = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(a))[0]
                json[i]['photo'] = photoUrl
        return json



    def page(self, id):
        for elem in self.tree.xpath('//*[@id="frontend-serp"]/div/div[6]/div/ul'):
            a = etree.tostring(elem, pretty_print=True)
            a = BeautifulSoup(a, "html.parser")
            link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(a))
            for i in link:
                init = cian_search(i)
                parsing_object_and_insert(id, init.objects())








while True:
    init = cian_search(config.url)
    id = parsin_uri_and_insert(config.url, init.count_object())
    parsing_object_and_insert(id, init.objects())
    init.page(id)
    time.sleep(1800)


