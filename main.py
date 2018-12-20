import requests

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
params = {
    'access_token': token,
    'v': '5.92',
}

params['screen_name'] = "eshmargunov"

get_groups = requests.get('https://api.vk.com/method/groups.get', params).json()

get_friends = requests.get('https://api.vk.com/method/friends.get', params).json()

group_list = get_groups['response']['items']

friend_list = get_friends['response']['items']

for i in group_list:
    params['group_id'] = i
    get_members = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
    group_memebers = get_members['response']['items']

    if not(set(group_memebers) & set(friend_list)):
        print(requests.get('https://api.vk.com/method/groups.getById', params).json())
