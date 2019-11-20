# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:37:13 2019

@author: Dora
"""

# main.py
from tables import *
from test_foursquare import *
from flask import Flask
from forms import PlaceSearchForm
from flask import flash, render_template, request, redirect
 
app = Flask(__name__)
app.secret_key = "dev"
 
@app.route('/', methods=['GET', 'POST'])
def index():
    search = PlaceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('index.html', form=search)
 
 
@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    
    results = call_API(search_string)
    # display results
    #results = [dict(city="Boston", name="Tatte", address="Beacon St")]
    table = Results(results)
    table.border = True
    return render_template('results.html', table=table)
 
if __name__ == '__main__':
    app.run()