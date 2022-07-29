import vlc as vlc
from youtube_dl import YoutubeDL
from tkinter import *
import os
import mutagen
from PIL import ImageTk, Image
import time
import threading
import urllib.request
import shutil
global immortals
immortals = {}

root = Tk()
root.config(bg="white")
root.resizable(False, False)

back_button = Image.open("Images/Back.png")
pause_button = Image.open("Images/Pause.png")
play_button = Image.open("Images/Play.png")
next_button = Image.open("Images/Next.png")
previous_button = Image.open("Images/Previous.png")

pause_button = pause_button.resize((63, 52), Image.ANTIALIAS)
play_button = play_button.resize((63, 52), Image.ANTIALIAS)
next_button = next_button.resize((54, 63), Image.ANTIALIAS)
previous_button = previous_button.resize((54, 63), Image.ANTIALIAS)

back_button = ImageTk.PhotoImage(back_button)
pause_button = ImageTk.PhotoImage(pause_button)
play_button = ImageTk.PhotoImage(play_button)
next_button = ImageTk.PhotoImage(next_button)
previous_button = ImageTk.PhotoImage(previous_button)

myFont = ("Helvetica", 20, "bold")
music_folder = r"D:/Conduit/Songs/"
thumbnail_folder = r"D:/Conduit/Album Art/"
if not os.path.exists(music_folder):
    os.makedirs(music_folder)
if not os.path.exists(thumbnail_folder):
    os.makedirs(thumbnail_folder)
songs = sorted(os.listdir(music_folder))
thumbnails = sorted(os.listdir(thumbnail_folder))
songs_playing = []
image_switch = [pause_button, play_button]
counter_image = 0


############################ LIBRARY #######################################################################################################
def clear():
    widgets = root.grid_slaves()
    for i in widgets:
        i.destroy()


def library():
    clear()
    root.title("Library")

    Button(root, image=back_button, borderwidth=0, bg="white", activebackground="white", command=main). \
        grid(column=0, row=0, stick="w", padx=0, pady=0)
    Label(root, text="Library", font=("Helvetica", 30, "bold"), fg="#222222", bg="white", anchor="w"). \
        grid(column=0, row=1, sticky="w", rowspan=2)
    Button(root, text="Artists", font=myFont, fg="#ff4a72", bg="white", width=20, anchor="w").grid(column=0, row=3, sticky="w", rowspan=2)
    Button(root, text="Albums", font=myFont, fg="#ff4a72", bg="white", width=20, anchor="w", command=album_win).grid(column=0, row=5, sticky="w", rowspan=2)
    Button(root, text="Playlists", font=myFont, fg="#ff4a72", bg="white", width=20, anchor="w").grid(column=0, row=7, sticky="w", rowspan=2)
    Button(root, text="Songs", font=myFont, fg="#ff4a72", bg="white", width=20, anchor="w", command=song_win).grid(column=0, row=9, sticky="w", rowspan=2)


def load_controls():
    global display_name, counter_image
    try:
        display_name = Label(controls, text=song_name, font=myFont, bg="#f8f3f3", fg="#222222", width=31, anchor="w")

        Button(controls, image=previous_button, bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100, command=lambda: change(-1)) \
            .grid(column=7, row=0, padx=0, pady=0, sticky="nsew")

        Button(controls, image=image_switch[counter_image], bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100, command=lambda: pause_song()) \
            .grid(column=8, row=0, padx=0, pady=0, sticky="nsew")

        Button(controls, image=next_button, bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100, command=lambda: change(1)) \
            .grid(column=9, row=0, padx=0, pady=0, sticky="nsew")

    except:
        display_name = Label(controls, text="", font=myFont, bg="#f8f3f3", fg="#222222", width=35, anchor="w")

        Button(controls, image=previous_button, bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100) \
            .grid(column=7, row=0, padx=0, pady=0, sticky="nsew")

        Button(controls, image=image_switch[counter_image], bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100) \
            .grid(column=8, row=0, padx=0, pady=0, sticky="nsew")

        Button(controls, image=next_button, bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100) \
            .grid(column=9, row=0, padx=0, pady=0, sticky="nsew")

    display_name.grid(column=0, row=0, sticky="w", padx=(20, 0))


def album_win():
    clear()
    root.title("Albums")
    albums = {}
    for i in songs:
        song = mutagen.File(music_folder + i)["albm"]
        if song[0] not in albums.keys():
            albums[song[0]] = []
        albums[song[0]].append(i)

    Button(root, image=back_button, borderwidth=0, bg="white", activebackground="white", command=library).grid(column=0, row=0, stick="w", padx=0, pady=0)
    counter = 0

    frame = Frame(root, border=1, width=100)
    canvas = Canvas(frame, bg="light gray", highlightthickness=0, bd=0)

    for i in range(len(albums)):
        album_names = list(albums.keys())
        album_names.sort()
        Button(canvas, text=album_names[i], font=("Helvetica", 15, "bold"), fg="#222222", bg="white", width=20,
               borderwidth=0, activebackground="white").grid(column=counter, row=i - counter, padx=1, pady=1)
        if counter == 0:
            counter += 1
        else:
            counter = 0
    canvas.grid(row=0, column=0)
    frame.grid(row=1, column=0)


def song_win():
    clear()

    def geometry(event):
        song_list.config(scrollregion=song_list.bbox("all"), width=900, height=300)

    def on_mousewheel(event):
        song_list.yview_scroll(int(-1*(event.delta/120)), "units")

    root.title("Songs")
    frame = Frame(root, border=1, width=200)
    global controls, slider
    controls = Frame(root, bg="#f8f3f3", width=70, highlightthickness=0, bd=0)
    song_list = Canvas(frame, bg="white", highlightthickness=0, bd=0)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=song_list.yview)
    frame.bind_all("<MouseWheel>", on_mousewheel)
    song_list.config(yscrollcommand=scrollbar.set)
    song_list_scrollbar = Frame(song_list, borderwidth=0, highlightthickness=0, relief="flat")
    counter = 0

 #   slider = Scale(controls, length=100, from_=0, to_=200, orient=HORIZONTAL)
  #  slider.configure(command=slide)
   # slider.grid(row=3, column=0, columnspan=10)

    Button(root, image=back_button, borderwidth=0, bg="white", activebackground="white", command=library).grid(column=0, row=0, stick="w", padx=0, pady=0)

    for i in range(len(songs)):
        path = music_folder + songs[i]
        song = mutagen.File(path)
        name = songs[i].replace(".m4a", "")
        playing = lambda s=i: play_song(s)
        artist = song.get('art\x00')[0]

        try:
            thumbnail_name = r"D:/Conduit/Album Art/" + name + artist + ".png"
            album_art = Image.open(thumbnail_name)
        except:
            album_art = Image.open("NoCover.png")

        album_art = ImageTk.PhotoImage(album_art)
        immortals[name] = album_art

        Button(song_list_scrollbar, image=immortals[name], borderwidth=0, command=playing, bg="white").grid(column=0, row=i + counter, rowspan=2, stick="w", padx=0, pady=0)
        Button(song_list_scrollbar, text=name, font=("Helvetica", 15, "bold"), fg="#222222", bg="white", anchor="sw", width=200, borderwidth=0,
               activebackground="white", command=playing).grid(column=1, row=i + counter, padx=(5, 0), pady=(0, 0), sticky="w")
        counter += 1
        Button(song_list_scrollbar, text=artist, font=("Helvetica", 10, "bold"), fg='#969699', bg="white", anchor="nw", width=200, borderwidth=0,
               activebackground="white", activeforeground="#969699", command=playing).grid(column=1, row=i + counter, sticky="w", padx=(5, 0), pady=(0, 3))

    frame.grid(column=0, row=1, columnspan=10)
    scrollbar.grid(column=10, row=0, sticky="ns")
    song_list.grid(row=0, column=0)
    song_list.create_window((0, 0), window=song_list_scrollbar, anchor="nw")
    song_list_scrollbar.bind("<Configure>", geometry)

    load_controls()
    controls.grid(row=2, column=0, columnspan=10)


def slide(x):
    global Current_Time
    Player = songs_playing[-1]
    Length = Player.get_length()
    x = int(float(x))
    Time = (Length) * (x / 5000)
    Player.set_time(int(Time))


def stop():
    global songs_playing, track
    try:
        songs_playing[-1].stop()
        global end
        end = True
        waiting.join()
    except:
        pass
    songs_playing.append(track)


def pause_song():
    global waiting, songs_playing, counter_image, end, song, x
    try:
        player = songs_playing[-1]
        player.pause()
        counter_image += 1

        try:
            Button(controls, image=image_switch[counter_image], bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100, command=pause_song) \
                .grid(column=8, row=0, padx=0, pady=0, sticky="nsew")

        except:
            counter_image = 0
            Button(controls, image=image_switch[counter_image], bg="#f8f3f3", borderwidth=0, cursor="hand2", width=100, command=pause_song) \
                .grid(column=8, row=0, padx=0, pady=0, sticky="nsew")
        if counter_image == 0:
            end = True
            waiting.join()
        else:
            length = song.info.length - (player.get_time() / 1000)
            waiting = threading.Thread(target=autoplay, args=(length,))
            waiting.start()
    except:
        pass


def change(direction):
    try:
        play_song(x + direction)
    except:
        pass


def autoplay(length):
    global end, x
    end = False
    count = 0
    while count != 1000:
        time.sleep(length / 1000)
        if end:
            break
        count += 1
    if count == 1000:
        x += 1
        play_song(x)


def play_song(played_song):
    global waiting, display_name, controls, song, song_name, x, track, counter_image

    counter_image = 0
    x = played_song

    try:
        path = music_folder + songs[x]
    except:
        x = 0
        path = music_folder + songs[x]
    song = mutagen.File(path)
    length = song.info.length
    track = vlc.MediaPlayer(path)
    stop()
    song_name = songs[x].replace(".m4a", "")
    display_name['text'] = song_name
    track.play()
    load_controls()
    waiting = threading.Thread(target=autoplay, args=(length,))
    waiting.start()


############################ ADDING SONGS ##################################################################################################


def add_ui():
    clear()
    root.title("Add Songs")

    var = StringVar(root, "1")

    Button(root, image=back_button, borderwidth=0, bg="white", activebackground="white", command=main). \
        grid(column=0, row=0, stick="w", padx=0, pady=0)
    Label(root, text="URL:", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=1, padx=10, pady=10)
    url = Text(root, height=1, width=48, font=myFont, borderwidth=5)
    url.grid(column=1, row=1, columnspan=3, padx=10, pady=10)

    Label(root, text="Song Title:", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=2, padx=10, pady=10)
    name = Text(root, height=1, width=48, font=myFont, borderwidth=5)
    name.grid(column=1, row=2, columnspan=3, padx=10, pady=(0, 10))

    Label(root, text="Artist:", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=3, padx=10, pady=10)
    artist = Text(root, height=1, width=48, font=myFont, borderwidth=5)
    artist.grid(column=1, row=3, columnspan=3, padx=10, pady=10)

    Label(root, text="Album:", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=4, padx=10, pady=10)
    album = Text(root, height=1, width=48, font=myFont, borderwidth=5)
    album.grid(column=1, row=4, columnspan=3, padx=10, pady=10)

    Label(root, text="Album Art:", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=5, padx=10, pady=10)
    Radiobutton(root, text="From Youtube", variable=var, value="1", indicator=0, font=myFont).grid(column=1, row=5)
    Radiobutton(root, text="Import picture", variable=var, value="2", indicator=0, font=myFont).grid(column=2, row=5)
    Radiobutton(root, text="None", variable=var, value="3", indicator=0, font=myFont).grid(column=3, row=5  )

    Label(root, text="Track Number", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=6, padx=10, pady=10)
    track = Text(root, height=1, width=48, font=myFont, borderwidth=5)
    track.grid(column=1, row=6, columnspan=3, padx=10, pady=10)

    Label(root, text="Year Made:", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=7, padx=10, pady=10)
    year = Text(root, height=1, width=48, font=myFont, borderwidth=5)
    year.grid(column=1, row=7, columnspan=3, padx=10, pady=10)

    Label(root, text="Genre:", font=myFont, bg="white", fg="#ff4a72").grid(column=0, row=8, padx=10, pady=10)
    genre = Text(root, height=1, width=48, font=myFont, borderwidth=5)
    genre.grid(column=1, row=8, columnspan=3, padx=10, pady=10)

    Button(root, text="Enter",
           command=lambda: add(url.get("1.0", "end-1c"), name.get("1.0", "end-1c"),
                               artist.get("1.0", "end-1c"), album.get("1.0", "end-1c"),
                               track.get("1.0", "end-1c"), year.get("1.0", "end-1c"),
                               genre.get("1.0", "end-1c"), var.get()),
           font=myFont).grid(column=0, row=9, columnspan=4, padx=10, pady=10)


def download(url, tags, name, opt):
    global songs, thumbnails

    entity = YoutubeDL({"format": "m4a"}).extract_info(url, download=False)

    if name == "None":
        name = entity['title']

    thumbnail_name = name + tags[2] + ".png"
    name += ".m4a"
    path = music_folder + name

    if opt == "1":
        thumbnail = entity['thumbnail']
        urllib.request.urlretrieve(thumbnail, thumbnail_name)
        shutil.move(thumbnail_name, thumbnail_folder)
        art = Image.open(thumbnail_folder + thumbnail_name)
        art = art.resize((107, 60), Image.ANTIALIAS)
        art = art.crop((24, 0, 84, 60))
        art.save((thumbnail_folder + thumbnail_name))

    elif opt == "2":
        print("work in progress")

    YoutubeDL({"format": "m4a", 'outtmpl': path}).extract_info(url)
    song_info = mutagen.File(path)

    song_info['name'] = tags[1]
    song_info['art'] = tags[2]
    song_info['albm'] = tags[3]
    song_info['trck'] = tags[4]
    song_info['date'] = tags[5]
    song_info['gnr'] = tags[6]
    song_info.save()

    songs = sorted(os.listdir(music_folder))
    thumbnails = sorted(os.listdir(thumbnail_folder))


def add(url, name, artist, album, track, year, genre, opt):
    tags = [url, name, artist, album, track, year, genre]
    for i in range(len(tags)):
        if tags[i].strip() == "":
            tags[i] = "None"
    download_song = threading.Thread(target=download, args=(url, tags, name, opt))
    download_song.start()


############################ MAIN WINDOW ###################################################################################################


def main():
    clear()
    root.title("Main Menu")
    Label(root, text="Menu", font=("Helvetica", 30, "bold"), fg="#222222", bg="white", anchor="w"). \
        grid(column=0, row=0, pady=(10, 0), sticky="w")
    Button(root, text="Add Music", command=add_ui, font=myFont, fg="#ff4a72", bg="white", width=20, anchor="w"). \
        grid(column=0, row=1, sticky="w")
    Button(root, text="Library", command=library, font=myFont, fg="#ff4a72", bg="white", width=20, anchor="w"). \
        grid(column=0, row=2, sticky="w")
    Button(root, text="Quit", command=quit, font=myFont, fg="#ff4a72", bg="white", width=20, anchor="w").grid(column=0, row=3, sticky="w")


main()
root.mainloop()
