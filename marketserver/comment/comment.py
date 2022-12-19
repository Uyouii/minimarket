from cmath import log
import json
import logging
import re
import sys
import time
from django.http import HttpResponse
from common import conf, utils
from auth import auth
from models import Comment
import random
from product import product

'''
|-1bit-|---41bit mstime---|---15bit random num---|---7bit tableid---|
|---------------------------- 64 bit -------------------------------|
confim that can get same table id from product_id and commentid
'''
def GenCommentId(product_id):
    table_index = product_id % conf.COMMENT_TABLE_COUNT
    ms_time = int(time.time() * 1000) - conf.GEN_ID_BGEIN_MS_TIME
    random_num = random.randint(0, 0x3fff)
    comment_id = (ms_time << 22) + (random_num << 7) + table_index
    logging.info("gen comment id: {}".format(comment_id))
    return comment_id

def GetTableIndexFromCommentId(comment_id):
    return (int(comment_id) & 0x7f)

def addCommentToProductApi(request):
    logging.info("request: data: {}".format(request.body))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    user_id = req['user_id']
    product_id = req.get('product_id', 0)
    content = req.get('content', '').strip()
    img =  req.get('img', '')

    if not product_id or not content:
        logging.info("addCommentToProduct, invalid "
            "request: {}".format(request.body))
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({'errcode': errcode}))
    
    errcode, comment_data = addCommentToProduct(user_id, product_id,
        content, img)
    
    resp = {'errcode': 0}
    if errcode != 0:
        logging.error("addCommentToProductApi failed, errcoee: {0}," 
            "req: {1}".format(errcode, req))
        resp['errcode'] = errcode
    else:
        logging.info("addCommentToProduct succees: {}".format(comment_data))
        resp['comment_data'] = comment_data
    
    return HttpResponse(json.dumps(resp))


def addCommentToProduct(user_id, product_id, content, img = ''):
    errcode, _ = product.getProductById(product_id)
    if errcode != 0:
        logging.error("addCommentToProduct, product not exists,"
            "product_id: {0} ".format(product_id))
        return conf.ERR_INVALID_PRODUCT, {}

    comment_id = GenCommentId(product_id)
    commentModel = Comment.getModel(product_id % conf.COMMENT_TABLE_COUNT)
    cur_time = int(time.time() * 1000)
    
    comment = commentModel(
        id= comment_id,
        product_id= product_id,
        user_id= user_id,
        resp_comment_id= 0,
        content= content[:512],
        create_time= cur_time, 
        update_time= cur_time,
        img= img
    )
    # insert to mysql
    comment.save()
    return 0, comment.getDict()

def getProductCommentApi(request):
    logging.info("request data: {}".format(request.body))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))
    
    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    product_id = req.get('product_id', 0)
    page_size = int(req.get('page_size', 20))
    cur_page = int(req.get('cur_page', 0))

    if not product_id:
        logging.info("getProductCommentApi, invalid "
            "request: {}".format(request.body))
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({'errcode': errcode}))
    
    errcode, comment_list = getProductComment(product_id, page_size, cur_page)

    resp = {'errcode': errcode, 'comment_list': comment_list}
    return HttpResponse(json.dumps(resp))

def getProductComment(product_id, page_size, cur_page):

    commentModel = Comment.getModel(
        product_id % conf.COMMENT_TABLE_COUNT)

    res = commentModel.objects.values('id', 'user_id', 'content', 'create_time',
        'img').filter(product_id=product_id).order_by('-create_time')[
        cur_page * page_size:(cur_page + 1) * page_size]
    
    comment_list = [c for c in res]
    return 0,comment_list

def addResponseToCommentApi(request):
    logging.info("request data: {}".format(request.body))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    user_id = req['user_id']
    resp_comment_id = req.get('resp_comment_id', 0)
    content = req.get('content', '').strip()
    img =  req.get('img', '')

    if not resp_comment_id or not content:
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    errcode, comment_data = addResponseToComment(user_id, 
        resp_comment_id, content, img)

    resp = {'errcode': 0}

    if errcode != 0:
        logging.error("addResponseToCommentApi failed, errcoee: {0}," 
            "req: {1}".format(errcode, req))
        resp['errcode'] = errcode
    else:
        logging.info("addResponseToCommentApi succees: {}".format(comment_data))
        resp['comment_data'] = comment_data
    
    return HttpResponse(json.dumps(resp))

def addResponseToComment(user_id, resp_comment_id, 
        content, img = ''):
    
    errcode, resp_commend_data = getCommentById(resp_comment_id)
    if errcode != 0:
        logging.error("addResponseToCommentApi invlaid respcomment, "
        "req: {}".format(resp_comment_id))
        return errcode, {}

    product_id = resp_commend_data['product_id']

    comment_id = GenCommentId(product_id)
    commentModel = Comment.getModel(
        product_id % conf.COMMENT_TABLE_COUNT)
    cur_time = int(time.time() * 1000)
    
    comment = commentModel(
        id= comment_id,
        product_id= product_id,
        user_id= user_id,
        resp_comment_id= resp_comment_id,
        content=content[:512],
        create_time= cur_time, 
        update_time= cur_time,
        img= img
    )
    # insert to mysql
    comment.save()
    return 0, comment.getDict()

def getCommentById(comment_id):
    table_index = GetTableIndexFromCommentId(comment_id)
    commentModel = Comment.getModel(table_index)
    errcode = 0
    try:
        res = commentModel.objects.get(id=comment_id)
    except commentModel.DoesNotExist as e:
        errcode = conf.ERR_DATA_NOT_EXISTS
        logging.error("getCommentById failed {}, product_id: {} "
                     "no exists".format(e, comment_id))
    
    data = res.getDict() if errcode == 0 else {}
    return errcode, data

def getCommentByIdApi(request, comment_id):
    logging.info("request: id: {}, data: {}".format(
        comment_id, request.body))

    if not comment_id:
        logging.info("getCommentByIdApi, invalid "
            "request: {}, id: {}".format(request.body, comment_id))
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))

    errcode, comment_data = getCommentById(comment_id)
    resp = {'errcode': errcode}
    if errcode == 0:
        resp['comment_data'] = comment_data

    return HttpResponse(json.dumps(resp))

def getCommentResponseApi(request):
    logging.info("request data: {}".format(request.body))

    errcode, req = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    errcode = auth.checkSessionFromReq(req)
    if errcode != 0:
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    page_size = int(req.get('page_size', 20))
    cur_page = int(req.get('cur_page', 0))
    comment_id = req.get('comment_id', 0)
    if not comment_id:
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    errcode, comment_list = getCommentResponse(comment_id, page_size, cur_page)
    resp = {'errcode': errcode, 'comment_list': comment_list}
    return HttpResponse(json.dumps(resp))
    

def getCommentResponse(comment_id, page_size, cur_page):
    commentModel = Comment.getModel(GetTableIndexFromCommentId(comment_id))

    res = commentModel.objects.values('id', 'user_id', 'content', 'create_time',
        'img').filter(resp_comment_id=comment_id).order_by('-create_time')[
        cur_page * page_size:(cur_page + 1) * page_size]
    
    comment_list = [c for c in res]
    return 0,comment_list