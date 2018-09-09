#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# message = "{"AlarmName\":\"awsrds-app-High-DB-Connections\",\"AlarmDescription\":null,\"AWSAccountId\":\"123456789123\",\"NewStateValue\":\"ALARM\",\"NewStateReason\":\"Threshold Crossed: 1 datapoint (10.0) was greater than or equal to the threshold (10.0).\",\"StateChangeTime\":\"2016-07-24T22:05:19.737+0000\",\"Region\":\"US West - Oregon\",\"OldStateValue\":\"OK\",\"Trigger\":{\"MetricName\":\"DatabaseConnections\",\"Namespace\":\"AWS/RDS\",\"Statistic\":\"AVERAGE\",\"Unit\":null,\"Dimensions\":[{\"name\":\"DBInstanceIdentifier\",\"value\":\"app\"}],\"Period\":300,\"EvaluationPeriods\":1,\"ComparisonOperator\":\"GreaterThanOrEqualToThreshold\",\"Threshold\":10.0}}"
from __future__ import print_function
from __future__ import unicode_literals
import json
import requests

corpid = 'wx8f478645fdb0c08b'
agentid = '1000002'
appsecret = 'venZ4be7f8ZIr80GrzXuUpLtdqWfml709zyTjqL6Qy4'

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
       "toparty": 1,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
                "content": newMessage
        },
        "safe":0
    }
    req=requests.post(msgsend_url, data=json.dumps(params))