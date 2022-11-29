# _*_ coding:utf-8 _*_
# Project: 
# FileName: ymy.py
# UserName: 高俊佶
# ComputerUser：19305
# Day: 2021/7/8
# Time: 22:28
# IDE: PyCharm

import time
import flask
import pymysql
import calendar
from flask_cors import CORS

now = time.localtime(time.time())
mysql_user = 'root'
mysql_password = 'gjj666'
week = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
month = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
env = {r.split('=')[0]: r.split('=')[1] for r in open('settings.ini', 'r', encoding='utf-8').read().split('\n')}  # 暴漏变量到环境中
for en in env:
    globals()[en] = env[en]
mysql = pymysql.connect(user=mysql_user, password=mysql_password, host='localhost', database='zl', port=3306, charset='utf8mb4', cursorclass=pymysql.cursors.SSDictCursor)
cursor = mysql.cursor()
app = flask.Flask(import_name=__name__)
app.config.from_object(__name__)
CORS(app, origins='*', supports_credentials=True)

# date_calc = lambda _, __: list(map(int, '-'.join([(lambda _: '-'.join(map(str, _)))(_)for _ in [(lambda _: [(lambda _: int(_[0]) and _[0] or '')(_)for _ in _])(_)for _ in calendar.TextCalendar().monthdays2calendar(_, __)]]).strip('-').split('-')))
date_calc = lambda _, __: [_ for _ in calendar.TextCalendar().itermonthdays(_, __)if _]


def check_user(user, password, admin):
    cursor.execute(f'select * from person where user = "{user}"')
    res = cursor.fetchall()
    if res:
        if res[0]['admin'] != admin:
            return {'res': '此账号无对应权限！', 'code': 0}
        elif res[0]['password'] != password:
            return {'res': '密码不正确！', 'code': 0}
        else:
            n = 'user.html'
            if admin:
                n = 'admin.html'
            return {'res': '登录成功！', 'code': 1, 'next': n}
    else:
        cursor.execute('select * from person')
        if not cursor.fetchall():
            if admin:
                cursor.execute(f"insert into person (`user`, `password`, `name`, `relation`, `admin`) values ('{user}', '{password}', '一家之主', '未知', 1)")
                mysql.commit()
                return {'res': f'账号 {user} 创建成功！请进去修改相关信息。', 'code': 1, 'next': 'admin.html'}
            return {'res': '第一次使用本系统请先创建一家之主账号！', 'code': 0}
        return {'res': '账号不存在！', 'code': 0}


def get_user(user):
    if user:
        cursor.execute(f'select * from person where user="{user}"')
        res = cursor.fetchall()
        if res:
            return {'res': res[0], 'code': 1}
        else:
            return {'res': f'用户{user}不存在！', 'code': 0}
    else:
        return {'res': '参数错误！', 'code': 0}


# def make_data(date: list):
#     if len(date) == 1:
#         date = [date_calc(date[0], _ + 1) for _ in range(12)]
#     elif len(date) == 2:
#         date = date_calc(date[0], date[1])
#     elif len(date) == 3:
#         if date[2] < 7:
#             if date[1] < 2:
#                 temp = date_calc(date[0] - 1, 12)[date[2]-7:]
#             else:
#                 temp = date_calc(date[0], date[1] - 1)[date[2]-7:]
#         else:
#             temp = []
#         date = temp + date_calc(date[0], date[1])[:date[2]]
#     return date
# make_data(list(map(int, '2021-07-01'.split('-'))))


def make_data_income(date: str):
    if len(date) == 8:
        res = []
        d = []
        if int(date[6:8]) < 7:
            if int(date[4:6]) < 2:
                temp = date_calc(int(date[:4]) - 1, 12)[int(date[6:8])-7:]
                for t in temp:
                    cursor.execute(f'select * from income where date like "{int(date[:4]) - 1}12{t}%"')
                    res.extend(cursor.fetchall())
                    d.append(f'12/{t}')
            else:
                temp = date_calc(int(date[:4]), int(date[4:6]) - 1)[int(date[6:8])-7:]
                for t in temp:
                    cursor.execute(f'select * from income where date like "{int(date[:6]) - 1}{t}%"')
                    res.extend(cursor.fetchall())
                    d.append('{:0>2}/{}'.format(int(date[4:6]) - 1, t))
        temp = date_calc(int(date[:4]), int(date[4:6]))[:int(date[6:8])]
        for t in temp:
            cursor.execute('select * from income where date like "' + date[:6] + '{:0>2}'.format(t) + '%"')
            res.extend(cursor.fetchall())
            d.append('{}/{:0>2}'.format(date[4:6], t))
        res = res[-7:]
        d = d[-7:]
    else:
        cursor.execute(f'select * from income where date like "{date}%"')
        res = cursor.fetchall()
        d = month
        if len(date) == 6:
            d = date_calc(int(date[:4]), int(date[4:6]))
    return res, d


def make_data_spend(date: str):
    if len(date) == 8:
        res = []
        d = []
        if int(date[6:8]) < 7:
            if int(date[4:6]) < 2:
                temp = date_calc(int(date[:4]) - 1, 12)[int(date[6:8])-7:]
                for t in temp:
                    cursor.execute(f'select * from spend where date like "{int(date[:4]) - 1}12{t}%"')
                    res.extend(cursor.fetchall())
                    d.append(f'12/{t}')
            else:
                temp = date_calc(int(date[:4]), int(date[4:6]) - 1)[int(date[6:8])-7:]
                for t in temp:
                    cursor.execute(f'select * from spend where date like "{int(date[:6]) - 1}{t}%"')
                    res.extend(cursor.fetchall())
                    d.append('{:0>2}/{}'.format(int(date[4:6]) - 1, t))
        temp = date_calc(int(date[:4]), int(date[4:6]))[:int(date[6:8])]
        for t in temp:
            cursor.execute('select * from spend where date like "' + date[:6] + '{:0>2}'.format(t) + '%"')
            res.extend(cursor.fetchall())
            d.append('{}/{:0>2}'.format(date[4:6], t))
        d = d[-7:]
    else:
        cursor.execute(f'select * from spend where date like "{date}%"')
        res = cursor.fetchall()
        d = month
        if len(date) == 6:
            d = date_calc(int(date[:4]), int(date[4:6]))
    return res, d


def judge_calc(data: list, p: int, d: (str, int), t = ''):
    a = 0.0
    if isinstance(d, int):
        if t == 'm':
            for da in data:
                if da['person'] == p and int(str(da['date'])[4:6]) == d:
                    a += float(da['price'])
        else:
            for da in data:
                if da['person'] == p and int(str(da['date'])[6:8]) == d:
                    a += float(da['price'])
    else:
        for da in data:
            if da['person'] == p and f"{str(da['date'])[4:6]}/{str(da['date'])[6:8]}" == d:
                a += float(da['price'])
    return a


def make_data(data: list, limit: list, t: int):
    cursor.execute(f'select * from person')
    person = {_['index']: _['name'] for _ in cursor.fetchall()}
    res = {}
    for p in person:
        res[person[p]] = []
        if t == 4:
            for d in range(1, 13):
                res[person[p]].append(judge_calc(data, p, d, 'm'))
        else:
            for d in limit:
                res[person[p]].append(judge_calc(data, p, d))
    return res

def set_t_chart(data_dict):
    data = {
        'title': {
            'text': data_dict['title']
        },
        'tooltip': {
            'trigger': 'axis'
        },
        'legend': {
            'data': [_ for _ in data_dict.keys() if _ not in ['title', 'day']]
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },
        'toolbox': {
            'feature': {
                'saveAsImage': {}
            }
        },
        'xAxis': {
            'type': 'category',
            'boundaryGap': False,
            'data': data_dict['day']
        },
        'yAxis': {
            'type': 'value'
        },
        'series': [
            {
                'name': _,
                'type': 'line',
                'stack': '总量',
                'data': data_dict[_]
            }
            for _ in data_dict.keys() if _ not in ['title', 'day']
        ]
    }
    return data


def make_pie(data: list):
    res = {}
    for d in data:
        if d['type'] not in res:
            res[d['type']] = 0.0
        res[d['type']] += float(d['price'])
    return res


def set_b_chart(data_dict, n):
    data = {
        'title': {
            'text': f'个人{n}',
            'subtext': n,
            'left': 'center'
        },
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left',
        },
        'series': [
            {
                'name': n,
                'type': 'pie',
                'radius': '50%',
                'data': [
                    {'value': data_dict[_], 'name': _}
                    for _ in data_dict
                ],
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
    return data


@app.route('/login', methods=['POST'])
def login():
    user = flask.request.json.get('user', '')
    password = flask.request.json.get('password', '')
    admin = flask.request.json.get('admin', '') and 1 or 0
    r = check_user(user, password, admin)
    res = flask.make_response(flask.jsonify(r), 200)
    res.set_cookie('user', user)
    return res

@app.route('/names', methods=['GET'])
def names():
    user = flask.request.cookies.get('user', '')
    return flask.jsonify(get_user(user))

@app.route('/chart', methods=['GET'])
def chart():
    date = flask.request.args.get('time', '')
    zf = flask.request.args.get('type', '')
    if not date:
        date = '-'.join([str(now.tm_year), '{:0>2}'.format(now.tm_mon), '{:0>2}'.format(now.tm_mday)])
    if '-' not in date:
        title = f'{date}年'
    elif date.count('-') == 1:
        title = f'{date}月'
    else:
        title = f'{date}周'
    if zf:
        ddd = make_data_spend(date.replace('-', ''))
        title += '支出图'
    else:
        ddd = make_data_income(date.replace('-', ''))
        title += '收入图'
    dd = {'title': title}
    dd.update({'day': ddd[1]})
    dd.update(make_data(*ddd, len(date.replace('-', ''))))
    return flask.jsonify(set_t_chart(dd))

@app.route('/get_users', methods=['GET'])
def get_users():
    cursor.execute('select * from person')
    return flask.jsonify({'res': [[_['index'], _['name']]for _ in cursor.fetchall()], 'code': 1})

@app.route('/add', methods=['POST'])
def add():
    res = flask.request.json
    try:
        if int(res['price']) < 0:
            cursor.execute(f"insert into spend (`date`, `person`, `price`, `type`, `note`) values ('{res['date'].replace('-', '').replace(' ', '').replace(':', '')}', '{res['person']}', {res['price'].replace('-', '')}, '{res['type']}', '{res['note']}')")
        elif int(res['price']) > 0:
            cursor.execute(f"insert into income (`date`, `person`, `price`, `type`, `note`) values ('{res['date'].replace('-', '').replace(' ', '').replace(':', '')}', '{res['person']}', {res['price']}, '{res['type']}', '{res['note']}')")
        mysql.commit()
        res = flask.jsonify({'res': '添加成功！', 'code': 1})
    except:
        mysql.rollback()
        res = flask.jsonify({'res': '添加失败！请检查输入内容格式是否有误。', 'code': 0})
    return res

@app.route('/leading', methods=['POST'])
def leading():
    data = [_.replace(',', ';').replace('，', ';').replace('；', ';').split(';')for _ in flask.request.json.get('date').replace(' ', '').split('\n')]
    try:
        for d in data:
            if int(d[2]) < 0:
                cursor.execute(f"insert into spend (`date`, `person`, `price`, `type`, `note`) values ('{d[0]}', '{d[1]}', {d[2].replace('-', '')}, '{d[3]}', '{len(d) == 5 and d[4] or ''}')")
            elif int(d[2]) > 0:
                cursor.execute(f"insert into income (`date`, `person`, `price`, `type`, `note`) values ('{d[0]}', '{d[1]}', {d[2]}, '{d[3]}', '{len(d) == 5 and d[4] or ''}')")
        mysql.commit()
        return flask.jsonify({'res': '批量导入成功！', 'code': 1})
    except:
        mysql.rollback()
        return flask.jsonify({'res': '批量导入失败！请检查输入内容格式是否有误。', 'code': 0})

@app.route('/search', methods=['POST'])
def search():
    person = flask.request.json.get('person', '')
    date = flask.request.json.get('dt[date]', '') and flask.request.json.get('date', '') or 0
    hm = flask.request.json.get('dt[time]', '') and flask.request.json.get('time', '') or 0
    io = flask.request.json.get('io', '') and 1 or 0
    s = ''
    q = '支出数据'
    if hm and date:
        s = str(hm).replace(':', '')
    sql = f'select * from spend where person="{person}"'
    if io:
        q = '收入数据'
        sql = f'select * from income where person="{person}"'
    if date:
        sql += f' and date like "{str(date).replace("-", "")}{s}%"'
    cursor.execute('select * from person')
    person = {_['index']: _['name'] for _ in cursor.fetchall()}
    cursor.execute(sql)
    res = cursor.fetchall()
    si = res and [{__: _[__]for __ in _ if __ not in ['index']} for _ in res] or []
    si and [_.update({'person': person[_['person']]}) for _ in si]
    return flask.jsonify({'chart': set_b_chart(make_pie(res), q), 'table': si, 'q': q})

@app.route('/table', methods=['GET'])
def table():
    cursor.execute(f'select * from person')
    person = [{__: _[__]for __ in _ if __ not in ['index', 'password', 'admin']} for _ in cursor.fetchall()]
    return flask.jsonify(person)

@app.route('/name', methods=['POST'])
def name():
    res = flask.request.json
    res = [[_, res[_]]for _ in res][0]
    try:
        cursor.execute(f'update person set name="{res[1]}" where user="{res[0]}"')
        mysql.commit()
        return flask.jsonify({'res': f'更新用户 {res[0]} 成功！', 'code': 1})
    except:
        mysql.rollback()
        return flask.jsonify({'res': f'更新用户 {res[0]} 失败！', 'code': 0})

@app.route('/relation', methods=['POST'])
def relation():
    res = flask.request.json
    res = [[_, res[_]]for _ in res][0]
    try:
        cursor.execute(f'update person set relation="{res[1]}" where user="{res[0]}"')
        mysql.commit()
        return flask.jsonify({'res': f'更新用户 {res[0]} 成功！', 'code': 1})
    except:
        mysql.rollback()
        return flask.jsonify({'res': f'更新用户 {res[0]} 失败！', 'code': 0})

@app.route('/del_user', methods=['GET'])
def del_user():
    user = flask.request.args.get('user', '')
    if user:
        try:
            cursor.execute(f'select admin from person where user="{user}"')
            res = cursor.fetchall()
            if res:
                if res[0]['admin']:
                    return flask.jsonify({'res': f'目标用户用户 {user} 具有管理员权限，无法删除！', 'code': 0})
                cursor.execute(f'delete from person where user="{user}"')
                mysql.commit()
                return flask.jsonify({'res': f'删除用户 {user} 成功！', 'code': 1})
        except:
            mysql.rollback()
            return flask.jsonify({'res': f'删除用户 {user} 失败！', 'code': 0})
    return flask.jsonify({'res': f'用户 {user} 不存在！', 'code': 0})

@app.route('/del_date', methods=['GET'])
def del_date():
    t = flask.request.args.get('t', '')
    date = flask.request.args.get('date', '')
    person = flask.request.args.get('person', '')
    cursor.execute('select * from person')
    person_dict = {_['name']: _['index'] for _ in cursor.fetchall()}
    try:
        if t[:2] == '收入':
            cursor.execute(f'delete from income where date="{date}" and person="{person_dict[person]}"')
            mysql.commit()
            return flask.jsonify({'res': f'删除 {t} [ {date} | {person} ] 成功！', 'code': 1})
        elif t[:2] == '支出':
            cursor.execute(f'delete from spend where date="{date}" and person="{person_dict[person]}"')
            mysql.commit()
            return flask.jsonify({'res': f'删除 {t} [ {date} | {person} ] 成功！', 'code': 1})
    except:
        mysql.rollback()
        return flask.jsonify({'res': f'删除 {t} [ {date} | {person} ] 失败！', 'code': 0})

@app.route('/register', methods=['POST'])
def register():
    user = flask.request.json.get('user', '')
    password = flask.request.json.get('password', '')
    name_ = flask.request.json.get('name', '')
    relation_ = flask.request.json.get('relation', '')
    try:
        cursor.execute(f'select * from person where user="{user}"')
        res = cursor.fetchall()
        if res:
            return flask.jsonify({'res': f'用户 {user} 已存在！添加失败。', 'code': 1})
        cursor.execute(f"insert into person (`user`, `password`, `name`, `relation`, `admin`) values ('{user}', '{password}', '{name_}', '{relation_}', 0)")
        mysql.commit()
        return flask.jsonify({'res': f'添加用户 {user} 成功！', 'code': 1})
    except:
        mysql.rollback()
        return flask.jsonify({'res': f'添加用户 {user} 失败！', 'code': 0})

@app.route('/change', methods=['POST'])
def change():
    user = flask.request.cookies.get('user', '')
    name_ = flask.request.json.get('name', '')
    password = flask.request.json.get('password', '')
    relation_ = flask.request.json.get('relation', '')
    try:
        cursor.execute(f'update person set name="{name_}", password="{password}", relation="{relation_}" where user="{user}"')
        mysql.commit()
        return flask.jsonify({'res': f'修改用户 {user} 信息成功！', 'code': 1})
    except:
        mysql.rollback()
        return flask.jsonify({'res': f'修改用户 {user} 信息失败！', 'code': 0})

@app.route('/logout', methods=['GET'])
def logout():
    res = flask.jsonify({'res': '退出登录成功！'})
    res.delete_cookie('user')
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6699, threaded=True, processes=1)
    cursor.close()
    mysql.close()
