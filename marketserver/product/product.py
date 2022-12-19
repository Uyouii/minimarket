# -*- coding: utf-8 -*

import json
import logging
import time
from django.http import HttpResponse
from common import conf, utils
from auth import auth
from models import Product
import traceback

def getProductByIdApi(request, product_id):
    logging.info("request: id: {}, data: {}".format(
        product_id, request.body))
    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    errcode, product_data = getProductById(product_id)
    resp = {'errcode': errcode}
    if errcode == 0:
        resp['product_data'] = product_data
    return HttpResponse(json.dumps(resp))

def getProductById(product_id):
    errcode = 0
    try:
        res = Product.objects.get(id=product_id)
    except Product.DoesNotExist as e:
        errcode = conf.ERR_DATA_NOT_EXISTS
        logging.info("getProductById failed {}, product_id: {} "
                     "no exists".format(e, product_id))

    data = res.getDict() if errcode == 0 else {}

    return errcode, data

def getAllProductApi(request):
    logging.info("request: {}".format(request.body))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))

    page_size = int(req.get('page_size', 20))
    cur_page = int(req.get('cur_page', 0))

    errcode, product_list = getAllProduct(page_size, cur_page)

    resp = {'errcode': errcode, 'product_list': product_list}
    return HttpResponse(json.dumps(resp))

def getAllProduct(page_size, cur_page):
    res = Product.objects.values('id', 'name', 'cate', 'photo')[
        cur_page * page_size:(cur_page + 1) * page_size]

    product_list = [p for p in res]
    return 0, product_list

def searchProductByName(name, page_size, cur_page):
    # 支持查询前缀分词
    search_word_list = name.split()
    searchname = ' '.join(["{}*".format(word) for word in search_word_list])

    res = Product.objects.values('id', 'name', 'cate', 'photo').filter(
        name__search=searchname)[
        cur_page * page_size:(cur_page + 1) * page_size]

    product_list = [p for p in res]
    return 0, product_list

def searchProductByNameApi(request):
    logging.info("request: {}".format(request.body))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))

    name = req.get('name', '').strip()
    if not name:
        return getAllProduct(request)

    page_size = int(req.get('page_size', 20))
    cur_page = int(req.get('cur_page', 0))

    errorcode, product_list = searchProductByName(name, page_size, cur_page)

    resp = {'errcode': errorcode, 'product_list': product_list}
    return HttpResponse(json.dumps(resp))

def searchProductByCate(cate, page_size, cur_page):
    search_word_list = cate.split()
    searchname = ' '.join(["{}*".format(word) for word in search_word_list])

    res = Product.objects.values('id', 'name', 'cate', 'photo').filter(
        cate__search=searchname)[cur_page * page_size:(cur_page + 1) * page_size]

    product_list = [p for p in res]
    return 0, product_list


def searchProductByCateApi(request):
    logging.info("request: {}".format(request.body))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    cate = req.get('cate', '').strip()
    if not cate:
        return getAllProduct(request)

    page_size = int(req.get('page_size', 20))
    cur_page = int(req.get('cur_page', 0))

    errcode, product_list = searchProductByCate(cate, page_size, cur_page)

    resp = {'errcode': errcode, 'product_list': product_list}
    return HttpResponse(json.dumps(resp))

# for test
def addProductApi(request):
    logging.info("request: {}".format(request.body))
    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))
    
    product_id = req.get('product_id', '')
    product_name = req.get('product_name', '').strip()
    product_cate = req.get('product_cate', '').strip()
    product_img = req.get('product_img', '')
    product_desc = req.get('product_desc', '').strip()
    if not product_id or not product_name or not product_cate:
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({'errcode': errcode}))
    
    errcode, product = addProduct(product_id, product_name, product_cate,
        product_desc, product_img)
    
    resp = {
        'errcode': errcode,
        'product_data': product
    }
    
    return HttpResponse(json.dumps(resp))


def addProduct(product_id, product_name, product_cate, 
    product_desc = '', product_img = ''):
    cur_time = int(time.time() * 1000)
    
    product = Product(
        id= product_id,
        name= product_name[:128],
        cate= product_cate[:32],
        create_time = cur_time,
        update_time=cur_time,
        descript = product_desc[:2048],
        photo=product_img
    )
    # insert to mysql
    product.save()
    return 0, product.getDict()
