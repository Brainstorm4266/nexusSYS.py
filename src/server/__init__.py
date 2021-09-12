from flask import Flask
from flask import send_file
from flask import request
from bs4 import BeautifulSoup
import asyncio

def init():
    print('[SERVER]: Initializing...')
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
        return "<p>Coming soon, mate! Your search query is: "+h+"."
    @app.route("/about")
    def about():
        return send_file("./html/about.html")
    asyncio.run(app.run())