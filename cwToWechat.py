#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import print_function
from __future__ import unicode_literals
import json
import requests

corpid = '*********'
agentid = '***************'
appsecret = '*****************'
toparty = 1

token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret

def getObject(m, f):
    return m.get(f)
def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    null = 'null'
    m = eval(message)

    AlarmName = getObject(m, 'AlarmName')
    AlarmDescription = getObject(m, 'AlarmDescription')
    NewStateValue = getObject(m, 'NewStateValue')
    OldStateValue = getObject(m, 'OldStateValue')
    NewStateReason = getObject(m, 'NewStateReason')
    NewStateReason = getObject(m, 'NewStateReason')
    Trigger = getObject(m, 'Trigger')


    newMessage = 'AlarmName: ' + AlarmName + '\n' + '\n' \
                + 'AlarmDescription: ' + AlarmDescription + '\n' + '\n' \
                + 'NewStateValue: ' + NewStateValue + '\n' + '\n' \
                + 'OldStateValue: ' + OldStateValue + '\n'  + '\n' \
                + 'NewStateReason: ' + NewStateReason + '\n' + '\n' \
                + 'Trigger: ' + str(Trigger)
    
    print(newMessage)
    req=requests.get(token_url)
    accesstoken=req.json()['access_token']
    msgsend_url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken

    params={
        # "touser": touser,
       "toparty": toparty,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
                "content": newMessage
        },
        "safe":0
    }
    req=requests.post(msgsend_url, data=json.dumps(params))
