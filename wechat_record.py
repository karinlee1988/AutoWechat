#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/3 16:30
# @Author  : karinlee
# @FileName: wechat_record.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/weixin_43972976
# @github : https://github.com/karinlee1988/
# @gitee : https://gitee.com/karinlee/
# @Personal website : https://karinlee.cn/

"""
本模块用于自动记录微信收到的信息，自动回复并记录到csv文件中。
"""

import csv
import itchat
# from itchat.content import *
import time

# 自动记录群聊@我的信息，写入message.csv文档中。
# 封装好的装饰器，当接收到的消息是Text，即文字消息
# @itchat.msg_register('Text')
# 封装好的装饰器，当接收到的消息是[TEXT, PICTURE,SHARING,ATTACHMENT,VIDEO]
# 对于不同消息的类型，采取不同的处理方法
# from itchat.content import *
# ==================================itchat.content=======================================
# TEXT       = 'Text'
# MAP        = 'Map'
# CARD       = 'Card'
# NOTE       = 'Note'
# SHARING    = 'Sharing'
# PICTURE    = 'Picture'
# RECORDING  = VOICE = 'Recording'
# ATTACHMENT = 'Attachment'
# VIDEO      = 'Video'
# FRIENDS    = 'Friends'
# SYSTEM     = 'System'
#
# INCOME_MSG = [TEXT, MAP, CARD, NOTE, SHARING, PICTURE,
#     RECORDING, VOICE, ATTACHMENT, VIDEO, FRIENDS, SYSTEM]
# =======================================================================================
# 引入后可使用itchat.content里面的常量，但也可以不引入 直接用字符串注册
# @itchat.msg_register([TEXT, PICTURE,RECORDING,ATTACHMENT,SHARING,VIDEO])

# def record_txt(name,message):
#     with open (r"message.txt","a",encoding='utf8') as f:
#         f.write(u'%s,%s\n' %(name,message))

def record_csv(clock,group,name,message):
    """
    传入4个参数，写入csv文件的4列。
    每调用1次该函数，就写入1行。（即1行*4列）
    """

    # 创建文件对象
    with open(r'message.csv','a',newline='',encoding='utf-8') as f:
        # 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)
        # 写入文件
        csv_writer.writerow([clock,group,name,message])

def wechat_autorecord():
    @itchat.msg_register(['Text'])
    def text_autorecord(msg):
        """
        用于微信私聊自动记录

        """
        # 我们只需要记录文本文件
        # 普通文本
        if msg['Type'] == 'Text':
            reply_message =  msg['Text']

        # 当消息不是由自己发出的时候
        if not msg['FromUserName'] == my_user_name:
            # 发送一条提示给文件助手
            itchat.send_msg(u"[%s]\n收到 好友  @%s  的 %s\n" %
                            (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                             msg['User']['NickName'],
                             reply_message), toUserName='filehelper')
            record_csv(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                       "私聊",msg['User']['NickName'],reply_message)
            # 回复给好友
            return u'[自动回复]信息\n-> %s <-\n收到，已自动记录。' % (reply_message)

    # 在注册时增加isGroupChat=True将判定为群聊回复
    @itchat.msg_register('Text', isGroupChat=True)
    def groupchat_autorecord(msg):
        """
        用于微信群聊@我自动回复
        """
        if msg['Type'] == 'Text':
            reply_message = msg['Text']

        # 当消息不是由自己发出的时候
        if not msg['FromUserName'] == my_user_name:

            if msg['isAt']:
                # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
                itchat.send_msg(u"[%s]\n收到 群聊 [%s] 好友[%s] 的 %s\n" %
                                (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])), # 格式化时间
                                 msg['User']['NickName'],  # 群聊名称
                                 msg['ActualNickName'],   # 好友备注名
                                 reply_message), toUserName='filehelper')
                # 回复给好友
                # 调用record()函数进行记录
                record_csv(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                           msg['User']['NickName'],
                            msg['ActualNickName'],
                           reply_message.replace("@李加林",''))  # 记录时不需要把 @李加林  这个信息记录下去

                # 回复给好友
                return u'[自动回复]已自动记录。\n%s-> %s' % (msg['ActualNickName'],reply_message.replace("@李加林",''))
    #登录微信
    itchat.auto_login(hotReload=True)
    # 获取自己的user_name
    my_user_name = itchat.get_friends(update=True)[0]["UserName"]
    #开始运行
    itchat.run()

if __name__ == '__main__':
    wechat_autorecord()