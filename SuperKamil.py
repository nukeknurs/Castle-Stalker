import os
import sys
from tkinter import *
from tkinter.ttk import *
from webbrowser import open_new

import keyboard
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from steam import steamid



'''CUSTOM DEFINITIONS'''
#changes link inside clipboard from Steam user profile to CastleFight profile
def link_change():
    url=app.clipboard_get()
    cf_url='https://dotacastlefight.com/players/'
    steamid64=steamid.steam64_from_url(url, http_timeout=30)
    k=str(str(cf_url)+str(steamid64))
    open_new(k)

#pretty self explanatory, I guess
def get_MMR():

    #clears inputbox
    blank.delete(0, END)
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
    value =str(soup)[str(soup).find('mmr')+5:str(soup).find('mmr')+9]

    #returns 'value' inside inputbox
    blank.insert(0,value)

def get_link_to_clipboard():
    url =app.clipboard_get()
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

#styles
style = Style()
style.configure('W.TButton', 
                foreground = 'black', 
                background = 'white')

style.configure("BW.TLabel",
                font = ('bold'), 
                foreground="white", 
                background="black")



'''LABELS'''
#MMR output box
blank = Entry(app)
Label(app,  text="MMR", 
            style='BW.TLabel').grid(
                row=1, 
                sticky=W)

blank.grid( row=1, 
            column=1)



'''BUTTONS'''
Button(app, text='Show MMR', 
            command=get_MMR, 
            style="W.TButton").grid(
                row=1, 
                column=2, 
                sticky=W)

Button(app, text='Get CF link', 
            command=get_link_to_clipboard, 
            style="W.TButton").grid(
                row=4, 
                column=0,
                sticky=W)

Button(app, text='Show profile', 
            command=link_change, 
            style="W.TButton").grid(
                row=4, 
                column=2, 
                sticky=E)

Button(app, text='Quit', 
            command=app.destroy, 
            style="W.TButton").grid(
                row=5, 
                column=1, 
                sticky=N)



'''SHORTCUTS'''
#triggers get_MMR on hotkey
keyboard.add_hotkey('capslock',get_MMR)



#apploop
app.mainloop()
