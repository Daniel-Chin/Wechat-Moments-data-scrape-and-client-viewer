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
    
    post_3=[]
    for post in pyq:
        xml=post['rawXML']
        root=ET.fromstring(xml)
        if root.find('ContentObject').find('contentStyle').text == '3':
            post_3.append(post)
            #===================================================================
            # pprint(post)
            # display(ET.fromstring(post['rawXML']),False)
            # input()
            #===================================================================
    
    cd('webpages')
    list_url=[]
    for post in post_3:
        root=ET.fromstring(post['rawXML'])
        list_url.append(root.find('ContentObject').find('contentUrl').text)
        
    master={}
    counter=0
    jdt_=jdt.CommJdt(len(list_url)//8+1)
    pool=dummy.Pool()
    for i in range(len(list_url)//8):
        jdt_.update(i)
        try:
            list_r=pool.map(requests.get,list_url[i*8:i*8+8])
        except:
            list_r=[]
            for ii in range(8):
                try:
                    list_r.append(requests.get(list_url[i*8+ii]))
                except:
                    #===========================================================
                    # print('\n',list_url[i*8+ii])
                    #===========================================================
                    list_r.append(-1)
        for r in list_r:
            if r==-1:
                counter+=1
            else:
                ext='html'
                with open(str(counter)+'.'+ext,'wb') as f:
                    f.write(r.content)
                master[list_url[counter]]=counter
                counter+=1
    for i in range((len(list_url)//8)*8,len(list_url)):
        r=requests.get(list_url[i])
        ext='html'
        with open(str(counter)+'.'+ext,'wb') as f:
            f.write(r.content)
        master[list_url[counter]]=counter
        counter+=1
    jdt_.complete()
    print(counter, len(list_url))

    with open('master.dict','wb') as f:
        pickle.dump(master,f)

main()
input('end')
sys.exit(0)
