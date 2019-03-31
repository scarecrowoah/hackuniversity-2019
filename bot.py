import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

def main():
    session = requests.Session()
    data = pd.read_excel('user_data.xlsx', header=0)
    print(data)
    uid = np.squeeze(data[['ID']].values)
    names = np.squeeze(data[['Имя']].values)
    vorname = data[['Фамилия']]
    fathername = data[['Отчество']]
    bday = data[['Дата рождения']]
    isreg = data[['ISREG']]
    vid = np.squeeze(data[['UID']].values)
    # Авторизация пользователя:
    """
    login, password = 'python@vk.com', 'mypassword'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """

    # Авторизация группы (для групп рекомендуется использовать VkBotLongPoll):
    # при передаче token вызывать vk_session.auth не нужно

    vk_session = vk_api.VkApi(token='adab1fa6eddbb4fcb0b897ef8372cb95c042700616fcb7b3bc615e352c5df8910138e9d4bd63e05386a7e')
    for i in range(0, len(vid)):
        vid[i] = 0
    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    isFound = False
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
            print(isFound)
            for i in range(0, len(vid)):
                if(int(event.user_id - vid[i]) == 0):
                    print("Found")
                    isFound = True
                    text = "Здравствуйте, " + names[i]
                    vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=text
                    )
                    break
                    
            
            data = event.text.split(" ", 1)
            com = data[0]
            print(data)
            if(com == "!id"):
                print("Регистрация...")
                s = event.text
                l = len(s)
                integ = []
                i = 0
                while i < l:
                    s_int = ''
                    a = s[i]
                    while '0' <= a <= '9':
                        s_int += a
                        i += 1
                        if i < l:
                            a = s[i]
                        else:
                            break
                    i += 1
                    if s_int != '':
                        integ.append(int(s_int))
                 
                idd = integ;
                for i in range(0, len(uid)):
                    if(idd == uid[i]):
                        vid[i] = str(event.user_id)
                        print(int(event.user_id - vid[i]))
                        #print(vid)
                        print("User is registered")
                        isFound = True
                        text = " "
                        for i in range(0, len(vid)):
                            if(int(event.user_id - vid[i]) == 0):
                                print("Found")
                                isFound = True
                                text = "Здравствуйте, " + names[i]
                                vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message=text
                                )
                                break
                        break
            
            if(com == "!next"):
                (x,y) = getVector(generate())
                text = str(getNext(x))
                draw(y)
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=text
                    )
            if(com == "!comp"):
                login, password = '89994456233', 'fedor12345'
                vk_session = vk_api.VkApi(login, password)

                try:
                    vk_session.auth(token_only=True)
                except vk_api.AuthError as error_msg:
                    print(error_msg)
                    return
                userid = event.user_id
                """ В VkUpload реализованы методы загрузки файлов в ВК
                """
            
                upload = vk_api.VkUpload(vk_session)
            
                photo = upload.photo(  # Подставьте свои данные
                    'pie.png',
                    album_id=261375384,
                    group_id=179758165
                )
            
                vk_photo_url = 'https://vk.com/photo{}_{}'.format(
                    photo[0]['owner_id'], photo[0]['id']
                )
                vk_session = vk_api.VkApi(token='adab1fa6eddbb4fcb0b897ef8372cb95c042700616fcb7b3bc615e352c5df8910138e9d4bd63e05386a7e')
                vk = vk_session.get_api()
            
                upload = VkUpload(vk_session)  # Для загрузки изображений
                longpoll = VkLongPoll(vk_session)
                vk.messages.send(
                    user_id=userid,
                    random_id=get_random_id(),
                    message="Диаграмма ваших интересов"
                    )
                vk.messages.send(
                    user_id=userid,
                    random_id=get_random_id(),
                    message=vk_photo_url
                    )           
            print('ok')
            

def getVector(vector):
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    ans = loaded_model.predict(vector)
    return ((np.where(ans>0.5, 1,0)), ans)



def getNext(vector):
    future_lectures = pd.read_excel('будущие лекции.xlsx')
    tmp = future_lectures[['Направление']].values
    print(vector[0][tmp[2][0]])
    for i in range(tmp.size):
        if (vector[0][tmp[i][0]]==1):
            return(future_lectures.loc[[i]])
            break
        
        
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def draw(data_values):
    data_names = [ 'Социальные проекты', 'Молодые профессионалы', 'Лидерские проекты',
                  'Национальная Технологическая Инициатива', 'Инфраструктурные проекты', 'Цифровая экономика', 'Направление «Развитие регионов»',
                  'Направление "Новый бизнес"', 'Департамент по коммуникациям','Корпоративный департамент','Административный департамент']
    
    
    dpi = 100
    fig = plt.figure(dpi = dpi, figsize = (1280 / dpi, 720 / dpi) )
    mpl.rcParams.update({'font.size': 10})
    
    plt.title('Предполагаемое распределение ваших интересов')
    
    xs = range(len(data_names))
    
    plt.pie( 
        np.squeeze(data_values), autopct='%.1f', radius = 1.1,
        explode = [0.15] + [0 for _ in range(len(data_names) )])
    plt.legend(
        bbox_to_anchor = (-0.6, 0.50, 0.25, 0.25),
        loc = 'lower left', labels = data_names )
    fig.savefig('pie.png')
    

def generate():
    return np.array([[np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      np.random.randint(0, 11), 
                      ]])

if __name__ == '__main__':
    main()