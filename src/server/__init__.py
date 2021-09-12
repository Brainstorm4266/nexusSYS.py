import asyncio
import json
import os
import sqlite3

import urllib3
from bs4 import BeautifulSoup
from flask import Flask, redirect, request, send_file


def init():
    print('[SERVER]: Initializing sqlite storage system...')
    app = Flask(__name__)
    @app.route("/")
    def homepage():
        return send_file('./html/index.html')
    @app.route("/style.css")
    def style():
        return send_file('./html/style.css')
    @app.route("/assets/nexusSYSlogobig.png")
    def nexsyslogobig():
        return send_file('./html/assets/nexusSYSlogobig.png')
    @app.route("/search.js")
    def searchjs():
        return send_file('./html/search.js')
    @app.route("/assets/jquery.js")
    def jquery():
        return send_file('./html/assets/jquery.js')
    @app.route("/search")
    def search():
        h = request.args.get('query')
        print(h)
        return send_file('./html/search.html')
    @app.route("/about")
    def about():
        return send_file("./html/about.html")
    @app.route("/api/search")
    def search_api():# APIs! Finally!
        print("Search API request recieved.")
    @app.route("/post")
    def get_post():
        connecc = sqlite3.connect("main_data.db")
        curs = connecc.cursor()
        h = request.args.get('post')
        h2 = request.args.get('chapter')
        if h == None:
            return "<p>You didn't specify any post!</p>"
        elif h2 == None:
            post = curs.execute('SELECT * FROM "posts"')
            lol = post.fetchall()[int(h)]
            chapterid = lol[0]
            html = open(os.path.dirname(os.path.realpath(__file__))+"/redirecting.html", "r").read()
            soup = BeautifulSoup(html, "html.parser")
            soup.find('a', {"id":"login"}).findChild("p").replace_with("Log In&nbsp;&nbsp;")
            soup.find('a', {"id":"signup"}).findChild("p").replace_with("Sign Up&nbsp;")
            soup.find('meta', {"id":"redir"}).replace_with(BeautifulSoup("<meta http-equiv='refresh' content='0.1; URL=/post?post="+str(h)+"&chapter="+str(chapterid)+"' />", "html.parser"))
            return soup.prettify("utf-8") # //TODO: Fix redirect page not displaying correctly!
        else:
            chapters = curs.execute('SELECT * FROM "chapters"')
            chapter = chapters.fetchall()[int(h2)]
            print(chapter)
            lol = chapter[3]
            return str(lol) # I'll switch it out so it would return a post webpage template, and that would get the chapter from API.
    asyncio.run(app.run())
