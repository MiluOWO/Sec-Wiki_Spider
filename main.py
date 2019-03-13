import requests
from lxml import etree
import time
tags = ['[文档]', '[Web安全]','[其它]', '[事件]', '[设备安全]', '[数据挖掘]', '[观点]', '[爆库]', '[视频]', '[杂志]', '[渗透测试]', '[漏洞分析]', '[恶意分析]', '[移动安全]', '[书籍]', '[逆向分析]', '[新闻]', '[法规]', '[运维安全]', '[会议]', '[取证分析]', '[编程技术]', '[无线安全]', '[比赛]', '[人物]', '[工具]', '[论文]']
def queryNew():
    MainSiteUrl = 'https://sec-wiki.com/'
    r = requests.get(MainSiteUrl)
    Match_result = etree.HTML(r.text).xpath('//*[@id="content"]/div/div[2]/div[5]/div/p[1]/a/@href')[0]
    digital = int(Match_result[8:])
    return digital

def getArticle(num,tag):
    url = 'https://sec-wiki.com/weekly/%d' % num
    r = requests.get(url)
    r.encoding = 'utf-8'
    weekly = etree.HTML(r.text).xpath('//*[@id="news"]//*[@class="single"]')
    dic = {}
    for i in weekly:
        if (i is not None):
            if (tag in str(i[0].text)):
                dic[i[0].tail]=i[2].text
                #print(i[0].tail, i[2].text)
                '''
                #用于在同一行输出(后续输入覆盖原始数据)，娱乐向
                print('第%d期'%num,i[0].tail, i[2].text,end=" ")  # tail  用于取不到内容的地方(比如两个/, <br>前面)
                time.sleep(1)
                print('\r',end='')
                '''
            else:
                pass
    return dic

def WriteFile(dic):
    with open('Output.html','w',encoding='utf-8') as f:
        f.write('''
        <!DOCTYPE html>
<html>
<head>
	<title>Sec-Wiki</title>
    <link type="text/css" rel="stylesheet" href="source.css">
    <meta charset="UTF-8">
</head>
<body>
        ''')
        for Num,Content in dic.items():
            f.write('<h1>'+'第%s期'%Num+'</h1>')
            for key,value in Content.items():
                f.write('<p>')
                f.write(key+':'+'<a href="'+value+'">点我跳转</a>')
                f.write('</p>')
            f.write('''
                </body>
                </html>
            ''')
def init(tag,startNum):
    dic ={}
    digital = queryNew()
    for i in range(startNum,digital+1):  #设置从哪期开始爬取
        print('-----第%d期-----'%i)
        dic[str(i)]=getArticle(i,tag)
    with open('Renew.txt','w') as f:
        f.write(str(digital))
    WriteFile(dic)
    return dic

def renew():
    with open('Renew.txt','r') as f:
        old = int(f.read())
    new = queryNew()
    if (new>int(old)):
        for i in range(old+1,new+1):
            getArticle(i)

def GetTags():
    tags = set()
    digital = queryNew()
    for i in range(0,digital+1):
        url = 'https://sec-wiki.com/weekly/%d' % i
        r = requests.get(url)
        r.encoding = 'utf-8'
        weekly = etree.HTML(r.text).xpath('//*[@id="news"]//*[@class="single"]')
        for j in weekly:
            if (j is not None):
                tags.add(str(j[0].text).replace('\xa0',''))
    print(tags)




if __name__=="__main__":
    dic = {}
    print('请选择需要爬取的类别，输入序号即可')
    for i,j in enumerate(tags):
        print('[%d]%s'%(i,j),end=' ')
    print()
    tag=tags[int(input())]
    print('请选择从第几期开始爬取，默认从0开始')
    startNum = input()
    if(startNum==''):
        print('你选择的是%s,从第0期开始爬取,正在爬取请等待...' % (tag))
        dic=init(tag,0)
    else:
        print('你选择的是%s,从第%s期开始爬取,正在爬取请等待...' % (tag,startNum))
        dic=init(tag,int(startNum))
    print(dic)
    #GetTags()

#xml_learn https://www.jianshu.com/p/e084c2b2b66d
#requests 编码 r.encoding='utf-8'