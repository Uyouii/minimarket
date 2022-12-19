import json
import os
from re import S
import sys
import threading
import time

import requests
import cate_list


def getData(id, shop_id):
    try:
        url = "https://shopee.sg/api/v4/item/get?itemid={}&shopid={}".format(id, shop_id)
        res = requests.get(url)
        data = json.loads(res.content)
        desc = data['data']['description'].encode('utf-8')
        cate_str = ''
        cate = data['data']['categories']
        if len(cate) >= 2:
            cate_str += cate[1]['display_name'].encode('utf-8')
        return cate_str, desc
    except Exception as e:
        print(e)
        return "",""
    

def handleFile(file_name):
    new_data_list = []
    with open('./productlist/{}'.format(file_name), 'r') as list_file:
        datas=list_file.read()
        product_list = json.loads(datas)
        for product in product_list:
            id = product['id']
            shop_id = product['shop_id']
            product['cate_str'], product['desc'] = getData(id, shop_id)
            if not product['cate_str']:
                continue
            product['name'] = product['name'].encode('utf-8')
            new_data_list.append(product)
            print("{}: {}".format(file_name, len(new_data_list)))
            # print(product)
            # time.sleep(0.01)
    with open('./complete_product/{}'.format(file_name), 'w') as new_file:
        new_file.write(json.dumps(new_data_list, indent=2))


if __name__ == '__main__':
    file_list = [cate_list.getFileName(name) for name in cate_list.keyword_list]
    # file_list = ["cate_snoy_list.json"]
    threads = []
    for file_name in file_list:
        t = threading.Thread(target=handleFile, args=(file_name, ))
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()