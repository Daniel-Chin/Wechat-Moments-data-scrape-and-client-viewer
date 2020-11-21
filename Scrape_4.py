from myxml import *
from os import chdir as cd
import sys
import pickle
from pprint import pprint
import requests
import jdt
from multiprocessing import dummy

def main():
    with open('pyq.list','rb') as f:
        pyq = pickle.load(f)
    
    post_4=[]
    for post in pyq:
        xml=post['rawXML']
        root=ET.fromstring(xml)
        if root.find('ContentObject').find('contentStyle').text == '4':
            post_4.append(post)
            #===================================================================
            # pprint(post)
            # display(ET.fromstring(post['rawXML']),False)
            # input()
            #===================================================================
    
    cd('MusicThumbs')
    list_url=[]
    for post in post_4:
        root=ET.fromstring(post['rawXML'])
        list_url.append(root.find('ContentObject').find('mediaList').find('media').find('thumb').text)
    
    master={}
    counter=0
    jdt_=jdt.CommJdt(len(list_url)//4+1)
    pool=dummy.Pool()
    for i in range(len(list_url)//4):
        jdt_.update(i)
        list_r=pool.map(requests.get,list_url[i*4:i*4+4])
        for r in list_r:
            if 'jpeg' in r.headers['Content-Type']:
                ext='jpg'
            elif 'png' in r.headers['Content-Type']:
                ext='png'
            else:
                ext=input(r.headers['Content-Type'])
            with open(str(counter)+'.'+ext,'wb') as f:
                f.write(r.content)
            master[list_url[counter]]=counter
            counter+=1
    for i in range((len(list_url)//4)*4,len(list_url)):
        r=requests.get(list_url[i])
        if 'jpeg' in r.headers['Content-Type']:
            ext='jpg'
        elif 'png' in r.headers['Content-Type']:
            ext='png'
        else:
            ext=input(r.headers['Content-Type'])
        with open(str(counter)+'.'+ext,'wb') as f:
            f.write(r.content)
        master[list_url[counter]]=counter
        counter+=1
    jdt_.complete()
    if counter==len(list_url):
        print('GOOD')
    else:
        print(counter,len(list_url))

    with open('master.dict','wb') as f:
        pickle.dump(master,f)

main()
input('end')
sys.exit(0)
