# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:11:55 2019

@author: Dora
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'