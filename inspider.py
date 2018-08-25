from getFromTab import getPicJson, saveSingleImage, saveMultiImages, saveVideo, saveText
from getFromUser import getHomeJson, getAllPicUrls, saveBio
import sys
import os
import argparse

def saveFromUrl(url, save_path):
    resJson, media_flag = getPicJson(url)
    if media_flag == 'single':
        saveSingleImage(resJson, save_path)
        # saveText(resJson, save_path)
    elif media_flag == 'multi':
        saveMultiImages(resJson, save_path)
        # saveText(resJson, save_path)
    elif media_flag == 'video':
        saveVideo(resJson, save_path)
        # saveText(resJson, save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify which kind of url.")
    parser.add_argument('--mode', dest='mode', help="Choose from \'p\' or \'u\', where \'p\' represents this url is a image url, and \'u\' represents this url is someone's homepage.", required=True)
    parser.add_argument('--url', dest='url', help="Specify an Instagram url.", required=True)
    parser.add_argument('--count', dest='count', type=int, default=20, help="How much urls you want to crawl.", required=False)
    
    args = parser.parse_args()
    ins_url = str(args.url)

    # 单个链接爬虫
    if args.mode == 'p':
        try:
            os.mkdir('Images')
        except FileExistsError:
            pass
            
        save_path = 'Images/' + ins_url.split('p/')[1][:-1]
        try:
            os.mkdir(save_path)
        except FileExistsError:
            pass
        saveFromUrl(ins_url, save_path)

    # 个人主页爬虫
    elif args.mode == 'u':
        save_path = ins_url.split('com/')[1][:-1]
        resJson = getHomeJson(ins_url)
        try:
            os.mkdir(save_path)
        except FileExistsError:
            pass

        saveBio(resJson, save_path)
        urls = getAllPicUrls(resJson, args.count)
        for i, url in enumerate(urls):
            print(str(i+1) + '/' + str(len(urls)))
            saveFromUrl(url, save_path)
        print("ALL FINISHED.")

