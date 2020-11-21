print('importing...')
import tkinter as tk
import pickle
from myxml import *
from moretk import *
import sys
from PIL import Image as PIL_Image, ImageTk
from os.path import isfile
from os import system as cmd
from friendly_time import friendlyTime
import textwrap

print('loading...')
def main():
    print('MAIN')
    global selected_post_index, pyq, root, menu, frame
    with open('pyq.list', 'rb') as f:
        pyq = pickle.load(f)
    selected_post_index = 0
    
    root=tk.Tk()
    root.geometry('1300x600')
    menu = tk.Menu(root)
    root.config(menu = menu)
    menu.add_command(label='Go to...', command=goTo)
    menu.add_command(label='Previous', command=prevPost)
    menu.add_command(label='Next', command=nextPost)
    menu.add_command(label='Likes & Comments', command=likesAndComs)
    menu.add_command(label='Big Text', command=bigCopyableText)
    menu.ephermeral = []
    frame = tk.Frame(root, bg='yellow')
    
    showPost()
    root.mainloop()

def error(msg):
    global root
    root.destroy()
    inputbox('Error',msg)
    sys.exit(1)

def showPost():
    global root, pyq, selected_post_index, frame, menu 
    post = pyq[selected_post_index]
    title = 'Post %d/%d ' % (selected_post_index, len(pyq))
    title += friendlyTime(post['timestamp'])+' '
    title += post['authorName']+' '
    like_count = len(post['likes'])
    if like_count>0:
        title += '♥ %d ' % like_count
    comment_count = len(post['comments'])
    if comment_count>0:
        title += 'Comment %d ' % comment_count
    root.title(title)
    
    # unload
    frame.destroy()
    while menu.ephermeral:
        menu.delete(menu.ephermeral.pop(0))
    
    # load
    frame = tk.Frame(root)
    makeStretcherParent(frame)
    frame.pack(fill = tk.BOTH,expand=True)
    e = ET.fromstring(post['rawXML'])
    style = int(e.find('ContentObject').find('contentStyle').text)
    if style == 1:
        menu.add_command(label = 'Big Picture', command = bigPicture)
        menu.ephermeral.append('Big Picture')
        e_mediaList = e.find('ContentObject').find('mediaList')
        image_num = len(e_mediaList)
        def makeArrange(image_num):
            if image_num == 1:
                temp = {0:(1,0,1,1),
                           1:(0,0,1,1)}
                col_num = 1
            elif image_num == 2:
                temp = {0:(2,0,1,1),
                           1:(0,0,1,1),
                           2:(1,0,1,1)}
                col_num = 2
            elif image_num == 3:
                temp = {0:(2,0,1,2),
                           1:(0,0,1,1),
                           2:(1,0,1,1),
                           3:(0,1,1,1)}
                col_num = 2
            elif image_num == 4:
                temp = {0:(2,0,1,2),
                           1:(0,0,1,1),
                           2:(1,0,1,1),
                           3:(0,1,1,1),
                           4:(1,1,1,1)}
                col_num = 2
            elif image_num == 5:
                temp = {0:(3,0,1,3),
                           1:(0,0,1,1),
                           2:(1,0,1,1),
                           3:(2,0,1,1),
                           4:(0,1,1,1),
                           5:(1,1,1,1)}
                col_num = 3
            elif image_num == 6:
                temp = {0:(3,0,1,3),
                           1:(0,0,1,1),
                           2:(1,0,1,1),
                           3:(2,0,1,1),
                           4:(0,1,1,1),
                           5:(1,1,1,1),
                           6:(2,1,1,1)}
                col_num = 3
            elif image_num == 7:
                temp = {0:(3,0,1,3),
                           1:(0,0,1,1),
                           2:(1,0,1,1),
                           3:(2,0,1,1),
                           4:(0,1,1,1),
                           5:(1,1,1,1),
                           6:(2,1,1,1),
                           7:(0,2,1,1)}
                col_num = 3
            elif image_num == 8:
                temp = {0:(3,0,1,3),
                           1:(0,0,1,1),
                           2:(1,0,1,1),
                           3:(2,0,1,1),
                           4:(0,1,1,1),
                           5:(1,1,1,1),
                           6:(2,1,1,1),
                           7:(0,2,1,1),
                           8:(1,2,1,1)}
                col_num = 3
            elif image_num == 9:
                temp = {0:(3,0,1,3),
                           1:(0,0,1,1),
                           2:(1,0,1,1),
                           3:(2,0,1,1),
                           4:(0,1,1,1),
                           5:(1,1,1,1),
                           6:(2,1,1,1),
                           7:(0,2,1,1),
                           8:(1,2,1,1),
                           9:(2,2,1,1)}
                col_num = 3
            else:
                raise AssertionError
            for i in temp:
                temp[i] = dict(zip(['column','row','columnspan','rowspan'],temp[i])) 
            return temp, col_num
        arrange, col_num = makeArrange(image_num)
        text = ToughText(frame, font='Times 15')
        text.insert(tk.END, indent(e.find('contentDesc').text))
        text.config(state=tk.DISABLED)
        text.grid(**arrange[0],sticky='wen')
        frame.grid_columnconfigure(arrange[0]['column'],
                                  weight=1, minsize = 0)
        for i in range(col_num):
            frame.grid_columnconfigure(i, weight = 1, 
                                      minsize = root.winfo_width()*0.7/(col_num))
        
        with open('Images/master.dict','rb') as f:
            master = pickle.load(f)
        for i, e_media in enumerate(e_mediaList):
            url = e_media.find('url').text
            try:
                id = str(master[url]) 
            except KeyError:
                error('No url in master: '+url)
            image_path = imagePath(id)
            stretchPicture = StretchPicture(frame,image_path) 
            stretchPicture.grid(**arrange[i+1])
    else:
        stretchMessage = StretchMessage(frame, fg='yellow', 
                                        font = 'Times 25', bg='black')
        stretchMessage.pack()
        stretchMessage.toughSetText(indent(e.find('contentDesc').text))
        if style == 2:
            pass # Do nothing. 
        elif style in (3, 5):
            if style == 3:
                StretchMessage(frame, text = '_ URL _').pack()
                menu.add_command(label = 'Cached', command = cached)
                menu.ephermeral.append('Cached')
            elif style == 5:
                StretchMessage(frame, text = '_ Video _').pack()
            title = e.find('ContentObject').find('title').text
            StretchMessage(frame, text = title, 
                           font = 'Times 25').pack()
            menu.add_command(label = 'Web', command = web)
            menu.ephermeral.append('Web')
        elif style == 4:
            menu.add_command(label = 'Web', command = web)
            menu.ephermeral.append('Web')
            menu.add_command(label = '_Play', command = play)
            menu.ephermeral.append('_Play')
            StretchMessage(frame, text = '_ Music _').pack()
            e_media = e.find('ContentObject').find('mediaList').find('media')
            app = e.find('appInfo').find('appName').text
            title = e_media.find('title').text
            author = e_media.find('description').text
            music_url = e_media.find('url').text
            thumb = e_media.find('thumb').text
            StretchMessage(frame, text = 'from '+app, fg='gray').pack()
            StretchMessage(frame, text = title, font = 'Times 25').pack()
            StretchMessage(frame, text = author, fg='gray').pack()
            with open('MusicThumbs/master.dict','rb') as f:
                master = pickle.load(f)
            id = str(master[thumb])
            image_path = thumbPath(id)
            StretchPicture(frame, image_path).pack()
        elif style == 15:
            menu.add_command(label = '_Play', command = bigVideo)
            menu.ephermeral.append('_Play')
            StretchMessage(frame, text = '_ Mini Video _').pack()
            e_media = e.find('ContentObject').find('mediaList').find('media')
            thumb = e_media.find('thumb').text
            with open('MiniVideoThumbs/master.dict','rb') as f:
                master = pickle.load(f)
            id = str(master[thumb])
            image_path = miniVideoThumbPath(id)
            StretchPicture(frame, image_path).pack()
        else:
            error('Unexpected style: %d' % style)

def imagePath(id):
    if isfile('Images/'+id+'.jpg'):
        return 'Images\\'+id+'.jpg'
    elif isfile('Images/'+id+'.png'):
        return 'Images\\'+id+'.png'
    else:
        error('No jpg or png found for master ID '+id)

def thumbPath(id):
    if isfile('MusicThumbs/'+id+'.jpg'):
        return 'MusicThumbs\\'+id+'.jpg'
    elif isfile('MusicThumbs/'+id+'.png'):
        return 'MusicThumbs\\'+id+'.png'
    else:
        error('No jpg or png found for master ID '+id)

def miniVideoThumbPath(id):
    if isfile('MiniVideoThumbs/'+id+'.jpg'):
        return 'MiniVideoThumbs\\'+id+'.jpg'
    elif isfile('MiniVideoThumbs/'+id+'.png'):
        return 'MiniVideoThumbs\\'+id+'.png'
    else:
        error('No jpg or png found for master ID '+id)

def goTo():
    global pyq, selected_post_index
    input = inputbox('Total = %d. Go to post: ' % len(pyq), selected_post_index)
    selected_post_index = int(input)
    showPost()

def prevPost():
    global selected_post_index
    if selected_post_index == 0:
        msgbox('No more. ')
    else:
        selected_post_index -= 1
        showPost()

def nextPost():
    global selected_post_index, pyq
    if selected_post_index == len(pyq)-1:
        msgbox('No more. ')
    else:
        selected_post_index += 1
        showPost()

def likesAndComs():
    global selected_post_index, pyq
    post = pyq[selected_post_index]
    likes = post['likes']
    comments = post['comments']
    tkLikes = tk.Tk()
    tkLikes.geometry('1000x650')
    tkLikes.update_idletasks()
    tkLikes.title('♥ & Comments')
    makeStretcherParent(tkLikes)
    
    tk.Label(tkLikes, text = '♥',fg='yellow',bg='black').pack()
    text=''
    for like in likes:
        text += like['userName'] + ', '
    text = text[:-2]
    stretchMessage = StretchMessage(tkLikes)
    stretchMessage.toughSetText(text)
    stretchMessage.pack()
    
    tk.Label(tkLikes, text = 'Comments',fg='yellow',bg='black').pack()
    for comment in comments:
        authorName = comment['authorName'] 
        content = comment['content']
        if 'toUserName' in comment:
            to_user = ' TO ' + comment['toUserName']
        else:
            to_user = ''
        head = authorName+to_user+': '
        text = ToughText(tkLikes, font = 'Times 20')
        height = 1 + bilingualStringLen(head+content, 20) // text.cget('width')
        text.config(height = height)
        text.insert(tk.END, head)
        text.tag_add('head', '1.0', '1.'+str(len(head)))
        text.tag_config('head', foreground='gray')
        text.insert(tk.END, content)
        text.pack()
    
    tkLikes.focus_force()
    tkLikes.mainloop()

def bigCopyableText():
    global selected_post_index, pyq
    post = pyq[selected_post_index]
    content = post['content']
    with open('temp.txt','w') as f:
        try:
            f.write(content)
        except:
            for i in content:
                try:
                    f.write(i)
                except:
                    f.write('?')
    cmd('start notepad temp.txt')

def bigPicture():
    global selected_post_index, pyq
    post = pyq[selected_post_index]
    e = ET.fromstring(post['rawXML'])
    e_mediaList = e.find('ContentObject').find('mediaList')
    with open('Images/master.dict','rb') as f:
        master = pickle.load(f)
    url = e_mediaList.find('media').find('url').text
    id = str(master[url])
    image_path = imagePath(id)
    cmd('start explorer ' + image_path)

def bigVideo():
    global selected_post_index, pyq
    post = pyq[selected_post_index]
    e = ET.fromstring(post['rawXML'])
    e_mediaList = e.find('ContentObject').find('mediaList')
    with open('MiniVideos/master.dict','rb') as f:
        master = pickle.load(f)
    url = e_mediaList.find('media').find('url').text
    id = master[url]
    image_path = 'MiniVideos\\%d.mp4' % id
    cmd('start explorer ' + image_path)

def web():
    global selected_post_index, pyq
    post = pyq[selected_post_index]
    e = ET.fromstring(post['rawXML'])
    url = e.find('ContentObject').find('contentUrl').text
    cmd('start explorer "' + url + '"')

def cached():
    global selected_post_index, pyq
    post = pyq[selected_post_index]
    e = ET.fromstring(post['rawXML'])
    url = e.find('ContentObject').find('contentUrl').text
    with open('WebPages/master.dict','rb') as f:
        master = pickle.load(f)
    try:
        id = master[url]
    except KeyError:
        error('URL not in master: '+url)
    path = 'WebPages\\%d.html' % id
    if isfile(path):
        cmd('start explorer ' + path)
    else:
        raise AssertionError

def play():
    global selected_post_index, pyq
    post = pyq[selected_post_index]
    e = ET.fromstring(post['rawXML'])
    url = e.find('ContentObject').find('mediaList').find('media').find('url').text
    cmd('start explorer "' + url + '"')

def indent(text):
    if text is None:
        return None
    if '\n' in text:
        return textwrap.indent(text, '    ')
    else:
        return text

main()
