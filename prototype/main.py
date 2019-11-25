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
from flask import flash, render_template, request, redirect, url_for
from flask_oauth import OAuth
from flask import session
from flask import redirect


oauth = OAuth()
 
app = Flask(__name__)
app.secret_key = "dev"


facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='437873623791939',
    consumer_secret='d4c50e029c24dc447aef350328451e18',
    request_token_params={'scope': 'email'}
)

@app.route('/oauth-authorized')
@facebook.authorized_handler
def oauth_authorized(resp):
    print("hello2")
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    #me = facebook.get('/me')
    return redirect(url_for("search"))

@app.route('/login')
def login():
    print("hello")
    return facebook.authorize(callback=url_for('oauth_authorized', _external=True))

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')

@app.route('/search', methods=['GET', 'POST'])
def search():
    search = PlaceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('search.html', form=search)
 
 
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

@app.route('/', methods=['POST', 'GET'])
def index():
    #return login()
    if request.method == 'POST':
        return login()
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(ssl_context='adhoc')