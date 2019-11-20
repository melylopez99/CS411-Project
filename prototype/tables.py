# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:19:53 2019

@author: Dora
"""

from flask_table import Table, Col

class Results(Table):
    #city = Col("City")
    name = Col("Name")
    address = Col("Address")