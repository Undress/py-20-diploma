import requests
import json
import time



def load_config(config_file):
    with open(config_file) as file:
        config = json.load(file)

    return config


params = load_config("token.json")


def get_group_list(id):

    try:
        params['user_id'] = int(id)
    except ValueError:
        params['user_ids'] = id
        get_user_id = requests.get('https://api.vk.com/method/users.get', params).json()
        params['user_id'] = get_user_id['response'][0]['id']
        params.pop('user_ids')

    get_groups = requests.get('https://api.vk.com/method/groups.get', params).json()
    print(".", sep=' ', end='', flush=True)

    return get_groups['response']['items']

def get_friend_list(id):

    try:
        params['user_id'] = int(id)
    except ValueError:
        params['user_ids'] = id
        get_user_id = requests.get('https://api.vk.com/method/users.get', params).json()
        params['user_id'] = get_user_id['response'][0]['id']
        params.pop('user_ids')

    get_friends = requests.get('https://api.vk.com/method/friends.get', params).json()
    print(".", sep=' ', end='', flush=True)

    return get_friends['response']['items']


def get_group_memebers(groups):

    group_member_list = []

    for i in groups:
        params['group_id'] = i

        print(".", sep=' ', end='', flush=True)
        get_members = requests.get('https://api.vk.com/method/groups.getMembers', params).json()

        try:
            group_member_list.append({'id': i, 'member_list': get_members['response']['items']})

        except Exception as e:
            if get_members['error']['error_code'] == 6:
                time.sleep(2)
                print(".", sep=' ', end='', flush=True)
                get_members = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
                group_member_list.append({'id': i, 'member_list': get_members['response']['items']})

            elif get_members['error']['error_code'] == 15:
                print("\nДоступ к группе: " + str(i) + " закрыт")
                pass

            else:
                print(e)
                pass



    return group_member_list


def get_unique_groups(group_members, friends):

    unique_groups = []

    for i in group_members:

        if not (set(i['member_list']) & set(friends)):
             unique_groups.append(i['id'])

    return unique_groups


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



# def get_final_list(groups, friends):
#
#     final_group_list = []
#
#
#     for i in groups:
#
#         params['group_id'] = i
#         group_params['group_id'] = i
#
#         print(".", sep=' ', end='', flush=True)
#
#
#
#
#         try:
#             get_members = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
#             group_memebers = get_members['response']['items']
#
#         except KeyError:
#             print(get_members)
#             try:
#                 get_members = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
#                 group_memebers = get_members['response']['items']
#             except KeyError:
#                 print(get_members)
#                 print("\nДоступ в группу id: " + get_members['error']['request_params'][4]['value'] + " закрыт.")
#                 pass
#
#         if not (set(group_memebers) & set(friends)):
#             print(".", sep=' ', end='', flush=True)
#
#             try:
#                 result_group = requests.get('https://api.vk.com/method/groups.getById', group_params).json()
#                 if not('deactivated' in result_group['response'][0]):
#                     final_group_list.append(result_group['response'][0])
#                 else:
#                     pass
#
#             except KeyError:
#                 time.sleep(3)
#                 result_group = requests.get('https://api.vk.com/method/groups.getById', group_params).json()
#                 if not('deactivated' in result_group['response'][0]):
#                     final_group_list.append(result_group['response'][0])
#                 else:
#                     pass
#
#     return final_group_list


def parse_to_json(group_list):

    groups_list = []

    for i in group_list:
        group_id = i['id']
        group_name = i['name']
        members_count = i['members_count']
        groups_list.append({"name" : group_name, "gid" : group_id, "members_count" : members_count})

    with open('groups.json', 'w', encoding='utf8') as f:
        json.dump(groups_list, f, ensure_ascii=False)

    print("\nДанные успешно записаны в файл")


def main():


    user_id = input("Введите ID пользователя: ")

    group_list = get_group_list(user_id)

    friend_list = get_friend_list(user_id)

    group_members = get_group_memebers(group_list)

    unique_group_list = get_unique_groups(group_members, friend_list)

    final_list = get_group_details(unique_group_list)

    parse_to_json(final_list)


if __name__ == '__main__':
    main()
