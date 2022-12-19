
# -*- coding: utf-8 -*
import json
import random
import re
import sys
import threading
import requests
import cate_list

user_sessions = {}
user_session_lock = threading.Lock()

def post(path, payload):
    try:
        # print("post, url: {0}, payload: {1}".format(path, payload))
        url = "http://127.0.0.1:8000{}".format(path)
        res = requests.post(url, json=payload)
        # show_url = "curl -d '{0}' '{1}'".format(json.dumps(payload), url)
        # print(show_url)
        return res.content
    except Exception as e:
        print(e)
        return ""


def login(username, password):
    path = "/auth/login/"
    payload = {"username": username, "password": password}
    return post(path, payload)

def getAuthData(username):
    with user_session_lock:
        if username in user_sessions:
            return user_sessions[username]
    res = login(username, "123456")
    user_auth_data = json.loads(res)
    with user_session_lock:
        user_sessions[username] = user_auth_data['user_id'], user_auth_data['session']
    return user_auth_data['user_id'], user_auth_data['session']

def addComment(username, product_id, content, img=''):
    user_id, session = getAuthData(username)
    return innerAddComment(user_id, session, product_id, content, img)

def innerAddComment(user_id, session, product_id, content, img = ''):
    product_id = int(product_id)
    path = "/comment/addcomment/"
    payload = {
        "user_id": user_id, 
        "session": session,
        "product_id":product_id,
        "content": content,
        "resp_comment_id": 0,
        'img': img
    }
    return post(path, payload)

def responseComment(username, comment_id, content, img=''):
    user_id, session = getAuthData(username)
    comment_id = int(comment_id)
    path = "/comment/responsecomment/"
    payload = {
        "user_id": user_id, 
        "session": session,
        "resp_comment_id": comment_id,
        "content": content,
        'img': img
    }
    return post(path, payload)


def getRandomUserName():
    random_num = random.randint(0, 9999999)
    return "testuser{}".format(random_num)

def handleSingleFile(file_name):
    count = 0
    with open('./comments/{}'.format(file_name), 'r') as list_file:
        datas=list_file.read()
        product_comments_list = json.loads(datas)
        for product_comments in product_comments_list:
            try:
                product_id = product_comments['id']
                for comment in product_comments['comment_list']:
                    if 'comment' not in comment or not comment['comment']:
                        print("no comment")
                        continue
                    username = getRandomUserName()
                    resp = addComment(username, product_id, comment['comment'])
                    count += 1
                    if not resp:
                        continue
                    print("{} {}".format(file_name, count))
                    if 'replay' in comment and comment['replay']['comment']:
                        resp_data = json.loads(resp)
                        print(resp_data)
                        if 'id' not in resp_data['comment_data']:
                            continue
                        comment_id = resp_data['comment_data']['id']
                        username = getRandomUserName()
                        responseComment(username, comment_id, comment['replay']['comment'])
                        print("{} {} reply".format(file_name, count))
            except Exception as e:
                print(e)

def handleFile(file_list):
    for file_name in file_list:
        try:
            handleSingleFile(file_name)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    keyword_list = [
        # 'phone', 'dress', 'health', 'kids', 'games', 'books', 
        # 'computer','food', 'sports', 'watches', 'shoes','automotive',
        # "jewellery", "cameras", "hobbies", "pet", "home", "living", 
        # "wear", "sony", "men", "women", "toy",'phone',
        # "travel",'baby','new','sexy','gift','wash','apple',
        # 'fahion','bottle','summer','daily','chinese','switch',
        # 'liveroom','dog','cat',
        # 'door','coffee','sugar','clothes','tshirt','pen','glasses',
        # 'hat','water','music','accessories','girl','boy','tool',
        # 'electrical appliances','wine','whiskey','pants','pan',
        # 'canner','beer','cup','office','sock','biscuit','organic food','salt',
        # 'milk','oil','car','disposabre article','face','lipstick','cosmetic',
        # 'monitor','bed',
        #'galaxy','facial','outdoor',
        #'football', 'banana','orange', 'strawberry','kitchen',
        # 'crisp','tv','decoration','air','jucie', 'mask', 
        'movie','laptop','seat',
        'beaf','chicken','icecream',
        'bathroom', 'bread','chocolate','paper',
        'nut','potato chips','tea',
    ]
    count = 3
    threads = []
    file_list = [cate_list.getFileName(name) for name in keyword_list]
    # file_list = ["cate_jucie_list.json"]
    step = len(file_list) / count
    for i in range(0, count - 1):
        t = threading.Thread(target=handleFile, 
            args=(file_list[step * i: step * (i + 1)], ))
        t.setDaemon(True)
        t.start()
        threads.append(t)
    t = threading.Thread(target=handleFile, 
        args=(file_list[step * (count - 1):], ))
    t.setDaemon(True)
    t.start()
    threads.append(t)

    for t in threads:
        t.join()