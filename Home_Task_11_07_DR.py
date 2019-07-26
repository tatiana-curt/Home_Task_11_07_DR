# from urllib.parse import urlencode
# from pprint import pprint
# import requests
# APP_ID = 6983474
#
# def get_TOKEN():
#     BASE_URL = 'https://oauth.vk.com/authorize'
#     auth_data = {
#         'client_id': APP_ID,
#         'display': 'page',
#         'response_type': 'token',
#         'scope': ['friends', 'groups'],
#         'v': '5.95'
#     }
#     print('Скопируйте токен по ссылке')
#     print('?'.join((BASE_URL, urlencode(auth_data))))
#
#     TOKEN = input('TOKEN = ')
#     return TOKEN
#
# TOKEN = get_TOKEN()
# # TOKEN = '613f50e5e9e0d9b250740680701913adf50302b5165a684067b1964ef5a65c80a35c25cb64ce85bc9c1ee'
#
# class User:
#     def __init__(self, token, user_id=142851850):
#         self.token = token
#         self.user_id = user_id
#
#     def get_params(self):
#         return dict(
#             access_token=self.token,
#             v='5.101',
#         )
#
#     def get_info(self):
#         params = self.get_params()
#         params['user_ids'] = self.user_id
#         params['fields'] = ['interests, bdate, sex, city, home_town, music, movies, books, games,']
#         response = requests.get('https://api.vk.com/method/users.get', params)
#         response_group = requests.get('https://api.vk.com/method/groups.get', params)
#
#         dict_info = dict(
#             age_from=2018 - int(response.json()['response'][0]['bdate'].split('.')[2]),
#             age_to=2022 - int(response.json()['response'][0]['bdate'].split('.')[2]),
#             sex=int(response.json()['response'][0]['sex']) + 1,
#             city=response.json()['response'][0]['city']['id'],
#             # interests=response.json()['response'][0]['interests'],
#             # music=response.json()['response'][0]['music'],
#             # books=response.json()['response'][0]['books'],
#             # games=response.json()['response'][0]['games'],
#             # id_group=response_group.json()['response']['items']
#
#         )
#
#         return dict_info
#
#     def get_users(self):
#         params = self.get_params()
#         dict_info = self.get_info()
#         get_users_params = {**params, **dict_info}
#         get_users_params['fields'] = ['interests, bdate, sex, city, home_town, music, movies, books, games,']
#         get_users_params['count'] = 5
#
#         pprint(get_users_params)
#
#         response = requests.get('https://api.vk.com/method/users.search', get_users_params)
#
#         return response.json()
#
#
# user = User(TOKEN)
# # pprint(user.get_profile_info())
# # pprint(user.get_info())
# pprint(user.get_users())
from pprint import pprint

import vk_api
import json


def define_search_criteria(vk):
    user_input_user = input('Введите id или имя пользователя в ВК для поиска пары: ')
    user_input_age_from = input('Введите нижнюю границу возраста для подбора пары: ')
    user_input_age_to = input('Введите верхнюю границу возраста для подбора пары: ')
    response_info = vk.users.get(user_ids=user_input_user, fields='sex,city')
    checked_info = check_user_data(vk, response_info)


    match_info = dict(
        age_from=user_input_age_from,
        age_to=user_input_age_to,
        sex=checked_info[0]['sex'],
        city=checked_info[0]['city']['id']
    )

    return match_info


def check_user_data(vk, info):

    if info[0]['sex'] == 0:
        user_input_sex = input('Введите пол пользователя, для которого подбирается пара:')
    else:
        user_input_sex = info[0]['sex']
    info[0]['sex'] = 2 if user_input_sex == 1 else 1

    if info[0].get('city', False) == False:
        user_input_country = input('Введите двухбуквенный код страны в стандарте ISO 3166-1 alpha-2, в которой проживает пользователь, для которого подбирается пара: ')
        response_country = vk.database.getCountries(need_all=0, code=user_input_country)
        user_input_city = input('Введите город проживания пользователя, для которого подбирается пара: ')
        response_city = vk.database.getCities(country_id=response_country['items'][0]['id'], q=user_input_city, count=1)
        info[0]['city'] = response_city['items'][0]

    return info


def search_pretender(vk, info):
    response_pretender = vk.users.search(
        count=10, fields='bdate,sex,city',
        age_from=info['age_from'], age_to=info['age_to'],
        sex=info['sex'], city=info['city']
    )
    return response_pretender


def get_top_3_avatars(vk, info):
    pretender_list = []
    for pretender in info['items']:
        response_photos = vk.photos.get(owner_id=pretender['id'], album_id='profile', extended=1)
        list_to_sort = response_photos['items']
        photo_list = sorted(list_to_sort, key=lambda x: x['likes']['count'], reverse=True)
        pretender = dict(id=pretender['id'], photos=[])
        for photo in photo_list[0:3]:
            pretender['photos'].append(photo['sizes'][-1]['url'])
        pretender_list.append(pretender)

    return json.dumps(pretender_list, ensure_ascii=False, indent=2)


def main():
    # user_input_login = input('Для доступа к программе введите свой логин и пароль или q для выхода.\nЛогин (или номер телефона: ')
    # user_input_password = input('Пароль: ')
    scope = 'photos,groups'
    vk_session = vk_api.VkApi(login='+79811522570', password='Qwe14051993ewQ', api_version='5.101', scope=scope)
    # vk_session = vk.api.VkApi(login=user_input_login, password=user_input_password, api_version='5.101', scope=scope)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    pretender_list = search_pretender(vk, define_search_criteria(vk))
    # pprint(pretender_list)
    # get_top_3_avatars(vk, pretender_list)
    print(get_top_3_avatars(vk, pretender_list))

if __name__ == '__main__':
    main()