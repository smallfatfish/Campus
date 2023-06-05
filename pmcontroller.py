from flask import jsonify, request
from Entity import Message
from database import db
from sqlalchemy import or_,and_
import datetime


def get_pm():
    try:
        sender = request.headers.get('Authorization')
        receiver = request.json['receiver']
        # 查询数据库获取符合条件的消息记录，并按照时间排序

        messages = Message.query.filter(
            or_(
                (Message.sender == sender) & (Message.receiver == receiver),
                (Message.sender == receiver) & (Message.receiver == sender)
            )
        ).order_by(Message.time).all()
        print(messages)
        # 构建要返回的消息数据字典列表
        messages_data = [serialize_message(message) for message in messages]

        response = {'status': 'success', 'messages': messages_data}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def serialize_message(message):
    return {
        'sender': message.sender,
        'receiver': message.receiver,
        'content': message.content,
        'time': message.time.strftime('%Y-%m-%d %H:%M:%S')
    }


def send_pm():
    sender = request.headers['Authorization']
    receiver = request.json['receiver']
    content = request.json['content']
    time = datetime.datetime.now()

    message = Message(sender=sender, receiver=receiver, content=content, time=time)

    try:
        db.session.add(message)
        db.session.commit()
        response = {'status': 'success', 'message': 'Private message sent successfully.'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)
