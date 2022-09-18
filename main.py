import datetime
import time

import pytz as pytz
import requests
from faker import Faker


def create_user():
    # добавление пользователя
    create_url = "http://localhost:8080/api/v0/users"
    fake = Faker()
    user = fake.user_name()
    data = {'name': user}
    d = requests.post(url=create_url, json=data)

    # дополнение данных пользователя
    update_url = "http://localhost:8080/api/v0/users/" + user
    phone_number = fake.phone_number()
    update_user = "{\"contacts\": { \"call\": \"" + phone_number + "\",\"email\": \"" + fake.email() + "\",\"slack\": \"" + user + "\",\"sms\": \"" + phone_number + "\"},\"full_name\": \"" + fake.first_name() + " " + fake.last_name() + "\",\"photo_url\": null,\"time_zone\": \"US/Pacific\",\"active\": 1}"
    d = requests.put(url=update_url, data=update_user)
    return user


# def create_team(team_name):
#     create_url = "http://localhost:8080/api/v0/teams"
#     team_data = {'name': team_name, 'scheduling_timezone': "US/Pacific", 'email': team_name + "@example.com",
#                  'slack_channel': "#" + team_name}
#     d = requests.post(url=create_url, json=team_data)
#     return None


# создание списка дежурных
def add_roster(team_name):
    create_url = "http://localhost:8080/api/v0/teams/" + team_name + "/rosters"
    roster = {'name': "on-duty"}
    d = requests.post(url=create_url, json=roster)
    return None


# добавление пользователя в список дежурных
def add_member(team_name, user):
    create_url = "http://localhost:8080/api/v0/teams/" + team_name + "/rosters/on-duty/users"
    data = {'name': user}
    d = requests.post(url=create_url, json=data)
    return None


# создания события (дежурства для каждого пользователя)
def create_event(team, user_1, user_2, set_hours, set_days):
    create_url = "http://localhost:8080/api/v0/events"
    date = datetime.datetime(2022, 9, 20) + datetime.timedelta(hours=set_hours)
    end_date = date + datetime.timedelta(days=set_days)
    # создаю сразу по 2 дежурства secondary и primary
    for i in range(12):
        date = end_date
        end_date = end_date + datetime.timedelta(days=set_days)
        event = {'start': time.mktime(date.timetuple()),
                 'end': time.mktime(end_date.timetuple()),
                 'user': user_1,
                 'team': team,
                 'role': "primary"}
        response = requests.post(url=create_url, json=event)
        event = {'start': time.mktime(date.timetuple()),
                 'end': time.mktime(end_date.timetuple()),
                 'user': user_2,
                 'team': team,
                 'role': "secondary"}
        response = requests.post(url=create_url, json=event)
        user_3 = user_1
        user_1 = user_2
        user_2 = user_3


if __name__ == '__main__':
    users = []
    # добавление 4-х пользователй
    for x in range(4):
        username = create_user()
        users.append(username)
    teams = []

    # добавление 2-x списков
    for x in range(2):
        # create_team("team" + str(x))
        teams.append("team" + str(x))
        add_roster("team" + str(x))

    i = 0
    # добавление пользователей в команды, по 2 в каждую
    for x in range(2):
        print(users[i])
        add_member(teams[x], users[i])
        i = i + 1
        print(users[i])
        add_member(teams[x], users[i])
        create_event(teams[x], users[i - 1], users[i], 8, 5)
