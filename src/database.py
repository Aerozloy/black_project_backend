import sqlite3
from datetime import datetime


con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()


def pass_in_queue(login, subject):
    try:
        cur.execute(f'SELECT group_name, ID FROM Users WHERE login = "{login}"')
        records = cur.fetchall()[0]
        group = records[0]
        user_id1 = records[1]

        cur.execute(f'SELECT ID FROM Subjects WHERE group_name = "{group}" and subject = "{subject}" ')
        subject_id = cur.fetchall()[0][0]

        cur.execute(f'SELECT queue_id FROM queue WHERE user_id = "{user_id1}" and subject_id = "{subject_id}" ')
        queue_id1 = cur.fetchall()[0][0]

        cur.execute(f'SELECT queue_id FROM queue WHERE user_id = "{user_id1}" and subject_id = "{subject_id}" ')
        queue_id1 = cur.fetchall()[0][0]

        queue_id2 = queue_id1 + 1

        cur.execute(
            f'UPDATE queue SET queue_id = 0 WHERE user_id = "{user_id1}" and subject_id = "{subject_id}" and group_name = "{group}" ')
        cur.execute(
            f'UPDATE queue SET queue_id = "{queue_id1}" WHERE queue_id = "{queue_id2}" and subject_id = "{subject_id}" and group_name = "{group}" ')
        cur.execute(
            f'UPDATE queue SET queue_id = "{queue_id2}" WHERE user_id = "{user_id1}" and subject_id = "{subject_id}" and group_name = "{group}" ')

        con.commit()
        return True
    except:
        return False


def delete_from_queue(login, subject):
    cur.execute(f'SELECT group_name, ID FROM Users WHERE login = "{login}"')
    records = cur.fetchall()[0]
    group = records[0]
    user_id = records[1]
    cur.execute(f'SELECT ID FROM Subjects WHERE group_name = "{group}" and subject = "{subject}" ')
    subject_id = cur.fetchall()[0][0]

    cur.execute(f'SELECT * from queue WHERE group_name = "{group}" and user_id = "{user_id}" and subject_id = "{subject_id}"')
    check = cur.fetchall()
    if not check:
        return False
    else:
        cur.execute(f'DELETE FROM queue WHERE group_name = "{group}" and user_id = "{user_id}" and subject_id = "{subject_id}"')
        con.commit()
        return True


def add_in_queue(login, subject):
    cur.execute(f'SELECT group_name, ID FROM Users WHERE login = "{login}"')
    records = cur.fetchall()[0]
    group = records[0]
    user_id = records[1]
    cur.execute(f'SELECT ID FROM Subjects WHERE group_name = "{group}" and subject = "{subject}" ')
    subject_id = cur.fetchall()[0][0]
    date = get_current_time()

    cur.execute(f'SELECT * from queue WHERE group_name = "{group}" and user_id = "{user_id}" and subject_id = "{subject_id}"')
    check = cur.fetchall()
    if not check:
        cur.execute(f'INSERT into queue(user_id, subject_id, queue_time, group_name) VALUES ("{user_id}", "{subject_id}", "{date}", "{group}")')
        con.commit()
        return True
    else:
        return False


def get_queue_list(login, subject):
    cur.execute(f'SELECT group_name, ID FROM Users WHERE login = "{login}"')
    records = cur.fetchall()[0]
    group = records[0]
    user_id = records[1]
    cur.execute(f'SELECT ID FROM Subjects WHERE group_name = "{group}" and subject = "{subject}" ')
    subject_id = cur.fetchall()[0][0]

    cur.execute(f'SELECT user_id FROM queue WHERE group_name = "{group}" and subject_id = "{subject_id}"')
    queue_user = cur.fetchall()
    queue_list = []
    for i in range(4):
        try:
            cur.execute(f'SELECT first_name, second_name FROM Users WHERE ID = "{queue_user[i][0]}"')
            recs = cur.fetchall()
            user = f'{recs[0][0]} {recs[0][1]}'
        except:
            user = 'Пусто'
        queue_list.append(user)
    return queue_list


def get_user_info(login):
    cur.execute(f"SELECT login, first_name, second_name, group_name FROM Users WHERE login = '{login}'")
    records = cur.fetchall()[0]
    return records


def get_user_subjects(login):
    cur.execute(f'SELECT group_name FROM Users WHERE login = "{login}"')
    group = cur.fetchall()[0][0]
    cur.execute(f'SELECT * FROM Subjects WHERE group_name = "{group}"')
    return cur.fetchall()


def is_token_valid(login, token):
    cur.execute(f"SELECT access_token FROM Users WHERE login = '{login}'")
    if token == cur.fetchall()[0][0]:
        return True
    else:
        return False


def insert_token(login, token):
    cur.execute(f"UPDATE Users SET access_token = '{token}' WHERE login = '{login}'")
    con.commit()


def login_check(login, password):
    cur.execute(f"SELECT * FROM Users WHERE login = '{login}' and password = '{password}'")
    try:
        records = list(cur.fetchall())[0]
    except:
        return False
    if not records:
        return False
    return True


def add_user(login, password, name, second_name):
    group = 'bvt2205'
    cur.execute(f"INSERT INTO Users(login, password, first_name, second_name, group_name) VALUES('{login}', '{password}', '{name}', '{second_name}', '{group}')")
    con.commit()


def get_current_time():
    # Получение текущего времени
    now = datetime.now()
    # Форматирование времени в формат "часы:минуты:секунды"
    return now.strftime("%H:%M:%S")


def week_even():
    current_date = datetime.now()
    week_number = current_date.isocalendar()[1]
    if week_number % 2 == 0:
        return True
    return False

