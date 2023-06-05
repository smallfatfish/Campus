from flask import request, jsonify
from sqlalchemy import text

from database import db
from Entity import Account


def recommend_users():
    # j_username = request.json['j_username']  # 获取前端发送的查询的j_username
    # response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:8848')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')
    # test = request.cookies
    # j_username=test['j_username']
    j_username = request.headers.get('Authorization')
    n = int(12)  # 选择相似度最高的前n个用户

    try:
        # 获取指定用户的爱好
        query = text("SELECT hobbies FROM account WHERE j_username = :j_username")
        result = db.session.execute(query, {'j_username': j_username})
        hobbies = result.fetchone()[0] if result.rowcount > 0 else ''
        # hobbies是查询结果中的爱好数据，类型为字符串，包含用户的爱好信息
        if hobbies is None:
            return jsonify(0)
        # 将爱好拆分为列表
        user_hobbies = [h.strip() for h in hobbies.split(',')]
        # user_hobbies是一个列表，包含了用户的爱好，通过将爱好字符串拆分后得到

        # 获取所有用户的爱好
        all_users = []
        all_users_query = text(
            "SELECT j_username, hobbies FROM account WHERE j_username != :j_username and hobbies is not null")
        all_users_result = db.session.execute(all_users_query, {'j_username': j_username})
        # all_users_result是查询结果，包含了其他用户的用户名和爱好数据，类型为SQLAlchemy的ResultProxy对象

        if all_users_result.rowcount > 0:
            # 遍历查询结果，并将每个用户的用户名和爱好存储到字典中，添加到all_users列表中
            for row in all_users_result.fetchall():
                if len(row) == 2:
                    user_data = {'j_username': row[0], 'hobbies': row[1]}
                    all_users.append(user_data)
        # all_users是一个列表，包含了所有其他用户的用户名和爱好信息，通过遍历查询结果得到

        # 计算每个用户与指定用户的爱好相似度
        similarity_scores = []
        for user in all_users:
            target_hobbies = [h.strip() for h in user['hobbies'].split(',')]
            similarity_score = calculate_similarity(user_hobbies, target_hobbies, len(target_hobbies))
            similarity_scores.append((user['j_username'], similarity_score))
        # similarity_scores是一个包含用户和相似度得分的元组的列表。
        # 每个元组的第一个元素是用户的用户名，第二个元素是与指定用户的爱好相似度得分。

        # 根据相似度排序，选择相似度较高的几个用户进行推荐
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        recommended_users = [str(user) for user in similarity_scores[:n]]
        # recommended_users是一个列表，包含了相似度最高的前n个用户的用户名，转换为字符串类型后得到
        # similarity_scores
        # 是一个包含用户和相似度得分的元组的列表。每个元组的第一个元素是用户的用户名，第二个元素是与指定用户的爱好相似度得分。
        #
        # sort
        # 方法用于对列表进行排序，其中的参数
        # key = lambda x: x[1]
        # 指定了排序的依据，即使用元组的第二个元素作为排序的依据（即相似度得分）。lambda x: x[1]
        # 是一个匿名函数，表示取每个元组的第二个元素作为排序的依据。

        response = {'status': 'success', 'recommended_users': recommended_users}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


def calculate_similarity(hobbies1, hobbies2, target_len):
    # 计算两个爱好列表的相似度，可以根据实际需求使用不同的相似度计算方法
    # 这里简单示例为计算共同爱好数量
    common_hobbies = set(hobbies1) & set(hobbies2)
    similarity_score = len(common_hobbies)
    return float(similarity_score/target_len)
