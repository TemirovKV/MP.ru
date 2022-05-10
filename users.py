import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from db_session import SqlAlchemyBase
from flask_login import UserMixin
import sqlite3


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    clas = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    score = sqlalchemy.Column(sqlalchemy.INT)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def make_calculations(self, id):
        a = 0
        from main import current_user
        con = sqlite3.connect("db/users.db")
        cur = con.cursor()
        self.list_of_rewards = cur.execute(f"""
            SELECT reward, deg FROM rewards
            WHERE id="{id}" """).fetchall()
        print(2)
        print(self.list_of_rewards)
        for i in self.list_of_rewards:
            print(i)
            print(i[0])
            self.a = cur.execute(f"""
            SELECT {i[1]} FROM score_table
            WHERE awards="{i[0]}" """).fetchone()
            print(self.a)
            a += int(self.a[0])
        print(3)
        cur.execute(f'''update users set score = '{a}' where id = {id}''')
        con.commit()
        con.close()