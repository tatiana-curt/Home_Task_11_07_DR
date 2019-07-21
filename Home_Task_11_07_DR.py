from urllib.parse import urlencode
from pprint import pprint
import requests
APP_ID = 6983474

def get_TOKEN():
    BASE_URL = 'https://oauth.vk.com/authorize'
    auth_data = {
        'client_id': APP_ID,
        'display': 'page',
        'response_type': 'token',
        'scope': ['friends', 'groups'],
        'v': '5.95'
    }
    print('Скопируйте токен по ссылке')
    print('?'.join((BASE_URL, urlencode(auth_data))))

    TOKEN = input('TOKEN = ')
    return TOKEN

TOKEN = get_TOKEN()
# TOKEN = '613f50e5e9e0d9b250740680701913adf50302b5165a684067b1964ef5a65c80a35c25cb64ce85bc9c1ee'

class User:
    def __init__(self, token, user_id=142851850):
        self.token = token
        self.user_id = user_id

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.101',
        )

    def get_info(self):
        params = self.get_params()
        params['user_ids'] = self.user_id
        params['fields'] = ['interests, bdate, sex, city, home_town, music, movies, books, games,']
        response = requests.get('https://api.vk.com/method/users.get', params)
        response_group = requests.get('https://api.vk.com/method/groups.get', params)

        dict_info = dict(
            age_from=2018 - int(response.json()['response'][0]['bdate'].split('.')[2]),
            age_to=2022 - int(response.json()['response'][0]['bdate'].split('.')[2]),
            sex=int(response.json()['response'][0]['sex']) + 1,
            city=response.json()['response'][0]['city']['id'],
            # interests=response.json()['response'][0]['interests'],
            # music=response.json()['response'][0]['music'],
            # books=response.json()['response'][0]['books'],
            # games=response.json()['response'][0]['games'],
            # id_group=response_group.json()['response']['items']

        )

        return dict_info

    def get_users(self):
        params = self.get_params()
        dict_info = self.get_info()
        get_users_params = {**params, **dict_info}
        get_users_params['fields'] = ['interests, bdate, sex, city, home_town, music, movies, books, games,']
        get_users_params['count'] = 5

        pprint(get_users_params)

        response = requests.get('https://api.vk.com/method/users.search', get_users_params)

        return response.json()


user = User(TOKEN)
# pprint(user.get_profile_info())
# pprint(user.get_info())
pprint(user.get_users())