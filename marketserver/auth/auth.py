# -*- coding: utf-8 -*
import json
import re
import time
import logging
from django.http import HttpResponse
from tcpcaller import tcppool
from cache.rediscache import RedisCache
from common import conf
from common import utils


def userRegister(request):
    logging.info("recv data: {0}".format(request.body))

    errcode, req_data = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))

    if not req_data.get('username') or not req_data.get('password'):
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({"errcode": errcode}))
    
    req_data['action'] = conf.AUTH_ACTION_REGISTER

    user_data = tcppool.TcpPool().call(req_data)
    
    if user_data.get("errcode") == 0:
        RedisCache().delete(user_data['user_id'])
    
    return HttpResponse(json.dumps(user_data))


def userLogin(request):
    logging.info("recv data: {0}".format(request.body))

    errcode, req_data = utils.loadRequest(request.body)
    if errcode != 0:
        return HttpResponse(json.dumps({'errcode': errcode}))
    
    if not req_data.get('username') or not req_data.get('password'):
        errcode = conf.ERR_INVALID_REQUEST
        return HttpResponse(json.dumps({"errcode": errcode}))

    req_data['action'] = conf.AUTH_ACTION_LOGIN

    user_data = tcppool.TcpPool().call(req_data)

    if user_data.get("errcode") == 0:
        RedisCache().delete(user_data['user_id'])

    return HttpResponse(json.dumps(user_data))

def checkSessionFromReq(req):
    user_id = req.get('user_id')
    session = req.get('session')
    if not user_id or not session:
        return conf.ERR_INVALID_REQUEST
    return checkUserSession(user_id, session)

"""
Parameters:
    user_id: int64 用户id
    session: string 校验的session
Returns:
    int, 0: 校验通过, other: 校验失败
"""
def checkUserSession(user_id, session):
    if not user_id or not session:
        return conf.ERR_INVALID_REQUEST
    
    cache = RedisCache()
    user_data = cache.get(user_id)
    curtime = int(time.time())

    # 先尝试从cache拉去判断
    if user_data is not None:
        if user_data["status"] != conf.AUTH_USER_STATUS_OK:
            return conf.STATUS_TO_ERRCODE_DICT[user_data["status"]]
        
        logintime = user_data.get('logintime', 0)
        if curtime - logintime > conf.AUTH_SESSION_TIMEOUT:
            logging.error("session timeout, cachedata: %s" % user_data)
            return conf.ERR_SESSION_TIMEOUT
        
        cache_session = user_data.get('session')
        if cache_session and cache_session != session:
            return conf.ERR_WROING_SESSION
        else:
            logging.info("check session in cache:ok")
            return conf.ERR_OK

    # cache中无缓存的session, 则从mysql获取session, 并将状态缓存到cache
    pool = tcppool.TcpPool()
    req_data = {
        "action": conf.AUTH_GET_USER_INFO,
        "user_id": user_id,
        "session": session
    }
    user_data = pool.call(req_data)

    errcode = user_data.get('errcode', -1)
    if errcode == 0:
        if not user_data['session']:
            user_data['status'] = conf.AUTH_USER_STATUS_NOT_LOGIN
        elif curtime - user_data['logintime'] > conf.AUTH_SESSION_TIMEOUT:
            user_data['status'] = conf.AUTH_USER_STATUS_TIME_OUT
        else:
            user_data['status'] = conf.AUTH_USER_STATUS_OK
        res = conf.STATUS_TO_ERRCODE_DICT[user_data["status"]]
    elif errcode == conf.ERR_USER_NOT_EXISTS:
        user_data['id'] = user_id
        user_data['status'] = conf.AUTH_USER_STATUS_NOT_REGISTER
        res = conf.ERR_USER_NOT_RESISTER
    else:
        res = conf.ERR_UNKNOWN_ERROR

    RedisCache().set(user_id, user_data, conf.AUTH_SESSION_TIMEOUT)

    if res != conf.ERR_OK:
        logging.error("check session failed, errcode: {0}, user_id: {1}, "
                      "session: {2}".format(res, user_id, session))
    else:
        logging.info("check session succ, user_id: {0}, session: {1}"
                     .format(user_id, session))

    return res
