#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:Darkpot

import requests
import json
import time
#import csv

def reqWebSite():
    success = True
    while success:
        try:
        #请求git地址仓库接口，拉取全部的代码仓库中的项目地址
        
            #请替换你的git中的请求accesstoken
            headers = {"PRIVATE-TOKEN":"YOUR_ACCESSTOKEN"}
            git = []
            #range 中的最大数，取决于/api/v4/projects接口查询你的页数，per_page为每页显示条数，page参数为第几页
            for b in range(1,500):
                #请求的git api 地址要根据当前的git版本查看git api手册自行调整
                url = 'https://YOUR_GITLAB/api/v4/projects?simple=yes&per_page=50&page='+str(b)
                req = requests.get(url,headers=headers)
                response = req.json()
                for num in range(len(response)):
                    i=response[num]["http_url_to_repo"]
                    if i not in git:
                        git.append(i)
        
            '''
            可导出project列表到csv
            with open('git.csv', 'w') as f:
                writer = csv.writer(f)
                for val in git:
                    writer.writerow([val])
            '''
            #将爬取的git仓库地址逐一发送给cobra白盒扫描器进行扫描，/api/add 为添加扫描任务接口，status为查询任务状态接口
            url2 = 'http://127.0.0.1:8888/api/add'
            url3 = 'http://127.0.0.1:8888/api/status'
            headers2 = {"Content-Type":"application/json"}
            sids=[]
            #将扫描出有漏洞的任务id sid保存到如下文件
            file = r'/YOUR_Dircetory/git.txt'
            for giturl in git:
                # CoBRA 任务添加接口的参数配置，key需要在cobra目录中的config进行自定义配置；rule 为本次扫描启用的规则
                data = '{"key":"YOU_COBRA_KEY","target":"'+giturl+':master","rule": "cvi-130003,cvi-130004,cvi-130001,cvi-130002,cvi-130005,cvi-130006"}'
                req2 =requests.post(url2, data=data, headers=headers2)
                response2 = req2.text
                json_result2 = json.loads(response2)
                sid2 = json_result2["result"]["sid"]
                while 1:
                    time.sleep(3)
                    # 添加完任务后，每隔3s请求一次任务状态，查看是否完成
                    data2 =  '{"key":"YOU_COBRA_KEY","sid":"'+sid2+'"}' 
                    req3 = requests.post(url3, data=data2, headers=headers2)
                    response3 = req3.text
                    json_result3 = json.loads(response3)
                    print(json_result3)
                    status =json_result3["result"]["status"]
                    if status=='running':
                        continue
                    else:
                        #如果任务完成间隔60s，再查看下任务状态，因为cobra扫描结果生成需要时间，当任务状态第一次变成done时可能结果会全部显示为0，容易产生漏报。
                        time.sleep(60)
                        req4 = requests.post(url3, data=data2, headers=headers2)
                        response4 = req4.text
                        json_result4 = json.loads(response4)
                        #将查询状态响应中返回的高中低危漏洞个数进行比较，只要其中有一个大于0则记录下来
                        high=json_result4["result"]["statistic"]["high"]
                        medium=json_result4["result"]["statistic"]["medium"]
                        critical=json_result4["result"]["statistic"]["critical"]
                        low=json_result4["result"]["statistic"]["low"]
                        if high!=0:
                            sids.append(sid2)
                            with open(file, 'a+') as f:
                                f.write(sid2+'\n') 
                            break
                        elif medium!=0:
                            sids.append(sid2)
                            with open(file, 'a+') as f:
                                f.write(sid2+'\n')
                            break
                        elif critical!=0:
                            sids.append(sid2)
                            with open(file, 'a+') as f:
                                f.write(sid2+'\n')
                            break
                        elif low!=0:
                            sids.append(sid2)
                            with open(file, 'a+') as f:
                                f.write(sid2+'\n')
                            break
                        else:
                            break

            print(sids)


        except Exception as e:
            print("出现如下异常%s"%e)
        
	
reqWebSite()



	
