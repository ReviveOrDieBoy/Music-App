from youtubesearchpython import VideosSearch
from customtkinter import *
from yt_dlp import YoutubeDL

def add_ui(page):
    
    widgets = page.grid_slaves()
    for i in widgets:
        i.destroy()
    
    global myFont
    myFont = CTkFont(size=20, weight="bold")
    query = CTkEntry(page, font=myFont, width=300)
    query.grid(row=0, column=0, padx=15, pady=15)
    CTkButton(page, text="Search", font=myFont, command=lambda:search(query.get(), page)).grid(row=1, column=0, padx=15)

def edit_tags(request, page):

    widgets = page.grid_slaves()
    for i in widgets:
        i.destroy()

    CTkLabel(page, text="Title:", font=myFont).grid(column=0, row=0)
    CTkEntry(page).grid(column=1, row=0)
    CTkLabel(page, text="Artist", font=myFont).grid(column=0, row=1)
    CTkLabel(page, text="Album", font=myFont).grid(column=0, row=2)
    CTkLabel(page, text="Year", font=myFont).grid(column=0, row=3)


def search(request, page):
    print(request)
    counter = 2
    results =VideosSearch(request, limit=5).result()
    for i in range(5):
        song = results["result"][i]
        title = song["title"]
        channel = song["channel"]["name"]
        print(counter+i)
        CTkButton(page, text=title, font=myFont, fg_color="#2b2b2b", hover_color="#2b2b2b", anchor=W, command=lambda s=song: edit_tags(s, page)).grid(row=counter+i, column=0, pady=(3,0), sticky="w")
        counter += 1
        print(counter+i)
        CTkButton(page, text=channel, font=CTkFont(size=15, weight="bold"), text_color="gray", fg_color="#2b2b2b", hover_color="#2b2b2b").grid(row=counter+i, column=0, sticky="w")

    def download(song):
        
        path = "Songs/" + song["title"] + ".m4a"
        YoutubeDL({"format": "m4a", 'outtmpl': path}).extract_info(song["link"])