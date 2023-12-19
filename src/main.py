from flask import Flask, render_template, Response, request, redirect, jsonify
from flask_login import LoginManager
from flask_cors import CORS
from database import login_check, add_user, insert_token, is_token_valid, get_user_info, get_user_subjects, get_queue_list, add_in_queue, delete_from_queue, pass_in_queue
import sys
from datetime import datetime, timedelta
import jwt


app = Flask(__name__)
# читаем, откуда появилась следующая строчка, и пытаемся понять, зачем она нужна
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


app.config['JWT_SECRET_KEY'] = '_5#y2L"F4Q8zdGEWQG$%@G!gs/'


def create_token(username):
    exp = 12
    token = jwt.encode({
        'user': username,
        'exp': datetime.utcnow() + timedelta(hours=exp)
    }, app.config['JWT_SECRET_KEY'])
    return token


@app.route('/delete_from_queue', methods=['POST'])
def pass_user_in_queue():
    token = request.json.get('access_token')
    subject = request.json.get('subject')
    try:
        login = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['user']
    except:
        return {'info': 'Access token is invalid'}

    if is_token_valid(login, token):
        if pass_in_queue(login, subject):
            return jsonify({'info': 'Вы пропустили человека перед собой!'})
        else:
            return jsonify({'info': 'Человека позади вас нет'})
    return jsonify({'info': 'Token is invalid'})


@app.route('/delete_from_queue', methods=['POST'])
def delete_user_from_queue():
    token = request.json.get('access_token')
    subject = request.json.get('subject')
    try:
        login = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['user']
    except:
        return {'info': 'Access token is invalid'}

    if is_token_valid(login, token):
        if delete_from_queue(login, subject):
            return jsonify({'info': 'Вы удалены из очереди!'})
        else:
            return jsonify({'info': 'Сначала войдите в очередь, чтобы выйти из неё'})
    return jsonify({'info': 'Token is invalid'})


@app.route('/add_in_queue', methods=['POST'])
def add_user_in_queue():
    token = request.json.get('access_token')
    subject = request.json.get('subject')
    try:
        login = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['user']
    except:
        return {'info': 'Access token is invalid'}

    if is_token_valid(login, token):
        if add_in_queue(login, subject):
            return jsonify({'info': 'Вы записаны в очередь'})
        else:
            return jsonify({'info': 'Вы уже в очереди'})
    return jsonify({'info': 'Token is invalid'})


@app.route('/get_queue', methods=['POST'])
def get_queue():
    token = request.json.get('access_token')
    subject = request.json.get('subject')
    try:
        login = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['user']
    except:
        return {'info': 'Access token is invalid'}

    if is_token_valid(login, token):
        queue_list = get_queue_list(login, subject)
        return jsonify(queue_list)
    return jsonify({'info': 'Token is invalid'})


# Функция для получения информации пользователя по токену
@app.route('/render', methods=['POST'])
def render():
    # Проверка токена
    token = request.json.get('access_token')
    try:
        login = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['user']
    except:
        return {'info': 'Access token is invalid'}

    if is_token_valid(login, token):
        login = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['user']
        user_info = get_user_info(login)
        subjects = get_user_subjects(login)
        responce = {}
        responce['login'] = user_info[0]
        responce['name'] = f'{user_info[1]} {user_info[2]}'
        responce['group'] = user_info[3]
        responce['subjects'] = []
        if subjects:
            for i in subjects:
                responce.get('subjects').append({'id': i[0],
                                                'name': i[1],
                                                'date': i[2],
                                                'even': i[3],
                                                'time_start': i[4],
                                                'time_end': i[5],
                                                'teacher': i[6],
                                                'classroom': i[7],
                                                'group': i[8]
                                                })
        # print(resp, file=sys.stderr)
        return jsonify(responce)
    else:
        return {'info': 'Access token is invalid'}


# Api для проверки авторизации
@app.route('/index', methods=['POST'])
def index():
    # Проверка токена
    token = request.json.get('access_token')
    try:
        login = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['user']
    except:
        return jsonify({'info': 'Token is invalid'})
    if is_token_valid(login, token):
        return jsonify({'info': 'Token is valid'})
    return jsonify({'info': 'Token is invalid'})


@app.route('/login', methods=['POST'])
def login():
    """
    Здесь вы видите переписанный login. Что с этим советую делать дальше:
    1) Введите обработку ошибок. При неудачной авторизации лучше возвращать
    в формате ошибки, а не json. И предусмотрите все возможные ошибки, которые могут
    выскочить в процессе выполнения этого роута.
    2) Почитать про то, как дальше фронт должен отправлять данные для ручек,
    где требуется авторизация (подсказка, лезем в документацию, лучше ищите для
    построения REST API на Flask, именно здесь будет информация без render_template)
    3) redirect происходит также на фронте. Бек просто получает запрос и отправляет данные
    обратно.
    """
    log = request.json.get('login')
    password = request.json.get('password')
    response = login_check(log, password)
    if not response:
        return jsonify({'login': 'False'})
    
    # Создание JWT токена при успешной аутентификации
    token = create_token(log)
    # Запись JWT токена в бд
    insert_token(log, token)

    return jsonify({'login': 'True',
                    'access_token': token,
                    })


@app.route('/registration', methods=['POST'])
def registration():


    # Получение данных пользователя
    full_name = request.json.get('Name')
    print(full_name, file=sys.stderr)
    name = full_name.split(' ')[1]
    second_name = full_name.split(' ')[0]
    login = request.json.get('Login')
    password = request.json.get('Password')
    # Проверка на то существует ли уже пользователь с таким же логином
    # ----

    # Проверка на то все ли поля заполнены
    if not name:
        return jsonify({
            'login': 'False',
            'error': 'Name is Null'
        })
    if not second_name:
        return jsonify({
            'login': 'False',
            'error': 'Second name in Null'
        })
    if not login:
        return jsonify({
            'login': 'False',
            'error': 'Login is Null'
        })
    if not password:
        return jsonify({
            'login': 'False',
            'error': 'Password is Null'
        })

    # Далее если все условия соблюдены - запись в бд и вывод положительного ответа json
    # Запись в бд
    # ----

    add_user(login, password, name, second_name)
    # Вывод json ответа
    return jsonify({
        'login': 'True',
    })


if __name__ == "__main__":
    # Создайте файл settings и вынесите host, pord, debug и остальные подобные настройки туда
    app.run(host='127.0.0.1', port=5000, debug=True)
