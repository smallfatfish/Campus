from flask import request, jsonify
from database import db
from Entity import Account


def edit_account():
    data = request.json
    # j_username = data['j_username']
    # test = request.cookies
    # j_username = test['j_username']
    j_username = request.headers.get('Authorization')
    new_name = data['name']
    new_city = data['city']
    new_hobbies = data['hobbies']
    while new_hobbies.startswith('\n') or new_hobbies.startswith('\t'):
        new_hobbies = new_hobbies[1:]
    new_sex = data['sex']
    if data['height'] != '':
        new_height = data['height']
    if data['weight'] != '':
        new_weight = data['weight']
    new_introduction = data['introduction']
    new_number = data['number']
    new_personality = data['personality']
    if data['age'] != '':
        new_et = data['age']
    new_major = data['major']

    try:
        # 根据学号查询学生对象
        account = Account.query.get(j_username)
        if account:
            # 更新学生信息
            account.name = new_name
            account.city = new_city
            account.hobbies = new_hobbies
            account.sex = new_sex
            if data['height'] != '':
                account.height = new_height
            if data['weight'] != '':
                account.weight = new_weight
            account.introduction = new_introduction
            account.number = new_number
            account.personality = new_personality
            if data['age']:
                account.age = new_et
            account.major = new_major
            db.session.commit()

            response = {'status': 'success', 'message': 'Account information updated.'}
        else:
            response = {'status': 'error', 'message': 'Account not found.'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers['Access-Control-Allow-Origin'] = '*'
    return jsonify(response)


def edit_labels():
    data = request.json
    j_username = request.headers.get('Authorization')
    new_labels = data['labels']
    try:
        # 根据学号查询学生对象
        account = Account.query.get(j_username)
        if account:
            # 更新学生信息
            account.labels = new_labels
            db.session.commit()
            response = {'status': 'success', 'message': 'labels updated.'}
        else:
            response = {'status': 'error', 'message': 'Account not found.'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    return jsonify(response)