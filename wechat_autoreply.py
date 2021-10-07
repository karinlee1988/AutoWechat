#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/2/1 15:46
# @Author : karinlee
# @FileName : wechat_autoreply.py
# @Software : PyCharm
# @Blog : https://blog.csdn.net/weixin_43972976
# @github : https://github.com/karinlee1988/
# @gitee : https://gitee.com/karinlee/
# @Personal website : https://karinlee.cn/

"""
本模块使用itchat库，实现微信消息自动收集并回复，群聊@我自动回复功能

"""

import itchat
# from itchat.content import *
import time

# 自动回复
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

def wechat_autoreply():
    @itchat.msg_register(['Text', 'Picture','Recording','Sharing','Attachment','Video'])
    def text_reply(msg):
        """
        用于微信私聊自动回复


        """
        # 对于不同类型的信息，我们要记录不同的内容来回复，
        # 普通文本
        if msg['Type'] == 'Text':
            reply_message = "信息: \n\n"  + msg['Text']

        # 图片，记录图片的名字，FileName这个键值可以表示图片，音频视频的名字
        elif msg['Type'] == 'Picture':
            reply_message = "：图片 -> " + msg['FileName']

        elif msg['Type'] == 'Recording':
            reply_message = "：语音 -> "

        elif msg['Type'] == 'Sharing':
            reply_message = "：分享链接 -> "

        elif msg['Type'] == 'Attachment':
            reply_message = "：文件 -> " + msg['FileName']

        elif msg['Type'] == 'Video':
            reply_message = "：视频 -> " + msg['FileName']

        else:
            reply_message = "：[信息]"

        # 当消息不是由自己发出的时候
        if not msg['FromUserName'] == my_user_name:
            # 发送一条提示给文件助手
            itchat.send_msg(u"[%s]\n收到 好友  @%s  的 %s\n" %
                            (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                             msg['User']['NickName'],
                             reply_message), toUserName='filehelper')
            # 回复给好友
            return u'[自动回复]本人微信目前处于python托管状态，您的消息已被自动记录。\n已经收到您的%s\n\n稍后我将回复您[微笑]' % (reply_message)

    # 在注册时增加isGroupChat=True将判定为群聊回复
    @itchat.msg_register('Text', isGroupChat=True)
    def groupchat_reply(msg):
        """
        用于微信群聊@我自动回复
        """
        if msg['Type'] == 'Text':
            reply_message = "信息 ： \n\n"  + msg['Text']

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
                return u'[自动回复]本人微信目前处于python托管状态，您@我的消息已被自动记录。\n已经收到您的%s\n\n稍后我将回复您[微笑]' % (reply_message)
    #登录微信
    itchat.auto_login(hotReload=True)
    # 获取自己的user_name
    my_user_name = itchat.get_friends(update=True)[0]["UserName"]
    #开始运行
    itchat.run()

if __name__ == '__main__':
    wechat_autoreply()