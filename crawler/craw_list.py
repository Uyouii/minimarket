import json
import os
import sys
# https://github.com/lthoangg/shopee-crawler
from shopee_crawler import Crawler
import cate_list

if __name__ == '__main__':

    crawler = Crawler()
    crawler.set_origin(origin="shopee.sg")

    # data = crawler.crawl_by_cat_url(cat_url='https://shopee.sg/Home-Appliances-cat.11027421')

    for search_word in cate_list.keyword_list:
        datas = []
        path = f"./productlist/cate_{search_word}_list.json"
        file = open(path, 'w')

        res = crawler.crawl_by_search(keyword=search_word)
        for p in res: 
            datas.append({
                'id': p['product_id'], 
                'name': p['product_name'], 
                'image': p['product_image'], 
                'link': p['product_link'].replace(' ', '-'),
                'shop_id': p['shop_id']
            })
        file.write(json.dumps(datas, indent=2))

