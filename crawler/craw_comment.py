import json
import os
from re import S
import sys
import threading
import time

import requests
import cate_list


def getComment(id, shop_id):
    try:
        url = "https://shopee.sg/api/v2/item/get_ratings?filter=0&flag=1&itemid={}&limit=6&offset=0&shopid={}&type=0".format(id, shop_id)
        res = requests.get(url)
        data = json.loads(res.content)
        comment_data = {
            'id': id,
            'shop_id': shop_id,
            'comment_list': []
        }
        if not data['data']['ratings']:
            return {}
        for rate in data['data']['ratings']:
            author_shopid = rate['author_shopid']
            userid = rate['userid']
            comment = rate['comment'].encode('utf-8')
            comment_data['comment_list'].append({
                'user_id': userid,
                'author_shop_id': author_shopid,
                'comment': comment,
                'orderid': rate['orderid'], 
                'rateing_str': rate['rating_star']
            })
            if 'ItemRatingReply' in rate:
                reply_data = rate['ItemRatingReply']
                if not reply_data:
                    continue
                reply_comment = reply_data['comment'].encode('utf-8')
                comment_data['comment_list'][-1]['replay'] = {
                    'user_id': reply_data['userid'], 
                    'comment':reply_comment
                }
        return comment_data
    except Exception as e:
        print(e)
        return {}
    

def handleFile(file_name):
    comment_list = []
    with open('./productlist/{}'.format(file_name), 'r') as list_file:
        datas=list_file.read()
        product_list = json.loads(datas)
        for product in product_list:
            id = product['id']
            shop_id = product['shop_id']
            comment_data = getComment(id, shop_id)
            if not comment_data or not comment_data['comment_list']:
                print("{}: no comments".format(file_name))
                continue
            comment_list.append(comment_data)
            print("{}: {}".format(file_name, len(comment_list)))
            # time.sleep(0.01)
    with open('./comments/{}'.format(file_name), 'w') as new_file:
        new_file.write(json.dumps(comment_list, indent=2))


if __name__ == '__main__':
    keyword_list = ['automotive', 'baby', 'bed', 'bread', 'cameras', 
        'canner', 'chicken', 'computer', 'cosmetic', 'decoration', 
        'disposabre article', 'electrical appliances', 'face',
        'games', 'gift', 'hat', 'health', 'lipstick', 'milk', 'monitor', 
        'movie', 'oil', 'paper', 'pen', 'shoes', 'sports', 'tshirt', 'wear',
        'whiskey']
    file_list = [cate_list.getFileName(name) for name in keyword_list]
    # file_list = ["cate_jucie_list.json"]
    threads = []
    for file_name in file_list:
        t = threading.Thread(target=handleFile, args=(file_name, ))
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
