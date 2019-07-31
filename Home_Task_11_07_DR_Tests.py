import unittest
import Home_Task_11_07_DR
import json
from mock import patch
import vk_api


info = []
def setUpModule():
    with open('fixtures/info.json', 'r', encoding='utf-8') as out_info:
        info.extend(json.load(out_info))
    vk_session = vk_api.VkApi(login=info[0]['login'], password=info[0]['password'], api_version='5.101', scope=info[0]['scope'])

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    global vk
    vk = vk_session.get_api()


class TestSecretaryProgram(unittest.TestCase):
    #
    @patch('Home_Task_11_07_DR.input')
    def test_define_search_criteria(self, mock_input):
        mock_input.side_effect = [info[1]['user_input_user'], info[1]['user_input_age_from'],
                                  info[1]['user_input_age_to']]

        res = Home_Task_11_07_DR.define_search_criteria(vk)
        self.assertIsInstance(res, dict) #проверяем что возвращается словарь
        self.assertIn('city', res.keys()) #проверяем что город добавлен в словарь

    @patch('Home_Task_11_07_DR.input')
    def test_search_pretender(self, mock_input):
        mock_input.side_effect = [info[1]['user_input_user'], info[1]['user_input_age_from'],
                                  info[1]['user_input_age_to']]
        info_dict = Home_Task_11_07_DR.define_search_criteria(vk)

        res = Home_Task_11_07_DR.search_pretender(vk, info_dict)
        self.assertEqual(len(res['items']), 10) #проверяем что найдено 10 претендентов


    @patch('Home_Task_11_07_DR.input')
    def test_get_top_3_avatars(self, mock_input):
        mock_input.side_effect = [info[1]['user_input_user'], info[1]['user_input_age_from'],
                                  info[1]['user_input_age_to']]
        info_dict = Home_Task_11_07_DR.define_search_criteria(vk)
        pretender_list = Home_Task_11_07_DR.search_pretender(vk, info_dict)

        res = Home_Task_11_07_DR.get_top_3_avatars(vk, pretender_list)
        print(res)
        for items in res:
            self.assertIn('photos', items.keys())  # проверяем что фото добавлены для всех найденных пользователей
            self.assertEqual(len(items['photos']), 3)  # проверяем что добавлено по 3 фото для всех найденных пользователей



