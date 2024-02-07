import requests
import time
import csv
import re

def get_users(file_path, token):
    users = []
    emails = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            users.append((row[0], row[1], None))
            emails.append(row[1])

    # TODO handle github api request limit with a catch 
    for email in emails:
        url = f"https://api.github.com/search/users?q={email}"
        headers = {
            'Authorization': f'token {token}'
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            login = data['items'][0]['login']
            users[emails.index(email)] += (login,)

        # Introduce a delay of 0.72 seconds between each request to avoid rate limiting
        # time.sleep(0.72)

    # expected output: [('Name', 'Email', 'Username')]
    return users

def detect_if_bot(user):
    regex = '([\W0-9_]bot$|^bot[\W0-9_]|[\W0-9_]bot[\W0-9_])'
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
