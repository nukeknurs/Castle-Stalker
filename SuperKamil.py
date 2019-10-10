import json
import logging
import os
import os.path
import re
import sys
import time
import tkinter as tk
from io import BytesIO
from tempfile import NamedTemporaryFile
from time import sleep
from tkinter import *
from tkinter.ttk import *
from webbrowser import open_new

import keyboard
from bs4 import BeautifulSoup
from gtts import gTTS
from playsound import playsound
from pygame import mixer
from requests_html import HTMLSession
from steam import steamid



# language which is used by speech generator 
language="pl"

#this line is importat for option "From file" to work
server_log_location = 'L:/SteamLibrary/steamapps/common/dota 2 beta/game/dota/server_log.txt'


'''CUSTOM DEFINITIONS'''
#this module should watch file for changes and if detects any 
#reports current MMR values for all players
'''
import sys, os.path, time, logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os

temp_name = '1.txt'

def kamil():

    try:
    
        f = open(temp_name,'r')
        number = int(f.read())
        number = number + 3
        f.close()

        f = open(temp_name,'w')
        f.write(str(number))
        print(number)

        if number >= 5:

            f.close()
            os.remove(temp_name)
            number = 0
            
            #tutaj wpisać co funkcja ma wykonywać. DOKŁADNIE KURWA TUTAJ

        else:
            
            f.close()

    except:

        temp = open(temp_name,'w+')
        temp.write('1')
        temp.close()

        kamil()


class MyEventHandler(PatternMatchingEventHandler):

    def on_moved(self, event):
        super(MyEventHandler, self).on_moved(event)
        logging.info("File %s was just moved" % event.src_path)

    def on_created(self, event): 
        super(MyEventHandler, self).on_created(event)
        logging.info("File %s was just created" % event.src_path)

    def on_deleted(self, event):
        super(MyEventHandler, self).on_deleted(event)
        logging.info("File %s was just deleted" % event.src_path)

    def on_modified(self, event):
        super(MyEventHandler, self).on_modified(event)
        logging.info("File %s was just modified" % event.src_path)
        print('Raz, czy dwa?')
        kamil()



def main(file_path=None):

    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    watched_dir = os.path.split(file_path)[0]
    print(watched_dir)
    print( 'watched_dir = {watched_dir}'.format(watched_dir=watched_dir))
    patterns = [file_path]
    print( 'patterns = {patterns}'.format(patterns=', '.join(patterns)))
    event_handler = MyEventHandler(patterns=patterns)
    observer = Observer()
    observer.schedule(event_handler, watched_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



if __name__ == "__main__":
    if 1:
        path = 'G:/GitHub/Castle-Stalker/penis.txt'
        main(file_path=path.strip())
'''


#changes link inside clipboard from Steam user profile to CastleFight profile
def link_change():
    url=app.clipboard_get()
    cf_url='https://dotacastlefight.com/players/'
    steamid64=steamid.steam64_from_url(url, http_timeout=30)
    k=str(str(cf_url)+str(steamid64))
    open_new(k)

#converts string to list and space as separator
def Convert(string): 
    li = list(string.split(" ")) 
    return li 


def get_MMR_2(steamid64):

    try:
        cf_url ='https://dotacastlefight.com/api/players/'

        new_url =str(str(cf_url)+str(steamid64))

        #create html session
        session = HTMLSession()
        r = session.get(str(new_url))

        #get html page content as text
        html_page =r.html.text

        #parse and find 'mmr' inside
        soup = BeautifulSoup(html_page ,'lxml')

        name = json.loads(str(soup.text))

        user = str(name["username"])
        MMR = str(str(name["mmr"])+'\n')

        username = str(user[0:15]+'\n')

        text_box.insert(INSERT,username)
        text_box2.insert(INSERT,MMR, 'center')

        #print('Player MMR: \t\t',name["username"])
        #print('Player MMR: \t\t',name["mmr"],'\n')

    except:
        no_name = str('NO DATA\n')
        no_MMR = str('NONE\n')
        text_box.insert(INSERT,no_name)
        text_box2.insert(INSERT,no_MMR, 'center')



def get_MMR_from_file():

    #handles file
    fileHandle = open (server_log_location,"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()

    amount = -1

    if 'loopback' in str(lineList[amount]):
        amount = -2

        if 'Party' in str(lineList[amount]):
            result = re.search('DOTA_GAMEMODE_CUSTOM (.*)\) ', lineList[amount])    #wartość przy current_line zmieniać co parzyste, online chyba co nieparzyste

        else:
            result = re.search('DOTA_GAMEMODE_CUSTOM (.*)\)', lineList[amount])

    else:
        if 'Party' in str(lineList[amount]):
            result = re.search('DOTA_GAMEMODE_CUSTOM (.*)\) ', lineList[amount])    #wartość przy current_line zmieniać co parzyste, online chyba co nieparzyste

        else:
            result = re.search('DOTA_GAMEMODE_CUSTOM (.*)\)', lineList[amount])


    x = result.group(1)
    converted_x = Convert(x)

    #unlocks text_box and clears it
    text_box.config(state=NORMAL)
    text_box.delete('1.0', END)
    text_box2.config(state=NORMAL)
    text_box2.delete('1.0', END)

    for i in converted_x:

        #print(i[2:])
        k = steamid.make_steam64(i[2:])
        number = str(int(i[0])+1)+'. '
        text_box.insert(INSERT,number)
        get_MMR_2(k)
        playsound('pop.wav')

    text_box.config(state=DISABLED)
    text_box2.config(state=DISABLED)

#pretty self explanatory, I guess
def get_MMR():
    try:

        #clears inputbox
        #blank.delete(0, END)
        url =app.clipboard_get()

        cf_url ='https://dotacastlefight.com/api/players/'
        steamid64 =steamid.steam64_from_url(url, http_timeout=30)
        new_url =str(str(cf_url)+str(steamid64))

        #create html session
        session = HTMLSession()
        r = session.get(str(new_url))

        #get html page content as text
        html_page =r.html.text

        #parse and find 'mmr' inside
        soup = BeautifulSoup(html_page ,'lxml')
        name = json.loads(str(soup.text))
        value = name["mmr"]

        #returns 'value' inside inputbox
        blank.configure(text=value, font='bold')

        #play sound when MMR is here
        playsound('good.wav')

        #GET Goole to read MMR
        myobj = gTTS(text=str(value), lang=language, slow=False)

        #store it
        f = NamedTemporaryFile(suffix='.mp3',)

        #write to tmpfile
        myobj.write_to_fp(f)

        #set tmpfile at beggining
        f.seek(0)

        #read tmpfile
        mixer.init()
        mixer.music.load(f)
        mixer.music.play()  

    except:
        #play sound when MMR is **NOT** here
        playsound('bad.wav')


def get_link_to_clipboard():
    url = app.clipboard_get()
    cf_url ='https://dotacastlefight.com/players/'

    #generate steamid64
    steamid64 = steamid.steam64_from_url(url, http_timeout=30)

    #make link with steamid64
    k = str(str(cf_url)+str(steamid64))
    app.clipboard_clear()
    app.clipboard_append(k)


#just to make sure that icon will be in .exe file
def resource_path(relative_path):    
    try:       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



'''MAIN APP MODULE'''
app = Tk()
app.title('Kamil')
#app.geometry('250x100')
app.wm_attributes('-alpha',0.8,'-topmost',1)
app.configure(background='black')

#icon in the top left corner
app.iconbitmap(default=resource_path('icons8-castle-64.ico'))

'''STYLES'''
style = Style()
style.configure('W.TButton', 
                foreground = 'black', 
                background = 'white',
                bd=0,
                bg='black')

style.configure("BW.TLabel",
                font = ('bold'), 
                foreground="white", 
                background="black")

style.configure('BW.TText',
                foreground='white',
                background='black')


'''TEXT BOXES'''
text_box = tk.Text(app,
                height=8,
                width=4,
                bg='black',
                fg='white',
                font='Calibri')


text_box.grid(                    
                row=6,
                column=0,
                columnspan=4,
                sticky='nsew')

text_box2 = Text(app,
                height=8,
                width=6,
                bg='black',
                fg='white',
                font='Calibri')

text_box2.tag_configure("center", justify='center')
text_box2.tag_add("center", 1.0, "end")


text_box2.grid(                    
                row=6,
                column=1,
                columnspan=4,
                sticky='nse')

#just to not temt fate
text_box.config(state=DISABLED)
text_box2.config(state=DISABLED)


'''LABELS'''
#MMR output box
blank = Label(app,
                background='black',
                foreground='white')

blank.grid( row=1, 
            column=1,
            pady=10)

Label(app,  text='MMR:', 
            style='BW.TLabel').grid(
                pady=10,
                row=1,
                column=0, 
                sticky='nsew')

Label(app,  text='Username', 
            style='BW.TLabel').grid(
                pady=2,
                row=5, 
                column=0,
                columnspan=2,
                sticky='ns')

Label(app,  text='MMR', 
            style='BW.TLabel').grid(
                pady=2,
                row=5, 
                column=2,
                sticky='ns')


'''BUTTONS'''
Button(app, 
            text='Show MMR', 
            command=get_MMR, 
            style="W.TButton").grid(
                row=4, 
                column=1, 
                sticky='nesw')


'''
Button(app, 
            text='Get CF link', 
            command=get_link_to_clipboard, 
            style="W.TButton").grid(
                row=4, 
                column=0,
                sticky=W)
'''


Button(app, 
            text='Show profile', 
            command=link_change, 
            style="W.TButton").grid(
                row=4, 
                column=0, 
                sticky=E)


Button(app, 
            text='From file', 
            command=get_MMR_from_file, 
            style="W.TButton").grid(
                row=4, 
                column=2, 
                sticky=E)


Button(app, 
            text='Quit',
            command=app.destroy, 
            style="W.TButton").grid(
                row=7, 
                column=1, 
                sticky='n',
                pady=3,
                padx=5)



'''SHORTCUTS'''
#triggers get_MMR on hotkey
keyboard.add_hotkey('caps lock',get_MMR)
keyboard.add_hotkey('ctrl+shift',get_MMR_from_file)



#apploop
app.mainloop()
