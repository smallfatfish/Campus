from flask import request, jsonify
from sqlalchemy import text
from sqlalchemy.orm import class_mapper

from database import db
from Entity import Account, Hobby


def get_message():
    # j_username = request.json['j_username']  # 前端发送的查询的j_username
    # test = request.cookies
    # j_username = test['j_username']
    # print(test)
    j_username = request.headers.get('Authorization')
    try:
        account_data = Account.query.filter_by(j_username=j_username).all()  # 返回的是一个列表
        # print(type(account_data))
        # print(account_data)
        account_data = [serialize_account(account) for account in account_data]
        # print(type(account_data))
        # print(account_data)
        response = {'status': 'success', 'accounts': account_data}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def get_other_user_message():
    j_username = request.json['j_username']  # 前端发送的查询的j_username
    try:
        account_data = Account.query.filter_by(j_username=j_username).all()  # 返回的是一个列表
        account_data = [serialize_account(account) for account in account_data]
        # print(type(account_data))
        # print(account_data)
        response = {'status': 'success', 'accounts': account_data}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def serialize_account(account):
    columns = [column.key for column in class_mapper(Account).columns]
    return {column: getattr(account, column) for column in columns}


# 这个函数serialize_account(account)的作用是将Account类的对象序列化为字典形式。
# 在函数内部，我们使用class_mapper(Account)来获取Account类的映射器对象，通过映射器对象可以获取到该类的所有列信息。
# 然后，我们通过遍历列信息，使用getattr(account, column)来获取account对象中对应列的属性值，并将列名和属性值作为键值对添加到字典中。
# 最后，返回包含对象属性键值对的字典。
# 这个函数的目的是将Account对象转换为字典，方便后续进行 JSON 序列化或其他操作。


def search_users():
    # 获取前端传来的搜索参数
    # test = request.cookies
    # j_username = test['j_username']
    j_username = request.headers.get('Authorization')
    result = None
    data = request.json
    # print(type(data))
    name = data['name'] if data['name'] != '' else None
    city = data['city'] if data['city'] != '' else None
    hobbies = data['hobbies'] if data['hobbies'] != '' else None
    sex = data['sex'] if data['sex'] != '' else None
    min_height = data['min_height'] if data['min_height'] != '' else None
    min_weight = data['min_weight'] if data['min_weight'] != '' else None
    max_height = data['max_height'] if data['max_height'] != '' else None
    max_weight = data['max_weight'] if data['max_weight'] != '' else None
    introduction = data['introduction'] if data['introduction'] != '' else None
    personality = data['personality'] if data['personality'] != '' else None
    age = data['age'] if data['age'] != '' else None
    number = data['number'] if data['number'] != '' else None
    major = data['major'] if data['major'] != '' else None
    print(name)
    try:
        # 构建 SQL 查询语句的基础部分
        sqlstr = "SELECT * FROM account WHERE 1=1 AND j_username != :j_username"
        # sqlstr = "SELECT * FROM account WHERE 1=1 "
        print(sqlstr)
        # 添加非空参数的条件到查询语句中
        if name is not None and name.lower() != "null":
            sqlstr = sqlstr + " AND name = :name"
        if city is not None and city.lower() != "null":
            sqlstr = sqlstr + " AND city = :city"
        if hobbies is not None and hobbies.lower() != "null":
            sqlstr = sqlstr + " AND hobbies LIKE :hobbies"
        if sex is not None and sex.lower() != "null":
            sqlstr = sqlstr + " AND sex = :sex"
        if min_height is not None and min_height.lower() != "null":
            sqlstr = sqlstr + " AND height >= :min_height"
        if min_weight is not None and min_weight.lower() != "null":
            sqlstr = sqlstr + " AND weight >= :min_weight"
        if max_height is not None and max_height.lower() != "null":
            sqlstr = sqlstr + " AND height <= :max_height"
        if max_weight is not None and max_weight.lower() != "null":
            sqlstr = sqlstr + " AND weight <= :max_weight"
        if personality is not None and personality.lower() != "null":
            sqlstr = sqlstr + " AND personality = :personality"
        if age is not None and age.lower() != "null":
            sqlstr = sqlstr + " AND age = :age"
        if major is not None and major.lower() != "null":
            sqlstr = sqlstr + " AND major = :major"

        print(sqlstr)
        # 执行 SQL 查询
        query = text(sqlstr)
        result = db.session.execute(query, {
            'j_username': j_username,
            'name': name,
            'city': city,
            'hobbies': f"%{hobbies}%",
            'sex': sex,
            'min_height': min_height,
            'min_weight': min_weight,
            'max_height': max_height,
            'max_weight': max_weight,
            'personality': personality,
            'age': age,
            'major': major,
        })
        # print(222, result)
    # if result is None:
    #     response = {'status': 'success', 'message': str("查询结果为空")}
    #     return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    try:
        # 获取查询结果并转换为字典格式
        users_data = [serialize_account(account) for account in result.fetchall()]

        response = {'status': 'success', 'users': users_data}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def get_hobbies():
    try:
        # 查询数据库获取所有hobbies信息
        hobbies = Hobby.query.all()

        # 构建要返回的hobbies信息字典列表
        hobbies_data = [serialize_hobby(hobby) for hobby in hobbies]

        response = {'status': 'success', 'hobbies': hobbies_data}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def serialize_hobby(hobby):
    return {
        'id': hobby.id,
        'hobby': hobby.hobby
    }


