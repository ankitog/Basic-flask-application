import sqlite3
from flask import request
from flask_restful import Resource, reqparse

class User():
    TABLE_NAME = "users"
    def __init__(self, id_, username_, password_):
        self.id =id_
        self.username = username_
        self.password = password_
    
    @classmethod
    def find_by_username(cls,username):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * FROM {table} WHERE username = ?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        user =  cls(*row) if row else None
        conn.commit()
        conn.close()
        return user

    @classmethod
    def find_my_id(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * FROM {table} WHERE id = ?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (_id,))
        row = cursor.fetchone()
        user =  cls(*row) if row else None
        conn.commit()
        conn.close()
        return user



class UserRegister(Resource):

    TABLE_NAME = "users"
    def post(self):
        data = request.get_json()

        if User.find_by_username(data['username']):
            return {'Message': 'User already exist'}, 400

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        insert_query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(insert_query, (data['username'], data['password']))
        conn.commit()
        conn.close()

        return {'Message': 'User created successfuly'}, 201
