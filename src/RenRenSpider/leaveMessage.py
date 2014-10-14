#! /usr/bin/env python
#coding:utf-8
'''
date:        2014/10/6
brief：            从网页抓取图片，之后保存到excel表格
author:      fish
'''

import re
import sys
import requests
import time
from _codecs import decode

from config import *
from login import login
from visit import getFriends

reload(sys)
sys.setdefaultencoding('utf-8')

def gossip(s, fDict):

    #用wireshark得知request URI是下面这个网址
    gossipUrl = 'http://gossip.renren.com/gossip.do'

    DefaultGossipText = '''    
                            Hello, I am a Web Robot made by Brother Ye, this is
                            created automatically!(\347\246\205\345\270\210)
                        '''
    
    name = raw_input('Input the name:')
    name = name.decode('utf-8')
    gossipText = raw_input('Input the message(\'Enter\' to use Default msg):')
    
    if '' == gossipText:
        gossipText = DefaultGossipText

    id = fDict[name][1]

    profileUrl = 'http://www.renren.com/'+ id +'/profile'
    
    res = s.get(profileUrl)   
     
    file = res.text.encode('utf-8') 
    reInfo = re.compile(r"get_check:'(.*?)',get_check_x:'(.*?)'", re.DOTALL)  
    info = reInfo.findall(file)  
    
    with open(tmpDir + 'friendProfile.txt','w+') as f: 
        f.write(file)  
        f.close()        
    
    tok  = info[0][0]  
    rtk  = info[0][1]
    
    gossipData = {'body'            : gossipText, 
                  'only_to_me'      : '0',
                  'from'            : 'main',
                  'id'              : '263045375',  
                  'cc'              : '263045375',
                  'ak'              : 'be884f0d474eb8987011136ad0c447dd',
                  'profilever'      : '2008',
                  'ref'             : profileUrl,
                  'requestToken'    : tok,  
                  '_rtk'            : rtk,
                  'color'           : ''          
                  }
  
    res=s.post(gossipUrl, gossipData)
    print 'Leave message to \"' + name + '\"success!'
    print 'Message： ' +  gossipText   

def gossipAct():
    #1.登陆
    (hostId, s, fDict) = login()
    
    #2.获取朋友列表 
    fDict = getFriends(s, fDict)
    
    #3.留言
    gossip(s, fDict)      

def main():
    gossipAct()

if __name__ == '__main__':   
    main()