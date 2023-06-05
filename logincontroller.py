from flask import request, jsonify, session, make_response

from Entity import Account,Administrator

from base64 import b64encode

# from networkx import descendants_at_distance
from pyDes import des, ECB, PAD_PKCS5
import datetime


def login():
    try:
        data = request.json
        j_username = data['j_username']
        j_password = data['j_password']
    except KeyError as e:
        return jsonify({'message': 'Invalid request data: {}'.format(str(e))}), 400

    account = Account.query.filter_by(j_username=j_username).first()  # 返回第一个对象

    if account and account.j_password == j_password:
        # 登录成功，将用户名存储在会话中
        # session['username'] = j_username
        # response = make_response()
        response = make_response(jsonify({'message': 'Login successful'}))
        expires = datetime.datetime.now() + datetime.timedelta(days=1)
        response.set_cookie('j_username', j_username, expires=expires)
        response.headers['Authorization'] = j_username
        return response
    else:
        return jsonify({'message': 'Invalid username or password'})


def adlogin():
    try:
        data = request.json
        id = data['id']
        password = data['password']
    except KeyError as e:
        return jsonify({'message': 'Invalid request data: {}'.format(str(e))}), 400

    account = Administrator.query.filter_by(id=id).first()  # 返回第一个对象

    if account and account.password == password:
        # 登录成功，将用户名存储在会话中
        # session['username'] = j_username
        # response = make_response()
        response = make_response(jsonify({'message': 'Login successful'}))
        expires = datetime.datetime.now() + datetime.timedelta(days=1)
        response.set_cookie('id', id, expires=expires)
        response.headers['Authorization'] = id
        return response
    else:
        return jsonify({'message': 'Invalid username or password'})


def home():
    # 从会话中获取用户名
    # j_username = session.get('j_username')
    j_username = request.headers.get('Authorization')
    # 根据用户名进行其他操作...

    return 'Welcome, {}'.format(j_username)


# 在 Flask 中，session 对象是一个字典，可以将数据以键值对的形式存储在会话中。在这种情况下，session['username'] 存储的是用户名，它是一个字符串形式的值。
#
# 当用户成功登录并且用户名被存储在 session['username'] 中后，Flask 会在后续的请求中自动将该会话信息传递给服务器，以便识别当前用户。
# 因此，可以通过访问 session['username'] 来获取已登录用户的用户名，并在应用程序的其他部分使用它来执行相关的操作或验证用户身份。


def encryptByDES():
    message = request.json['j_password']
    secret_key = 'PassB01Il71'[0:8]  # 密钥
    iv = secret_key  # 偏移
    # secret_key:加密密钥，EBC:加密模式，iv:偏移, padmode:填充
    des_obj = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    # des_obj = des(secret_key, ECB, iv,  padmode=PAD_PKCS5)/
    # 返回为字节
    secret_bytes = des_obj.encrypt(message, padmode=PAD_PKCS5)
    # 返回为base64字符串
    secret_base64 = b64encode(secret_bytes).decode('utf-8')
    response = {'status': 'success', 'password': secret_base64}
    return jsonify(response)

# print(encryptByDES("@lyp2408676557"))
