from customtkinter import *
import os
import time 
import threading        
from add_songs import add_ui
from classes import Song

music_folder = "Songs/"
songs_playing = []

root = CTk()
root.grid_columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)  
myFont = CTkFont(size=20, weight="bold")
set_appearance_mode("System")
set_default_color_theme("green")
main = CTkFrame(root, fg_color="black", corner_radius=0)

main.columnconfigure(0, weight=0)
main.columnconfigure(1, weight=2)
main.rowconfigure(0, weight=0)
main.rowconfigure(1, weight=1)
main.rowconfigure(2, weight=1)

def clear():
    widgets = page.grid_slaves()
    for i in widgets:
        i.destroy()

def open_songs():
    clear()

    global songs
    songs = []
    for i in sorted(os.listdir(music_folder)):
        songs.append(Song("Songs/"+i))
    counter = 0
    song_scrollpage = CTkFrame(page, fg_color="gray", width=300)
    for i in range(len(songs)):
        CTkButton(song_scrollpage, text=songs[i].name[:32], font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b", command=(lambda s=i: play_song(s)), corner_radius=0, width=350, anchor=W).grid(column=0, row=i+counter, pady=1)
        counter += 1
    song_scrollpage.grid(ipady=1)

def open_add(page):
    add_ui(page)

def stop(song):
    global songs_playing, end
    try:
        songs_playing[-1].track.stop()
        end = True
       # waiting.join()
    except:
        pass
    songs_playing.append(song)

def autoplay(length):
    global end
    end = False
    count = 0
    while count != 1000:
        time.sleep(length/1000)
        if end:
            break
        count += 1
    if count == 1000:
        song_index += 1
        play_song(song_index)

def change(direction):
    try:
        play_song(song_index + direction)
    except:
        pass

def play_song(i):
    global waiting, display_name, song_index
    
    song_index = i

    try:
        song = songs[song_index]
    except:
        song_index = 0
        song = songs[song_index]

    stop(song)
    song.track.play()
    waiting = threading.Thread(target=autoplay, args=(song.length,))
    waiting.start()
    display_name.configure(text=songs[song_index].name[:32])

page = CTkFrame(main, width=320)
page.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(2,10) ,pady=10)
main.grid(row=0, column=0, sticky="nsew")

home = CTkFrame(main)
CTkButton(home, text="Home", font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b").grid(row=0, column=0, padx=15, pady=(10, 5))
CTkButton(home, text="Settings", font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b").grid(row=1, column=0, padx=15, pady=(5, 10))
CTkButton(home, text="Add Songs", font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b", command=lambda:open_add(page)).grid(row=2, column=0, padx=15, pady=(5, 10))
home.grid(row=0, column=0, sticky="nsew", padx=(10,3) ,pady=(10,3))

library = CTkFrame(main)
CTkLabel(library, text="Library", font=myFont).grid(row=0, column=0, padx=15, pady=(10,5))
CTkButton(library, text="Songs", font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b", command=open_songs).grid(row=1, column=0, padx=15, pady=(5,5))
CTkButton(library, text="Artists", font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b").grid(row=2, column=0, padx=15, pady=(5,5))
CTkButton(library, text="Albums", font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b").grid(row=3, column=0, padx=15, pady=(5,10))
library.grid(row=1, column=0, sticky="nsew", padx=(10,3) ,pady=(3,10))

controls = CTkFrame(main)

controls.columnconfigure(0, weight=1)

display_name = CTkLabel(controls, corner_radius=10, fg_color="blue", font=myFont, anchor=W)
display_name.grid(row=0, column=0, sticky="nsew")
#CTkSlider(controls).grid(row=0, column=1)
CTkButton(controls, text="Back", width=70, command=lambda:change(-1)).grid(row=0, column=2)
CTkButton(controls, text="Pause", width=70).grid(row=0, column=3)
CTkButton(controls, text="Next", width=70, command=lambda:change(1)).grid(row=0, column=4)
controls.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0,10))

root.mainloop()