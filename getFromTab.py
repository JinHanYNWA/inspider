#-*- coding: utf-8 -*-
"""
Created on Sat Sep 23 13:48:39 2017

@author: Administrator
"""

import json
import urllib.request, urllib.error
import socket
import sys
import ssl

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

# 设置urllib.request的代理
proxy_support = urllib.request.ProxyHandler({'https': '127.0.0.1:1087'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

# 记录错误urls
def writeErrors(src, save_path):
    f = open(save_path + '/FailedUrls.txt', 'a', encoding = 'utf-8')
    f.write(src + '\n')
    f.close()

# 得到json对象
def getPicJson(ins_url):
    req= urllib.request.Request(ins_url + "?__a=1", headers = headers)
    attempts = 0
    success = False 

    while attempts < 3 and not success:
        try:
            response = urllib.request.urlopen(req, timeout = 8)
            html = response.read()

        except socket.timeout:
            print(ins_url + " time out!")
            attempts += 1
        except urllib.error.URLError as e:
            print(e, ins_url + " is Error!")
            attempts += 1
        except http.client.IncompleteRead:
            print("Read response incompeletely!")
            attempts += 1

        else:
            success = True
            resJson = json.loads(html.decode('utf-8'))

    # 判断是否是多张Image
    if resJson['graphql']['shortcode_media']['__typename'] == 'GraphImage':
        media_flag = 'single'
    elif resJson['graphql']['shortcode_media']['__typename'] == 'GraphSidecar':
        media_flag = 'multi'
    elif resJson['graphql']['shortcode_media']['__typename'] == 'GraphVideo':
        media_flag = 'video'

    print("Getting from " + ins_url)
    print("Likes: " + str(resJson['graphql']['shortcode_media']['edge_media_preview_like']['count']))
    print("Comments: "+ str(resJson['graphql']['shortcode_media']['edge_media_to_comment']['count']))
    return resJson, media_flag

    '''
    resJsonIndent = json.dumps(resJson, indent = 4)
    f = open('mixsource.txt', 'w', encoding = 'utf-8')
    f.write(str(resJsonIndent))
    f.close()
    '''

# 单张图片保存
def saveSingleImage(resJson, save_path):
    img_src = resJson['graphql']['shortcode_media']['display_url']
    media_name = resJson['graphql']['shortcode_media']['shortcode']
    print(img_src)
    try:
        urllib.request.urlretrieve(img_src, save_path + "/" + media_name + ".jpg")

    except ssl.SSLEOFError:
        writeErrors(img_src, save_path)
    except urllib.error.URLError:
        writeErrors(img_src, save_path)
    except urllib.error.ContentTooShortError:
        writeErrors(img_src, save_path)
    else:
        print("Save Image Successfully!\n")

# 多张图片/视频保存
def saveMultiImages(resJson, save_path):
    img_dict = resJson['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
    for e in img_dict:
        if e['node']['is_video'] == True:
            media_src = e['node']['video_url']
            media_name = e['node']['shortcode']
            try:
                urllib.request.urlretrieve(media_src, save_path + '/' + media_name + '.mp4')
                
            except ssl.SSLEOFError:
                writeErrors(media_src, save_path)
            except urllib.error.URLError:
                writeErrors(media_src, save_path)
            except urllib.error.ContentTooShortError:
                writeError(media_src, save_path)

            else:
                print(media_src)

        else:
            media_src = e['node']['display_url']
            media_name = e['node']['shortcode']
            try:
                urllib.request.urlretrieve(media_src, save_path + '/' + media_name + '.jpg')
                
            except ssl.SSLEOFError:
                writeErrors(media_src, save_path)
            except urllib.error.URLError:
                writeErrors(media_src, save_path)
            except urllib.error.ContentTooShortError:
                writeErrors(media_src, save_path)

            else:
                print(media_src)

    print("Save All Media Successfully!\n")

# 视频保存
def saveVideo(resJson, save_path):
    mp4_src = resJson['graphql']['shortcode_media']['video_url']
    media_name = resJson['graphql']['shortcode_media']['shortcode']
    print(mp4_src)
    try:
        urllib.request.urlretrieve(mp4_src, save_path + "/" + media_name + ".mp4")
        
    except ssl.SSLEOFError:
        writeErrors(mp4_src, save_path)
    except urllib.error.URLError:
        writeErrors(mp4_src, save_path)
    except urllib.error.ContentTooShortError:
        writeErrors(mp4_src, save_path)
        
    else:
        print("Save Video Successfully!\n")

# 文本保存
def saveText(resJson, save_path):
    text_list = resJson['graphql']['shortcode_media']['edge_media_to_caption']['edges']
    if len(text_list) == 0:
        text = ''
    else:
        text = text_list[0]['node']['text']
    likes = str(resJson['graphql']['shortcode_media']['edge_media_preview_like']['count'])

    ft = open(save_path + "/text.txt", 'w', encoding = 'utf-8')
    ft.write(text)
    ft.close()
    fl = open(save_path + "/likes.txt", 'w', encoding = 'utf-8')
    fl.write(likes)
    fl.close()
