from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #  创建了一个名为db的SQLAlchemy对象，它代表了整个数据库的抽象。


# flask_sqlalchemy 是 Flask 框架的一个扩展，提供了与 SQLAlchemy ORM（对象关系映射）库的集成，用于在 Flask 应用程序中方便地进行数据库操作。
#
# SQLAlchemy 是一个功能强大的 Python SQL 工具包，用于管理数据库。它提供了一种将数据库表示为 Python 对象的方式，通过对象之间的关系和操作来进行数据库的查询和操作，从而使开发人员能够使用面向对象的方式来处理数据库。
#
# 在上述代码中，db = SQLAlchemy() 创建了一个 SQLAlchemy 对象实例，用于与数据库进行交互。通过使用这个实例，我们可以执行各种数据库操作，例如创建数据库模型、查询数据、插入数据、更新数据和删除数据等。
#
# 在 Flask 应用程序中，通过将这个 db 对象与应用程序进行关联，我们可以在视图函数或模型中轻松地使用 SQLAlchemy 提供的功能来进行数据库操作，简化了与数据库的交互过程，提高了开发效率。