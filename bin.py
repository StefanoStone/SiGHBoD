from dotenv import load_dotenv
from github import Github
import requests
import time
import csv
import logging
import re

def check_quota(token):
    g = Github(token)
    quota = g.get_rate_limit().core

    return quota

def guarded_api_call(token, url):
    if check_quota(token).remaining == 0:
        time.sleep(check_quota(token).reset.timestamp() - time.time())

    headers = {
        'Authorization': f'token {token}'
    }

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 403:
           guarded_api_call(token, url)
        elif e.response.status_code == 404:
            return {}
        else:
            logging.debug(f"Error: {e}")
            raise e
        
    data = response.json()

    return data

def get_users(file_path, token):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            users.append((row[0], row[1], None))

    for user in users:
        full_name = user[0]
        email = user[1]
        data = guarded_api_call(token, f"https://api.github.com/search/users?q={email}")

        if 'items' in data and len(data['items']) > 0:
            new_user = list(user)
            new_user[2] = data['items'][0]['login']
            users[users.index(user)] = new_user
        else: 
            data = guarded_api_call(token, f"https://api.github.com/search/users?q={full_name}")

            if 'items' in data and len(data['items']) > 0:
                new_user = list(user)
                new_user[2] = data['items'][0]['login']
                users[users.index(user)] = new_user


    # expected output: [('Name', 'Email', 'Username')]
    return users

def detect_if_bot(user):
    bot_regex = '([\W0-9_]bot$|^bot[\W0-9_]|[\W0-9_]bot[\W0-9_])'
    test_regex = '([\W0-9_]test$|^test[\W0-9_]|[\W0-9_]test[\W0-9_])'
    auto_regex = '([\W0-9_]auto$|^auto[\W0-9_]|[\W0-9_]auto[\W0-9_])'
    regex = f"({bot_regex}|{test_regex}|{auto_regex})"
    email_prefix = user[1].split('@')[0]
    results = []
    results.append(re.search(regex, user[0], re.IGNORECASE))
    results.append(re.search(regex, email_prefix, re.IGNORECASE))
    if user[2] is not None:
        results.append(re.search(regex, user[2], re.IGNORECASE))

    return any(results)

def bin(token, file_path):
    users = get_users(file_path, token)
    for user in users:
        is_bot = detect_if_bot(user)
        users[users.index(user)] += (is_bot,)
    
    with open('output.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(users)

    return users
