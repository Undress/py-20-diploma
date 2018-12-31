import requests
import json
import time


def load_config(config_file):
    with open(config_file) as file:
        config = json.load(file)

    return config


params = load_config("token.json")


def set_user_param(id):

    try:
        params['user_id'] = int(id)

    except ValueError:
        params['user_ids'] = id
        get_user_id = requests.get('https://api.vk.com/method/users.get', params).json()

        try:
            params['user_id'] = get_user_id['response'][0]['id']

        except Exception as e:
            if get_user_id['error']['error_code'] == 6:
                time.sleep(2)
                get_user_id = requests.get('https://api.vk.com/method/users.get', params).json()
                params['user_id'] = get_user_id['response'][0]['id']
            else:
                print(e)
                pass

        params.pop('user_ids')


def get_group_list(id):

    set_user_param(id)
    print(".", sep=' ', end='', flush=True)
    get_groups = requests.get('https://api.vk.com/method/groups.get', params).json()

    try:
        return get_groups['response']['items']

    except Exception:
            if get_groups['error']['error_code'] == 6:
                time.sleep(2)
                print(".", sep=' ', end='', flush=True)
                get_groups = requests.get('https://api.vk.com/method/groups.get', params).json()
                try:
                    return get_groups['response']['items']
                except Exception:
                    return []
            else:
                return []


def get_friend_list(id):

    set_user_param(id)

    get_friends = requests.get('https://api.vk.com/method/friends.get', params).json()

    return get_friends['response']['items']


def get_unique_groups(friend_list, group_list):

    not_unique_groups = set()

    for i in friend_list:

        friend_group_list = get_group_list(i)

        not_unique_groups.update(set(friend_group_list) & set(group_list))

    unique_group_list = list(set(group_list) - not_unique_groups)

    return unique_group_list


def get_group_details(group_list):

    group_detais = []

    params['fields'] = 'members_count'

    for i in group_list:
        params['group_id'] = i

        try:
            result_group = requests.get('https://api.vk.com/method/groups.getById', params).json()
            if not('deactivated' in result_group['response'][0]):
                group_detais.append(result_group['response'][0])
            else:
                pass

        except Exception as e:
            if result_group['error']['error_code'] == 6:
                time.sleep(2)
                result_group = requests.get('https://api.vk.com/method/groups.getById', params).json()
                if not ('deactivated' in result_group['response'][0]):
                    group_detais.append(result_group['response'][0])
                else:
                    pass

            else:
                print(e)
                pass

    return group_detais


def parse_to_json(group_list):

    groups_list = []

    for i in group_list:
        group_id = i['id']
        group_name = i['name']
        members_count = i['members_count']
        groups_list.append({"name": group_name, "gid": group_id, "members_count": members_count})

    with open('groups.json', 'w', encoding='utf8') as f:
        json.dump(groups_list, f, ensure_ascii=False)

    print("\nДанные успешно записаны в файл")


def main():

    user_id = input("Введите ID пользователя: ")

    group_list = get_group_list(user_id)

    friend_list = get_friend_list(user_id)

    unique_group_list = get_unique_groups(friend_list, group_list)

    final_list = get_group_details(unique_group_list)

    parse_to_json(final_list)


if __name__ == '__main__':
    main()
