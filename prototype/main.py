# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:37:13 2019

@author: Dora
"""

# main.py
from tables import *
from test_foursquare import *
from flask import Flask
from forms import *
from flask import flash, render_template, request, redirect, url_for
from flask_oauth import OAuth
from flask import session
from flask import redirect
import requests
import json
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3

oauth = OAuth()

app = Flask(__name__)
app.secret_key = "dev"

#creates a db file in the repo
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False)
#     image_urls = db.Column(db.Char)
#     comment_count = db.Column(db.Integer)
#     captions = db.Column(db.Char)
#     num_likes = db.Column(db.Integer)
# #   posts = db.relationship('Post', lazy=True)

    
def __repr__(self):
    return f"User('{self.id}', '{self.username}')"

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='437873623791939',
    consumer_secret='d4c50e029c24dc447aef350328451e18',
    request_token_params={'scope': 'email, instagram_basic, pages_show_list, instagram_manage_insights, instagram_manage_comments'}
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
    print("resp is ",resp)
    session['oauth_token'] = (resp['access_token'], '')
    #me = facebook.get('/me')
    return redirect(url_for("main_menu"))

@app.route('/login')
def login():
    print("hello")
    return facebook.authorize(callback=url_for('oauth_authorized', _external=True))

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')

def append_person(s):
    person = get_facebook_token()[0]
    link = s + person
    return link

@app.route('/main_menu', methods=['GET','POST'])
def main_menu():
    link = append_person('https://graph.facebook.com/v5.0/me?fields=first_name&access_token=')
    r = requests.get(link)
    r = json.loads(r.text)
    name = r["first_name"]
    session['first_name'] = name
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'Search_id':
            return redirect(url_for('search'))
        elif request.form['btn_identifier'] == 'Analytics_id':
            return redirect(url_for('analytics'))

    return render_template('main_menu.html',name=name)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search = PlaceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('search.html', form=search)

def accounts_get():
    accounts_link = append_person('https://graph.facebook.com/v5.0/me?fields=accounts&access_token=')
    accounts_res = requests.get(accounts_link)
    accounts_res = json.loads(accounts_res.text)
    page_name = accounts_res["accounts"]["data"][0]["name"]
    session["page_name"] = page_name
    page_id = accounts_res["accounts"]["data"][0]["id"]
    session["page_id"] = page_id
    
def ig_get():
    page_id = session["page_id"]
    ig_link = 'https://graph.facebook.com/v5.0/' + page_id + '?fields=instagram_business_account&access_token='
    ig_link = append_person(ig_link)
    ig_res = requests.get(ig_link)
    ig_res = json.loads(ig_res.text)
    ig_id = ig_res["instagram_business_account"]["id"]
    session["ig_id"] = ig_id
    
def media_get():
    ig_id = session["ig_id"]
    media_link = 'https://graph.facebook.com/v5.0/' + ig_id + "/media?access_token="
    media_link = append_person(media_link)
    media_res = requests.get(media_link)
    media_res = json.loads(media_res.text)
    posts = []
    for x in range(len(media_res["data"])):
        posts += [media_res["data"][x]["id"]]
    session["posts"] = posts
    captions = []
    likes = []
    urls = []
    for x in range(len(posts)):
        x_cap = captions_get(posts[x])
        x_likes = likes_get(posts[x])
        x_url = photo_url(posts[x])
        urls += [x_url]
        captions += [x_cap]
        likes += [x_likes]
    session["photo_urls"] = urls
    session["captions"] = captions
    session["likes"] = likes
    
def photo_url(post_id):
    post_link = 'https://graph.facebook.com/v5.0/' + post_id + "?fields=media_url&access_token="
    post_link = append_person(post_link)
    url_res = requests.get(post_link)
    url_res = json.loads(url_res.text)
    return url_res["media_url"] 
    
def captions_get(post_id):
    post_link = 'https://graph.facebook.com/v5.0/' + post_id + "?fields=caption&access_token="
    post_link = append_person(post_link)
    caption_res = requests.get(post_link)
    caption_res = json.loads(caption_res.text)
    return caption_res["caption"] 
    
def likes_get(post_id):
    post_link = 'https://graph.facebook.com/v5.0/' + post_id + "?fields=like_count&access_token="
    post_link = append_person(post_link)
    likes_res = requests.get(post_link)
    likes_res = json.loads(likes_res.text)
    return likes_res["like_count"]

def to_Database(table, ana_list): 
    # creating connection to Database 
    db_file = r"InstagramAnalytics.db" 
    conn = sqlite3.connect(db_file, timeout=10.0)
 
    in_table = ''' INSERT INTO Instagram(name, likes, captions) VALUES(?,?,?) '''
    cur = conn.cursor() 
    cur.execute(in_table, ana_list)
    conn.commit() 
    conn.close() 

@app.route('/analytics', methods=['GET','POST'])
def analytics():
    accounts_get()
    page_name=session["page_name"]
    ig_get()
    media_get()
    photo_urls = session["photo_urls"]
    analytics_list = [page_name, session["likes"], session["captions"]]
    to_Database(page_name, analytics_list)

###########
    # CommentCount = len(session["captions"])
    # userToAdd = User(username=page_name, image_urls=photo_urls, comment_count=CommentCount, captions=session["captions"], num_likes=sum(session["likes"])
    # db.session.add(UserToAdd)
###########

    return render_template('analytics.html', page_name=page_name, photos=photo_urls)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    
    results = call_API(search_string)
    #display results
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




