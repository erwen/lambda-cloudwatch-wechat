# cloudwatch集成微信报警
## 为什么做这次分享
传统的zabbix等监控可以集成微信，钉钉，短信等平台。cloudwatch默认只支持邮件告警，时效性比较低，今天要分享的就是cloudwatch如何集成第三方如微信、钉钉、等支持API操作的即时聊天软件，这次就以微信告警为例，相信大家参考这次分享，可以简单的集成其他的即时聊天平台。

如果企业自身的监控平台已经与第三方即时聊天软件结合，配合这次分享，可将所有的监控集成在一起，减少监控告警平台

## 这次分享所需的资源
* aws账号一个
    * cloudwatch
        * AWS自带的监控系统
    * SNS
        * AWS提供的发布/订阅消息收发服务，这次分享使用SNS将告警信息推送给lambda
    * lambda
        * 无需考虑服务器即可运行代码，只需按使用的计算时间付费，可以由AWS的服务触发运行。这次分享使用lambda接受SNS的触发，处理后将警报推送给微信


* 企业微信号一个
    * Agentid
    * Secret
    * 企业ID
    * 部门ID

## 监控数据流向图

## 分享中不包括的内容
企业微信号的注册、设置、信息的收集，网上已经有很多教程，这里就不详述了。

## 步骤
1. 配置SNS订阅
2. 配置lambda
3. 创建并上传lambda python代码
4. 创建警报进行报警测试

## 配置SNS订阅
登录aws账号，进入SNS服务，点击创建主题

![images](lambda-cloudwatch-wechat/image/SNS-topic.png)

## 配置lambda
1. 登录aws账号，进入lambda服务，点击创建函数，选择从头开始创作

![images](https://github.com/erwen/lambda-cloudwatch-wechat/blob/master/image/SNS-topic.png)
    
    * 名称和角色名称自定义
    * 角色选项选择，从模板创建新角色
    
2. 进入创建的函数页面，打开Designer选项卡，选中SNS选项，在配置触发器选项卡中，SNS主题选择之前创建的cloudwatch_alarms主题，点击右下角的添加，然后点击右上角的保存

![images](lambda-cloudwatch-wechat/image/lambdas-init.png)

3. 退回到lambda主页面，然后进入之前创建的函数，更改函数代码选项卡中的处理程序选项为cwToWechat.lambda_handler

![images](lambda-cloudwatch-wechat/image/lambda-function.png)

    * cwToWechat为我们后面python代码的入口文件名称
    * lambda_handler为我们使用lambda处理警报的代码函数名称
    * 具体使用方法可参考AWS官方lambda使用文档

## 创建并上传lambda python代码
1. 下载代码到本地
```shell
https://github.com/erwen/lambda-cloudwatch-wechat.git
```
2. 由于lambda的python环境只有一些标准的python模块，我们需要把附加的pytho模块和代码一起打包
3. 添加第三方模块，使用的第三方模块只有一个requests
```
pip install requests -t lambda-cloudwatch-wechat
```
4. 替换cwToWechat.py中的corpid,agentid,appsecret为自己的微信信息
5. 打包zip类型代码（不要打包主文件夹，只需打包其中自己写的代码和第三方模块）
6. 上传代码到lambda，打开aws页面中的lambda中的创建的函数，函数代码选项卡中的代码输入类型，选择上传.zip文件，点击保存

![images](lambda-cloudwatch-wechat/image/lambda-code-upload.png)

## 创建警报进行报警测试
1. 创建一个CPU使用率的警报

![images](lambda-cloudwatch-wechat/image/create-alarms.png)
    
    * 选择通知时，选择刚刚创建的SNS主题
