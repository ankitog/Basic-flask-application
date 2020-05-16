# -*- coding: utf-8 -*-
"""
Created on Sat May  9 22:49:20 2020

@author: LENOVO
"""
from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
    
def identity(payload):
    user_id = payload['identity']
    return User.find_my_id(user_id)