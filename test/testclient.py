# -*- coding: utf-8 -*

import logging
import random
import sys
import time
import requests
import json


def post(path, payload):
    # print("post, url: {0}, payload: {1}".format(path, payload))
    url = "http://127.0.0.1:8000{}".format(path)
    res = requests.post(url, json=payload)
    show_url = "curl -d '{0}' '{1}'".format(json.dumps(payload), url)
    print(show_url)
    return res.content


def login(username, password):
    path = "/auth/login/"
    payload = {"username": username, "password": password}
    return post(path, payload)


def getAuthData(username):
    res = login(username, "123456")
    user_auth_data = json.loads(res)
    return user_auth_data['user_id'], user_auth_data['session']


def register(username, password, avatar):
    path = "/auth/register/"
    payload = {"username": username, "password": password, "avatar": avatar}
    return post(path, payload)


def getProduct(username, product_id):
    user_id, session = getAuthData(username)
    path = "/product/id/{}/".format(product_id)
    payload = {"user_id": user_id, "session": session}
    return post(path, payload)


def getAllProduct(username, page_size=20, cur_page=0):
    user_id, session = getAuthData(username)
    path = "/product/all/"
    payload = {
        "user_id": user_id,
        "session": session,
        "page_size": page_size,
        "cur_page": cur_page
    }
    return post(path, payload)


def searchProductByName(username, name, page_size=20, cur_page=0):
    user_id, session = getAuthData(username)
    print("search by name {0}".format(name))
    path = "/product/searchname/"
    payload = {
        "user_id": user_id,
        "session": session,
        "name": name,
        "page_size": page_size,
        "cur_page": cur_page
    }
    return post(path, payload)


def searchProductByCate(username, cate, page_size=20, cur_page=0):
    user_id, session = getAuthData(username)
    print("search by cate {0}".format(cate))
    path = "/product/searchcate/"
    payload = {
        "user_id": user_id,
        "session": session,
        "cate": cate,
        "page_size": page_size,
        "cur_page": cur_page
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


def addComment(username, product_id, content, img=''):
    user_id, session = getAuthData(username)
    return innerAddComment(user_id, session, product_id, content, img)


def innerAddComment(user_id, session, product_id, content, img=''):
    product_id = int(product_id)
    path = "/comment/addcomment/"
    payload = {
        "user_id": user_id,
        "session": session,
        "product_id": product_id,
        "content": content,
        "resp_comment_id": 0,
        'img': img
    }
    return post(path, payload)


def randomAddComment(username, product_id, count):
    count = int(count)
    user_id, session = getAuthData(username)
    product_id = int(product_id)
    for i in range(count):
        comment = random.choice(data.COMMENTS)
        innerAddComment(user_id, session, product_id, comment)


def getCommentById(username, comment_id):
    user_id, session = getAuthData(username)
    comment_id = int(comment_id)
    path = "/comment/id/{}/".format(comment_id)
    payload = {"user_id": user_id, "session": session}
    return post(path, payload)


def getProductComment(username, product_id, page_size=20, cur_page=0):
    user_id, session = getAuthData(username)
    product_id = int(product_id)
    path = "/comment/productcomments/"
    payload = {
        "user_id": user_id,
        "session": session,
        "product_id": product_id,
        "page_size": page_size,
        "cur_page": cur_page,
    }
    return post(path, payload)


def getCommentResponse(username, comment_id, page_size=20, cur_page=0):
    user_id, session = getAuthData(username)
    comment_id = int(comment_id)
    path = "/comment/commentresponses/"
    payload = {
        "user_id": user_id,
        "session": session,
        "comment_id": comment_id,
        "page_size": page_size,
        "cur_page": cur_page,
    }
    return post(path, payload)


def printUsage():
    usage = [
        "login [username] [password]",
        "register [username] [password] [avatar]",
        "getallproduct [username] [pagesize=20] [curpage=0]",
        "getproduct [username] [productid]",
        "searchproductname [username] [searchname] [pagesize=20] [curpage=0]",
        "searchproductcate [username] [cate] [pagesize=20] [curpage=0]",
        "getproductcomment [username] [productid] [pagesize=20] [curpage=0]",
        "getcomment [username] [commentid]",
        "addcomment [username] [productid] [content]",
        "responsecomment [username] [commentid] [content]",
        "getcommentresponses [username] [commentid] [pagesize=20] [curpage=0]"
        # "randomaddcomment [username] [productid] [count]",
    ]
    for s in usage:
        print(s)
    sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] '
                        '[%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    action_func = {
        "login": (3, login),
        "register": (4, register),
        "getproduct": (3, getProduct),
        "getallproduct": (2, getAllProduct),
        "searchproductname": (3, searchProductByName),
        "searchproductcate": (3, searchProductByCate),
        "getcomment": (3, getCommentById),
        "addcomment": (4, addComment),
        "responsecomment": (4, responseComment),
        "randomaddcomment": (4, randomAddComment),
        "getproductcomment": (3, getProductComment),
        "getcommentresponses": (3, getCommentResponse),
    }

    args = sys.argv[1:]
    if not args:
        printUsage()

    action = args[0]
    if action not in action_func or len(args) < action_func[action][0]:
        printUsage()

    func = action_func[action][1]
    res = func(*args[1:])
    res_data = json.loads(res)
    print('\n' + json.dumps(res_data, indent=2))
