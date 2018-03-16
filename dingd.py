#!/usr/bin/python
#encoding=utf-8
'''
基于BaseHTTPServer的http server实现，包括get，post方法，get参数接收，post参数接收。
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib,httplib
import os, sys

host = '0.0.0.0'
port = 18025
addr = (host,port)


import logging
import requests
import re

class DingTalkRobot(object):
    def __init__(self, api_url, access_token):
        self.url = '%s?access_token=%s' % (api_url, access_token)
        
    def send_text_msg(self, content, at_all=False):
        newcon = re.sub('\+all.*\)\+|\[\]|O1\+|\[P0\]|\+', " ", content)
        msg = {
            'msgtype': 'text',
            'text': {
                'content': newcon
            },
            'at': {
                'atMobiles': [],
                'isAtAll': at_all
            }
        }
        r = requests.post(self.url, json=msg, headers={'Content-Type': 'application/json'})


class Servers(BaseHTTPRequestHandler):

    def do_POST(self):
        mpath,margs=urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.do_action(mpath, datas)

    def do_action(self, path, args):
        self.outputtxt(path + args )
        self.send_sms(args)

    def outputtxt(self, content):
        #指定返回编码
        enc = "UTF-8"
        content = content.encode(enc)
        self.send_response(200)  

    def send_sms(self,args):

        post_str = urllib.unquote(args)
        post_dict = dict([x.split('=',1) for x in post_str.split('&')])
        #包含content和tos两部分
        DingTalkRobot(
            'https://oapi.dingtalk.com/robot/send',
            'access_token').send_text_msg(
            "监控报警："+post_dict['content'], False)

print 'server is running....'
server = HTTPServer(addr,Servers)
server.serve_forever()
