from flask import Flask, send_from_directory

app = Flask(__name__)

# @app.route('/avatars/<filename>')


def get_avatar(filename):
    avatars_dir = 'avatars'  # 头像图片存放的目录
    return send_from_directory(avatars_dir, filename)  # 从指定目录发送文件

def get_avatar(filename):
    avatars_dir = 'avatars'  # 头像图片存放的目录
    return send_from_directory(avatars_dir, filename)  # 从指定目录发送文件