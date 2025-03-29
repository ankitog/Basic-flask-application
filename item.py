from flask import jsonify, request
import sqlite3
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

class Item(Resource):
    TABLE_NAME = "items"

   
    def get(self, name):
        print("photo")
        print("hello")
        item =  self.find_by_name(name)
        if item:
            return item
        return {'Message': 'Item not found'}, 404
    
    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {'item': {'name':row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "INSERT INTO {table} VALUES (?,?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['name'], item['price']))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'An item with name {} already exist'.format(name)}

        
        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}

        return item

    


    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}
    
    def put(self, name):
        request_data = request.get_json()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': request_data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}

        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}
        return updated_item
            
    
class ItemList(Resource):
    TABLE_NAME ="items"
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * FROM {}".format(self.TABLE_NAME)
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        conn.close()

        return {'item': items}