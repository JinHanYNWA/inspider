#-*- coding: utf-8 -*-
"""
Created on Sat Sep 23 13:48:39 2017

@author: Administrator
"""

import json
import urllib.request, urllib.error
import sys
import os
import socket
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
        }

# 设置urllib.request的代理
proxy_support = urllib.request.ProxyHandler({'https': '127.0.0.1:1087'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

# 得到json对象
def getHomeJson(ins_url):
    req = urllib.request.Request(ins_url + '?__a=1', headers = headers)
    attempts = 0
    success = False 

    while attempts < 3 and not success:
        try:
            response = urllib.request.urlopen(req, timeout = 8)

        except socket.timeout:
            print(ins_url + " time out!")
            attempts += 1

        except urllib.error.URLError as e:
            print(e.reason)
            attempts += 1

        else:
            success = True
            html = response.read()
            resJson = json.loads(html.decode('utf-8'))
            resJsonIndent = json.dumps(resJson, indent = 4)
            '''
            f = open('pagesource.txt', 'w', encoding = 'utf-8')
            f.write(str(resJsonIndent))
            f.close()
            '''
    return resJson

def saveBio(resJson, save_path):
    bio = resJson['graphql']['user']['biography']
    if resJson['graphql']['user']['external_url'] != None:
        bio = bio + '\n' + resJson['graphql']['user']['external_url']
    if bio == None:
        bio = ''
    fb = open(save_path + "\\biography.txt", 'w', encoding = 'utf-8')
    fb.write(bio)
    fb.close()

def getAllPicUrls(initResJson, count):
    urls = []
    first_page_urls = initResJson['graphql']['user']['edge_owner_to_timeline_media']['edges']
    
    for e in first_page_urls:
        code = e['node']['shortcode']
        urls.append("https://www.instagram.com/p/" + code + "/")
        print("GET " + "https://www.instagram.com/p/" + code + "/")
        if count != None and len(urls) >= count:
            return urls

    user_id = initResJson['graphql']['user']['id']
    end_cursor = initResJson['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    has_next_page = initResJson['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

    while(has_next_page):
        next_url = "https://www.instagram.com/graphql/query/?variables=%%7B%%20%%22id%%22%%3A%%22%s%%22%%2C%%22first%%22%%3A12%%2C%%22after%%22%%3A%%22%s%%22%%7D&query_id=17888483320059182"
        req = urllib.request.Request(next_url % (user_id, end_cursor))
        attempts = 0
        success = False

        while attempts < 3 and not success:
            try:
                response = urllib.request.urlopen(req, timeout = 8)

            except socket.timeout:
                print(next_url + " time out!")
                attempts += 1

            except urllib.error.URLError:
                print(next_url + " is Error!")
                attempts += 1

            else:
                success = True
                html = response.read()
                nextJson = json.loads(html.decode('utf-8'))
        
        items = nextJson['data']['user']['edge_owner_to_timeline_media']['edges']
        for e in items:
            if count != None and len(urls) >= count:
                return urls

            code = e['node']['shortcode']
            urls.append("https://www.instagram.com/p/" + code + "/")
            print("GET " + "https://www.instagram.com/p/" + code + "/")

        end_cursor = nextJson['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        has_next_page = nextJson['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

    return urls