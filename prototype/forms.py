# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:32:32 2019

@author: Dora
"""

# forms.py
 
from wtforms import Form, StringField, SelectField
 
class PlaceSearchForm(Form):

    select = SelectField('Search for music:')
    search = StringField('')