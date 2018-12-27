import requests
import json
import time


token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
params = {
    'access_token': token,
    'v': '5.92'
}

group_params = {
    'access_token': token,
    'v': '5.92',
    'fields': 'members_count'
}

def get_group_list(id):
    try:
        params['user_id'] = int(id)
    except ValueError:
        params['screen_name'] = id

    get_groups = requests.get('https://api.vk.com/method/groups.get', params).json()
    print(".", sep=' ', end='', flush=True)

    return get_groups['response']['items']

def get_friend_list(id):
    try:
        params['user_id'] = int(id)
    except ValueError:
        params['screen_name'] = id

    get_friends = requests.get('https://api.vk.com/method/friends.get', params).json()
    print(".", sep=' ', end='', flush=True)

    return get_friends['response']['items']


def get_final_list(groups, friends):

    final_group_list = []


    for i in groups:

        params['group_id'] = i
        group_params['group_id'] = i

        print(".", sep=' ', end='', flush=True)

        try:
            get_members = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
            group_memebers = get_members['response']['items']

        except KeyError:
            time.sleep(3)
            get_members = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
            group_memebers = get_members['response']['items']

        if not (set(group_memebers) & set(friends)):
            print(".", sep=' ', end='', flush=True)

            try:
                result_group = requests.get('https://api.vk.com/method/groups.getById', group_params).json()
                final_group_list.append(result_group['response'][0])
            except KeyError:
                time.sleep(3)
                result_group = requests.get('https://api.vk.com/method/groups.getById', group_params).json()
                final_group_list.append(result_group['response'][0])

    return final_group_list

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

    final_list = get_final_list(group_list, friend_list)

    parse_to_json(final_list)


if __name__ == '__main__':
    main()
