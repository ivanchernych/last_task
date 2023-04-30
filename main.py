import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
import wikipedia
import requests
from getting_coordinates import getting

wikipedia.set_lang("ru")

token = 'vk1.a.mSyBz6V_e7Yn4_t3Okw5Pg2YE5GbN1GfG_UQCdNxpGvIVKhP7cX60Oilu5POb6g1B6OixJjVrdjOkiCFmIhOzrLUx1nDjC3T8JF1iJT56cEtLwnUxlXsgjqDhR1p9Y7CT1TmO72NwcohWT0gLXCBilzbB-tWwg6artjkNyAHSF9o70VqiWdds-4I2_TcFD9mSxcjEYvxQQR-skdsAnY-tw'

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


def mes(id, m, a):
    vk_session.method('messages.send', {
        'user_id': id,
        'attachment': a,
        'message': m,
        'random_id': 0
    })


def mes2(id, m):
    vk_session.method('messages.send', {
        'user_id': id,
        'message': m,
        'random_id': 0
    })


for event in VkLongPoll(vk_session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": msg,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        print(response.url)

        tompony = getting(response)

        ad = "{0},{1}".format(tompony[0], tompony[1])

        delta = "0.009"

        map_params = {
            "ll": ad,
            "spn": ",".join([delta, delta]),
            "l": "map",
            "pt": f'{ad},pm2dgl,'
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        if response:
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)

        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages('map.png')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        mes(user_id, 'нашел:', attachment)
