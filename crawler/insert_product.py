
# -*- coding: utf-8 -*
import json
import threading
import requests
import cate_list


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

def handleFile(file_name_list):
    count = 0
    for file_name in file_name_list:
        try:
            with open('./complete_product/{}'.format(file_name), 'r') as list_file:
                datas=list_file.read()
                product_list = json.loads(datas)
                for product in product_list:
                    data = {
                        'product_id':  product['id'],
                        'product_name': product['name'],
                        'product_cate':  product['cate_str'], 
                        'product_img': product['image'],
                        'product_desc': product['desc'].encode('utf-8'),
                    }

                    res = post("/product/add/", data)
                    count += 1
                    print("{} {}".format(file_name, count))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    keyword_list = [
        # 'phone', 'dress', 'health', 'kids', 'games', 'books', 
        # 'computer','food', 'sports', 'watches', 'shoes','automotive',
        # "jewellery", "cameras", "hobbies", "pet", "home", "living", 
        # "wear", "sony", "men", "women", "toy",'phone',
        # "travel",'baby','new','sexy','gift','wash','apple',
        'fahion','bottle','summer','daily','chinese','switch',
        'galaxy','facial','outdoor','movie','laptop','seat',
        'beaf','chicken','icecream','football','banana','orange',
        'strawberry','kitchen','bathroom','liveroom','dog','cat',
        'door','coffee','sugar','clothes','tshirt','pen','glasses',
        'hat','water','music','accessories','girl','boy','tool',
        'electrical appliances','wine','whiskey','pants','pan',
        'canner','beer','cup','office','sock','biscuit','organic food','salt',
        'milk','oil','car','disposabre article','face','lipstick','cosmetic',
        'monitor','bed','bread','chocolate','paper','crisp','tv','decoration',
        'air','jucie','mask','nut','potato chips','tea',
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