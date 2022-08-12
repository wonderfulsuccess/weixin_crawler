"""
RESTful API
"""
from web_server.api.helloworld import HelloWorld
from web_server.api.crawler import Crawler
from web_server.api.gzh import GZH
from web_server.api.settings import Settings
from web_server.api.search import Search
from web_server.api.like import MyLikeAPI

api_resources = [
    {'res':HelloWorld, 'url':'/helloworld'},
    {'res':Crawler, 'url':'/crawler'},
    {'res':GZH, 'url':'/gzh'},
    {'res':Settings, 'url':'/settings'},
    {'res':Search, 'url':'/search'},
    {'res':MyLikeAPI, 'url':'/like'},
]
