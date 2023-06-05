from database import db


class Account(db.Model):
    __tablename__ = 'account'

    j_username = db.Column(db.String(12), primary_key=True)
    j_password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(10))
    city = db.Column(db.String(10))
    hobbies = db.Column(db.String(100))
    sex = db.Column(db.String(2))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    introduction = db.Column(db.String(1000))
    number = db.Column(db.String(11))
    personality = db.Column(db.String(4))
    age = db.Column(db.Integer)
    major = db.Column(db.String(30))
    labels = db.Column(db.String(55))
    # def __init__(self, j_username, name, city, hobbies, sex, height, weight, introduction, number, personality, age, major):
    #     self.j_username = j_username
    #     self.name = name
    #     self.city = city
    #     self.hobbies = hobbies
    #     self.sex = sex
    #     self.height = height
    #     self.weight = weight
    #     self.introduction = introduction
    #     self.number = number
    #     self.personality = personality
    #     self.age = age
    #     self.major = major
    # 其他代码...


class Hobby(db.Model):
    __tablename__ = 'hobbies'

    id = db.Column(db.Integer, primary_key=True)
    hobby = db.Column(db.String(20))


class Administrator(db.Model):
    __tablename__ = 'administrator'
    id = db.Column(db.String(12), primary_key=True)
    password = db.Column(db.String(20))


class Report(db.Model):
    __tablename__ = 'report'
    # __mapper_args__ = {
    #     "non_primary": True
    # }
    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.String(12))
    reported_username = db.Column(db.String(12))
    message = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    itype = db.Column(db.String(8))

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(12))
    receiver = db.Column(db.String(12))
    content = db.Column(db.String(100))
    time = db.Column(db.DateTime)

    # def __init__(self, sender, receiver, content, time):
    #     self.sender = sender
    #     self.receiver = receiver
    #     self.content = content
    #     self.time = time
