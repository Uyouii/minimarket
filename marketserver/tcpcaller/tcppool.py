# -*- coding: utf-8 -*

import json
import logging
import random
import re
import select
import socket
import struct
import threading
import time
import uuid

from common import conf
from common import utils


class TcpPool():
    __metaclass__ = utils.SingletonType

    def __init__(self):
        self.socktes = {}  # key: sock, value: buffer
        self.resps = {}  # key: request_id, value: {event, msg}
        self.recv_thread = None
        self.running = False
        self.socktes_lock = threading.Lock()
        self.resps_lock = threading.Lock()
        self.running_lock = threading.Lock()
        self.__start()
        self.reconn_thread = None


    def __start(self):
        with self.running_lock:
            if self.running:
                return
            self.__connectToServer(conf.TCP_CONN_COUNT)
            logging.info("tcp pool started")

            self.running = True

            self.recv_thread = threading.Thread(target=self.__run)
            self.recv_thread.setDaemon(True)
            self.recv_thread.start()

            self.reconn_thread = threading.Thread(target=self.__reconn)
            self.reconn_thread.setDaemon(True)
            self.reconn_thread.start()

    def __del__(self):
        self.stop()
    
    def restart(self):
        self.stop()
        self.__start()

    def stop(self):
        with self.running_lock:
            self.__stopThread(self.recv_thread)
            self.__stopThread(self.reconn_thread)
            self.recv_thread = None
            self.reconn_thread = None
            self.running = False
            self.__clearSocket()
            self.resps = {}

    # request_id + threading.event sync get rpc result
    def call(self, req_data):
        request_id = str(uuid.uuid1())

        event = threading.Event()
        self.__registerRequest(request_id, event)
        req_data['request_id'] = request_id

        if self.__send(json.dumps(req_data)) != 0:
            return {}
    
        event.wait(conf.TCP_RPC_EVENT_TIMEOUT) # timeout
        resp_data = self.__popResponse(request_id)
        resp_data.pop('request_id', None)

        return resp_data
    
    def __stopThread(self, thread):
        if thread:
            thread.stop()

    def __addSocket(self, sock):
        with self.socktes_lock:
            self.socktes[sock] = ''

    def __delSocket(self, sock):
        with self.socktes_lock:
            self.socktes.pop(sock, None)

    def __clearSocket(self):
        with self.socktes_lock:
            for s in self.socktes:
                s.close()
            self.socktes = {}

    def __registerRequest(self, request_id, event):
        with self.resps_lock:
            self.resps[request_id] = {'event': event, 'data': None}

    def __addResponse(self, request_id, data):
        with self.resps_lock:
            if request_id in self.resps:
                self.resps[request_id]['data'] = data
                self.resps[request_id]['event'].set()  # set event

    def __popResponse(self, request_id):
        data = None
        with self.resps_lock:
            if request_id not in self.resps:
                return data
            data = self.resps[request_id]['data']
            self.resps.pop(request_id)
        return data

    def __reconn(self):
        # 尝试重连一下
        while self.running:
            time.sleep(conf.TCP_RECONNECT_TIME)
            if len(self.socktes) < conf.TCP_CONN_COUNT:
                self.__connectToServer(conf.TCP_CONN_COUNT - len(self.socktes))

    def __connectToServer(self, count):
        threads = []
        for i in range(count):
            t = threading.Thread(target=self.__connServer)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def __connServer(self):
        sock = socket.socket()
        try:
            sock.connect((conf.TCP_SERVER_ADDR, conf.TCP_SERVER_PORT))
        except socket.error as msg:
            logging.error("connect failed: {}".format(msg))
        else:
            logging.info("sockconnect succees {}".format(sock.getsockname()))
            self.__addSocket(sock)
    
    def __getListenSocks(self):
        with self.socktes_lock:
            return [s for s in self.socktes]

    def __run(self):
        while self.running:
            socket_list = self.__getListenSocks()

            rlist, _, elist = select.select(socket_list, [], [], 1)

            for s in rlist:
                recv_data = s.recv(conf.TCP_RECV_BUFF_LEN)
                if recv_data != '':
                    logging.info("recv data: {}".format(recv_data))
                    self.__handleRespData(s, recv_data)
                else:
                    logging.error("{} closed".format(s.getsockname()))
                    if s in socket_list:
                        self.__delSocket(s)

            for s in elist:
                logging.error('exception condition on {}'.format(s.getsockname()))
                self.__delSocket(s)
                s.close()
    
    # TODO: 可以轮询发送
    def __getRandomSocket(self):
        client_idx = random.randint(0, len(self.socktes) - 1)
        with self.socktes_lock:
            return self.socktes.keys()[client_idx]

    def __send(self, msg):
        if not self.socktes:
            logging.error('send failed, no valid socket')
            return -1
        msg_len = len(msg)
        len_buf = struct.pack('>I', msg_len)
        sock = self.__getRandomSocket()
        sock.send(len_buf + msg)
        return 0

    def __handleRespData(self, s, data):

        recv_buffer = self.socktes[s]
        recv_buffer += data

        while len(recv_buffer) > 4:
            data_len = struct.unpack('>I', recv_buffer[:4])[0]

            if len(recv_buffer) < 4 + data_len:
                break
            
            msg = recv_buffer[4:4 + data_len]
            recv_buffer = recv_buffer[4 + data_len:]
            logging.info("msg: {}".format(msg))
            
            try:
                data = json.loads(msg)
                request_id = data.get('request_id')
                if request_id:
                    self.__addResponse(request_id, data)
            except json.decoder.JSONDecodeError as e:
                logging.error("loadresponse invalid data: {}".format(data))
        
        if len(self.socktes[s]) != len(recv_buffer):
            self.socktes[s] = recv_buffer

