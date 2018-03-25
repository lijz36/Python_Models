#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
import gevent
from gevent import monkey
monkey.patch_all()


def createScoketTCPServer(host, port, lis):
    ADDR = (host, port)
    sockfd = socket(AF_INET, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(lis)
    return sockfd


def createScoketTCPClient(host, port):
    ADDR = (host, port)
    sockfd = socket(AF_INET, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    return sockfd


def createScoketUDPServer(host, port):
    ADDR = (host, port)
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    return sockfd


def createScoketUdPClient(host, port):
    ADDR = (host, port)
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return sockfd


def createBroadcastServer(host, port):
    ADDR = (host, port)
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    return sockfd


def createBroadcastClient(host, port):
    ADDR = (host, port)
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sockfd.bind(ADDR)
    return sockfd


class my_gevent(object):
    """通过协程实现服务端程序"""
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def accept(self):
        while True:
            try:
                connfd, addr = self.sockfd.accept()
                gevent.spawn(self.handler, connfd)
            except Exception as e:
                print(e)
        self.sockfd.close()

    def handler(self, connfd):
         try:
            while True:
                data = connfd.recv(2048).decode()
                if not data:
                    break
                print(data)
                connfd.send(ctime().encode())
        except Exception as e:
            print(e)
        finally:
            connfd.close()



