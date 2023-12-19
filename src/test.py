import jwt
import datetime
from flask import jsonify


resp1 = ('admin', 'a', 'n', 'bvt2205')
resp = [(1, 'Электротехника', '2', 1, '11:20', '12:50', 'Преподаватель', 'Кабинет', 'bvt2205'), (2, 'ИТИП', '2', 1, '13:20', '12:50', 'Преподаватель', 'Кабинет', 'bvt2205')]
js = {}
js['login'] = resp1[0]
js['name'] = f'{resp1[1]} {resp1[2]}'
js['group'] = resp1[3]
js['subject'] = []
for i in resp:
    js.get('subject').append({'id': i[0],
                              'name': i[1],
                              'date': i[2],
                              'even': i[3],
                              'time_start': i[4],
                              'time_end': i[5],
                              'teacher': i[6],
                              'classroom': i[7],
                              'group': i[8]
                              })

print(len(js['subject']))
