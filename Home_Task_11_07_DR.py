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

    if 'city' not in info[0]: # Исправлено (пункт 4 доработки)
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

    return pretender_list
    # return json.dumps(pretender_list, ensure_ascii=False, indent=2)


def write_to_bd():
    import Write_to_BD
    import sqlalchemy.exc

    Write_to_BD.create_all()

    try:
        Write_to_BD.add_persons()
    except sqlalchemy.exc.IntegrityError as e:
        print('Данные уже записны')
        drop = input('Для удалния данных введите команду "d": ')
        if drop == 'd':
            Write_to_BD.drop_all()
            print('Данные удалены. Перезапустите программу')
        else:
            return 'Перезапустите программу'


def main():
    user_input_login = input('Для доступа к программе введите свой логин и пароль.\nЛогин (или номер телефона): ')
    user_input_password = input('Пароль: ')
    scope = 'photos,groups'
    vk_session = vk_api.VkApi(login=user_input_login, password=user_input_password, api_version='5.101', scope=scope)
    # vk_session = vk_api.VkApi(login='', password='', api_version='5.101', scope='photos,groups')

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    pretender_list = search_pretender(vk, define_search_criteria(vk))

    with open('Top_10_person.json', 'w', encoding='utf-8') as file:
        json.dump(get_top_3_avatars(vk, pretender_list), file, ensure_ascii=False, indent=2) # Записываем результат в Json (пункт 5 доработки)

    write_to_bd() # Записываем результат в БД


if __name__ == '__main__':
    main()
