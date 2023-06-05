from flask import request, jsonify, session
from sqlalchemy import text
from sqlalchemy.orm import class_mapper

from database import db
from Entity import Account


def get_liked_users():
    # j_username = session.get('username')
    # j_username = request.json['j_username']  # 前端发送的点赞者的j_username
    try:
        # test = request.cookies
        # j_username = test['j_username']
        j_username = request.headers.get('Authorization')
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    try:
        # 执行原始的SQL查询，找到点赞者点赞过的人
        liked_query = text("SELECT liked_username FROM likes WHERE j_username = :j_username")
        liked_result = db.session.execute(liked_query, {'j_username': j_username})  # 查询结果是一个包含多个元组的列表
        # print(liked_result.fetchall())
        # print(type(liked_result))
        liked_users = [row[0] for row in liked_result]
        print(liked_users)
        # 执行原始的SQL查询，找到给该点赞者点赞的人
        liked_by_query = text("SELECT j_username FROM likes WHERE liked_username = :j_username")
        liked_by_result = db.session.execute(liked_by_query, {'j_username': j_username})
        liked_by_users = [row[0] for row in liked_by_result]
        print(liked_by_users)

        # 查询account表中liked_by_users的所有数据并返回
        liked_by_users_data = Account.query.filter(Account.j_username.in_(liked_by_users)).all()
        liked_by_users_data = [serialize_account(account) for account in liked_by_users_data]

        like_each_other=[]
        for like in liked_users:
            for liked in liked_by_users:
                if like == liked:
                    like_each_other.append(like)

        response = {'status': 'success', 'like_each_other': like_each_other, 'liked_by_users_data': liked_by_users_data}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def serialize_account(account):
    columns = [column.key for column in class_mapper(Account).columns]
    return {column: getattr(account, column) for column in columns}


def save_like():
    # j_username = request.json['j_username']  # 点赞者的j_username
    # test = request.cookies
    # j_username = test['j_username']
    j_username = request.headers.get('Authorization')
    liked_username = request.json['liked_username']  # 被点赞者的j_username

    try:
        # 检查记录是否存在
        query = text("SELECT * FROM likes WHERE j_username = :j_username AND liked_username = :liked_username")
        result = db.session.execute(query, {'j_username': j_username, 'liked_username': liked_username})

        if result.fetchone():
            # 如果记录存在，则删除该记录
            delete_query = text("DELETE FROM likes WHERE j_username = :j_username AND liked_username = :liked_username")
            db.session.execute(delete_query, {'j_username': j_username, 'liked_username': liked_username})
            response = {'status': 'success', 'message': 'Unliked successfully.'}
        else:
            # 如果记录不存在，则创建新的点赞记录
            insert_query = text("INSERT INTO likes (j_username, liked_username) VALUES (:j_username, :liked_username)")
            db.session.execute(insert_query, {'j_username': j_username, 'liked_username': liked_username})
            response = {'status': 'success', 'message': 'Liked successfully.'}

        db.session.commit()
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def if_like():
    # test = request.cookies
    # j_username = test['j_username']
    j_username = request.headers.get('Authorization')
    current_username = request.json['current_username']
    try:
        sqlstr="SELECT * FROM likes WHERE j_username = :j_username AND liked_username = :current_username"
        querry=text(sqlstr)
        result=db.session.execute(querry, {
            'j_username': j_username,
            'current_username': current_username
        })
        # liked_users = [row[0] for row in result]
        # print(result.fetchone())result.fetchone()返回查询结果的下一行作为单个结果元组，或者在没有更多行时返回None。
        if result.fetchone():
            response = {'status': 'success', 'message': str("like")}
        else:
            response = {'status': 'success', 'message': str("no like")}
        # if result.fetchone():
        #     response = {'status': 'success', 'message': str("no like")}
        # else:
        #     response = {'status': 'success', 'message': str("like")}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    return response
