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
from tkinter import ttk

import keyboard
from bs4 import BeautifulSoup
from gtts import gTTS
from playsound import playsound
from pygame import mixer
from requests_html import HTMLSession
from steam import steamid
import threading
from PIL import Image, ImageTk


'''MAIN CONFIG SCHEME'''
#config to your liking
#all colors
light_grey = '#c2c2c2'
dark_grey= '#828282'
everything_that_is_white = '#ffffff'
everything_that_is_black = '#000000'

#all fonts
label_font = 'Helvetica 15 bold'
button_font = 'Arial 10 bold'
mainText_font = 'Arial 14'
progressBar_font = 'Arial 9 bold'

#main window attributes
alpha = 0.8
always_on_top = True

#language which is used by speech generator 
language='pl'

#this line is importat for option 'From file' to work
server_log_location = 'L:/SteamLibrary/steamapps/common/dota 2 beta/game/dota/server_log.txt'

#Temporary file where server_log is stored
temp_name = 'tmp.txt'
temp = open(temp_name,'w+')
temp.close()

#time in which app checks file for changes
time_in_seconds_to_check_for_changes = 60

#convert seconds to miliseconds
interval = time_in_seconds_to_check_for_changes * 1000   

#time to first check file after startup
first_check = interval//100

#-------------------------------------------------------------------------------------------------#

'''CUSTOM DEFINITIONS'''
#this module should watch file for changes and if detects any 
#reports current MMR values for all players

def quick_check():

    fileHandle = open (server_log_location,'r' )
    line_serverList = fileHandle.readlines()
    fileHandle.close()

    log_content = str(line_serverList[-3:])

    f = open(temp_name,'r')
    log_memorization = f.read()
    f.close()

    try:
        if str(log_memorization) != log_content:

            #print('weszło w ifa!')
            temp = open(temp_name,'w+')
            temp.write(log_content)

            #print(log_content)
            temp.close()
            get_MMR_from_file()

            pass
        else:
            pass
        pass

    except:
        pass


    run_progressBar()
    #print('checking')
    
    app.after(1, quick_check)



#changes link inside clipboard from Steam user profile to CastleFight profile
def link_change():
    url=app.clipboard_get()
    cf_url='https://dotacastlefight.com/players/'
    steamid64=steamid.steam64_from_url(url, http_timeout=30)
    k=str(str(cf_url)+str(steamid64))
    open_new(k)

#converts string to list and space as separator
def Convert(string): 
    li = list(string.split(' ')) 
    return li 


def get_MMR_2(steamid64):

    try:
        cf_url ='https://dotacastlefight.com/api/players/'

        new_url =str(str(cf_url)+str(steamid64))

        #create html session
        session = HTMLSession()
        r = session.get(str(new_url))

        #get html page content as text
        html_page = r.html.text

        #parse and find 'mmr' inside
        soup = BeautifulSoup(html_page ,'lxml')

        name = json.loads(str(soup.text))

        user = str(name['username'])
        MMR = str(str(name['mmr'])+'\n')

        username = str(user[0:15]+'\n')

        text_box.insert(INSERT,username)
        text_box2.insert(INSERT,MMR, 'center')

        #print('Player MMR: \t\t',name['username'])
        #print('Player MMR: \t\t',name['mmr'],'\n')

    except:
        no_name = str('NO DATA\n')
        no_MMR = str('NONE\n')
        text_box.insert(INSERT,no_name)
        text_box2.insert(INSERT,no_MMR, 'center')

'''
        r2 = session.get(str(leaderboard_url))
        leaderboard_url = 'https://dotacastlefight.com/api/leaderboard'
        html_page_leaderboard = r.html.text
'''

def get_MMR_from_file():

    #handles file
    fileHandle = open (server_log_location,'r' )
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
        playsound('./Sounds/pop.wav')

    text_box.config(state=DISABLED)
    text_box2.config(state=DISABLED)

#pretty self explanatory, I guess
def get_MMR():
    try:

        #clears inputbox
        url = app.clipboard_get()

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
        value = name['mmr']

        username = name['username']

        #returns 'value' inside inputbox
        blank.configure(text=value)
        user_name_label.configure(text=username[0:18])

        #play sound when MMR is here
        playsound('./Sounds/good.wav')

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
        playsound('./Sounds/bad.wav')


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
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def run_progressBar():

    max_value=1000

    progressBar['value'] = 0
    progressBar['maximum'] = max_value

    #counts time left to another check
    sleep_time=interval/1000000
    step_time = float(interval/(max_value*1000))
    starting_time = interval/max_value
    time_left = starting_time

    for i in range(1,1001):
        time.sleep(sleep_time)
        text=str('Automatic check in: '+ str(round(time_left,1))+' seconds')
        progressBar_style.configure('Horizontal.TProgressbar',text=text)
        time_left = starting_time - (step_time*i)
        progressBar['value'] = i
        #uncomment to print all steps in the console
        #print('step:\t',float(i),'time left:\t',round(time_left,3))
        progressBar.update()


def Exit():
    os.remove('tmp.txt')
    app.destroy()



'''MAIN APP MODULE'''
app = Tk()

#Title
app.title('SuperKamil')
app.resizable(0,0)

#if always_on_top == True or 1:
app.grab_set()
app.focus_force()

app.wm_attributes('-alpha',alpha,'-topmost',always_on_top)
app.configure(background=everything_that_is_black)

#icon in the top left corner
app.iconbitmap(default=resource_path('./Icon/icons8-castle-64.ico'))

#imported PNG to cuz tried to use it somehow, but it's pointless
#my_png =  PhotoImage(file='./Icon/icons8-castle-64.png')
#my_png = my_png.subsample(2)


'''STYLES'''
style = Style()
Style().theme_use('clam')
style.configure('W.TButton', font=(button_font),
                foreground = dark_grey, 
                background = everything_that_is_black, 
                relief='groove',
                borderwidth=3, 
                height=20)

style.configure('BW.TLabel', font=(label_font),
                foreground=everything_that_is_white, 
                background=everything_that_is_black)




'''TEXT BOXES'''
text_box = tk.Text(app,
                height=8,
                width=18,
                bg=everything_that_is_black,
                fg=everything_that_is_white,
                font=mainText_font,bd=1)


text_box.grid(                    
                row=6,
                column=0,
                columnspan=3,
                sticky='nsew')

text_box2 = Text(app,
                height=8,
                width=8,
                bg=everything_that_is_black,
                fg=everything_that_is_white,
                font=mainText_font,bd=1)

text_box2.tag_configure('center', justify='center')
text_box2.tag_add('center', 1.0, 'end')


text_box2.grid(                    
                row=6,
                column=2,
                #columnspan=4,
                sticky='nse')

#just to not temt fate
text_box.config(state=DISABLED)
text_box2.config(state=DISABLED)



'''LABELS'''
#MMR output box
blank = Label(app, text='MMR', 
                font=(label_font),
                background=everything_that_is_black,
                foreground=everything_that_is_white)

blank.grid( row=1, 
            column=2,
            pady=10,
            sticky='ns')

user_name_label = Label(app,
                font=label_font,
                background=everything_that_is_black,
                foreground=everything_that_is_white,
                text='Nick')
                #style='BW.TLabel')
                
user_name_label.grid(
                pady=10,
                row=1,
                column=0, 
                columnspan=2,
                sticky='ns')

Label(app,  text='Username', 
            style='BW.TLabel').grid(
                pady=5,
                row=5, 
                column=0,
                columnspan=2,
                sticky='ns')

Label(app,  text='MMR', 
            style='BW.TLabel').grid(
                pady=5,
                row=5, 
                column=2,
                sticky='ns')



'''BUTTONS'''
Button(app, 
            text='Direct', 
            command=get_MMR, 
            style='W.TButton').grid(
                row=4, 
                column=1, 
                sticky='nesw')


'''
Button(app, 
            text='Get CF link', 
            command=get_link_to_clipboard, 
            style='W.TButton').grid(
                row=4, 
                column=0,
                sticky=W)
'''


Button(app, 
            text='Browser', 
            command=link_change, 
            style='W.TButton').grid(
                row=4, 
                column=0, 
                sticky='nesw')


Button(app, 
            text='File', 
            command=get_MMR_from_file, 
            style='W.TButton').grid(
                row=4, 
                column=2, 
                sticky='nesw')


quit_button = Button(app, 
            text='Q U I T',
            command=Exit, 
            style='W.TButton').grid(
                row=8, 
                column=1, 
                sticky='ns',
                pady=3,
                padx=5)



'''POGRESS BAR'''

progressBar = ttk.Progressbar(app,
             orient='horizontal',
             style='Horizontal.TProgressbar',
             mode='determinate')
            

progressBar.grid(
                row=7,
                column=0,
                columnspan=3,
                #pady=3,
                ipady=3,
                sticky='nesw')

progressBar_style = Style()
#progressBar_style.theme_use('winnative') #to choose from ('xpnative','winnative','clam', 'alt', 'default', 'classic','vista')

progressBar_style.layout('Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
               {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}), 
              ('Horizontal.Progressbar.label', {'sticky': 'ns'}),
              ('Horizontal.Progressbar.border', {'border': 'False'})])

progressBar_style.configure('Horizontal.TProgressbar', 
                            text='Please wait, loading app and results',
                            font=(progressBar_font), sticky='ns')

style.configure('Horizontal.TProgressbar', 
                troughcolor= dark_grey, 
                bordercolor=dark_grey, 
                background=light_grey, 
                lightcolor=light_grey, 
                darkcolor=light_grey,
                width=30)

'''
THREADING ATTEMPT
progressBar_thread = threading.Thread()
progressBar_thread.__init__(target=run_progressBar, args=())
#progressBar_thread.start()
'''


'''SHORTCUTS'''
#triggers get_MMR on hotkey
keyboard.add_hotkey('caps lock',get_MMR)
keyboard.add_hotkey('ctrl+shift',get_MMR_from_file)



#triggering progressbar and first file check
app.after(first_check,quick_check)

#apploop
app.mainloop()

