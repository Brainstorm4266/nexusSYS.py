import asyncio
import hashlib
import json
import os
import sqlite3
import uuid
from array import array
from base64 import encode

import OpenSSL
import urllib3
from bs4 import BeautifulSoup
from flask import Flask, redirect, request, send_file


def create_session_id():
    return uuid.UUID(bytes = os.urandom(16))

def hash_pass(password):
    return hashlib.md5(str(password).encode('utf-8')).hexdigest()

def compare_hashes(userhash, passhash):
    if userhash == passhash:
        return True
    else:
        return False

def check_hash(userpass, passhash):
    return compare_hashes(hashlib.md5(str(userpass).encode('utf-8')).hexdigest(), passhash)

def parse(data):
    if isinstance(data, dict):
        return data
    elif isinstance(data, str):
        try:
            return json.loads(data)
        except:
            return str(data)
    elif isinstance(data, array):
        return data
    elif isinstance(data, int):
        return int(data)
    elif isinstance(data, float):
        return float(data)
    else:
        return data
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
            return soup.prettify("utf-8") # //TODO: Fix redirect page visual issues caused by bs4.
        else:
            chapters = curs.execute('SELECT * FROM "chapters"')
            chapter = chapters.fetchall()[int(h2)]
            print(chapter)
            lol = chapter[3]
            return send_file("./post.html") # I'll switch it out so it would return a post webpage template, and that would get the chapter from API.
    @app.route("/api/get_post")
    def post_api():
        h = request.args.get('post')
        print("[nexusSYS]: API REQUEST: /api/get_post")
        connecc = sqlite3.connect("main_data.db")
        curs = connecc.cursor()
        print(request.get_data())
        if h == None:
            return "Invalid request.", 400
        else:
            if True: # Do I look like I want to unindent all of this right now?
                data = h
                if h == None:
                    return "Invalid request.", 400
                else:
                    def get_user(id):
                        user = curs.execute('SELECT * FROM "users"').fetchall()[int(id)]
                        return {
                            "id": parse(user[0]),
                            "name": parse(user[1])
                        }
                    def get_chapters():
                        chaps = json.loads(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][4])
                        table = []
                        for chap in chaps:
                            table.append({
                                "id": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][0]),
                                "private": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][1]),
                                "author": parse(get_user(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][2])),
                                "text": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][3]),
                                "notes": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][4]),
                                "note_top": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][5]),
                                "note_bottom": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][6]),
                                "post": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][7]),
                                "name": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][8]),
                                "chapter_num":parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(chap)][9])
                            })
                        return table
                    return {
                        "id": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][0]),
                        "name": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][1]),
                        "author": parse(get_user(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][2])),
                        "chapters_amount": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][3]),
                        "chapters": get_chapters(),
                        "private": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][5]),
                        "description": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][6])
                    }
    @app.route("/api/get_chapter")
    def chapter_api():
        h = request.args.get('chapter')
        print("[nexusSYS]: API REQUEST: /api/get_chapter")
        connecc = sqlite3.connect("main_data.db")
        curs = connecc.cursor()
        print(request.get_data())
        if h == None:
            return "Invalid request.", 400
        else:
            if True: # Do I look like I want to unindent all of this right now?
                data = h
                if h == None:
                    return "Invalid request.", 400
                else:
                    def get_user(id):
                        user = curs.execute('SELECT * FROM "users"').fetchall()[int(id)]
                        return {
                            "id": parse(user[0]),
                            "name": parse(user[1])
                        }
                    def get_post():
                        table = {
                            "id": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][0]),
                            "name": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][1]),
                            "author": parse(get_user(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][2])),
                            "chapters_amount": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][3]),
                            "chapters": parse(json.loads(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][4])),
                            "private": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][5]),
                            "description": parse(curs.execute('SELECT * FROM "posts"').fetchall()[int(h)][6])
                        }
                        return table
                    return {
                        "id": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][0]),
                        "private": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][1]),
                        "author": parse(get_user(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][2])),
                        "text": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][3]),
                        "notes": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][4]),
                        "note_top": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][5]),
                        "note_bottom": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][6]),
                        "post": get_post(),
                        "name": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][8]),
                        "chapter_num": parse(curs.execute('SELECT * FROM "chapters"').fetchall()[int(h)][9])
                    }
    @app.route("/post.js")
    def get_post_js():
        return send_file('./html/post.js')
    @app.route('/api/create_user', methods = ['POST'])
    def create_user():
        connecc = sqlite3.connect("main_data.db")
        curs = connecc.cursor()
        print("CREATE USER REQUEST RECIEVED.")
        json_object = json.loads(request.data)
        session_id = create_session_id()
        curs.execute("INSERT INTO \"users\" (name, password_hash, valid_sessions) VALUES (\""+str(json_object["name"])+"\", \""+str(json_object["password_hash"])+"\", \"[\""+str(session_id)+"\"]\")")
        connecc.commit()
        return {
            "success": True,
            "name": str(json_object["name"]),
            "password_hash": str(json_object["password_hash"]),
            "session_id": str(session_id)
        }
    asyncio.run(app.run())
    print("[nexusSYS]: APP STARTED.")
