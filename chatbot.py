# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:27:06 2019

@author: Федор
"""

from pprint import pprint
import array
from rocketchat_API.rocketchat import RocketChat


rocket = RocketChat('atomasha', 'selena', server_url='http://rosatom-chat.ml:3000')
#pprint(rocket.me().json())
#pprint(rocket.channels_list().json())

#Со сменой имени
#pprint(rocket.chat_post_message('Ну что, пацаны, хакатон?', channel='GENERAL', alias='ZDAROV').json())

#Все то же, json делает вывод лога
#pprint(rocket.chat_post_message('тест', channel='GENERAL').json())
#pprint(rocket.channels_history('GENERAL', count=5).json())

#Без вывода лога
#rocket.chat_post_message('тест', channel='GENERAL')
pprint(rocket.im_list().json())
print("delete")
pprint(rocket.im_close('bZ4uJ45GBehdk9L7GoyJLq8BjyvnsrhsjD').json())
jsonData = rocket.im_list().json()
chatid = jsonData['ims'][0]['_id']

#for i in range(0, jsonData['ims'].length):
    

print(chatid)