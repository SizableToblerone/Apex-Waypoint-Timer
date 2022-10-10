import tkinter
import tkinter.font
from distutils.dir_util import copy_tree
from tkinter import *
from tkinter import messagebox

import pyglet as pyglet
from pyautogui import *
import time
import PIL
from PIL import Image, ImageTk
import re

root = Tk()
root.title('Waypoint Timer')
window_width = 200
window_height = 350
# root.geometry(f'{window_width}x{window_height}+2520+300')   # debug location
root.geometry(f'{window_width}x{window_height}+1500+100') # publish location
root.attributes('-alpha', 0.95)

ringring = Canvas(root, width=300, height=300, bg='#999999')
arc = ringring.create_arc(50, 50, 200, 200)  # start=0, extent=0, fill='#4477ff', style=ARC)

SV_profile = StringVar()
# SV_profile.set('')
# SV_start_time = StringVar()
# SV_start_time.set('00:00')
SV_duration = StringVar()
SV_duration.set('22:00')
SV_time_passed = StringVar()
SV_time_passed.set('00:00')
SV_time_remaining = StringVar()
SV_time_remaining.set(SV_duration.get())
DV_radial_degree = DoubleVar()
DV_radial_degree.set(0)
SV_waypoints = StringVar()
e_waypoints = Text(root, height=50, width=20, relief='sunken')

appdata_path = os.getenv('APPDATA')

openpng = PIL.ImageTk.PhotoImage(PIL.Image.open('button_graphics/open.png'))
b_open = Menubutton(root, direction='right', relief='flat', image=openpng)
time_elapsed = PIL.ImageTk.PhotoImage(PIL.Image.open('button_graphics/time_elapsed.png'))
time_remaining = PIL.ImageTk.PhotoImage(PIL.Image.open('button_graphics/time_remaining.png'))
b_progress = Button(root)
e_progress = Entry(root)


start_time = 0
end_time = 0
tokking = False
paused = False

w_graphic = tkinter.Toplevel()

pyglet.font.add_file('Digital_Dismay.otf')  # Graphic timer font
DigiDismay = tkinter.font.Font(family='Digital Dismay', size=30, weight='normal')

# TODO: This shit broke, rounds too strongly. Fix it.
timer_scale = 0.9


def main():
    """
    Window that launches the graphic timer when the trigger is met.
    """
    w_graphic.destroy()

    # make APPDATA paths, if necessary.
    if not os.path.exists(f'{appdata_path}\wp_profiles'):
        os.makedirs(f'{appdata_path}\wp_profiles')
        copy_tree(f'wp_profiles', f'{appdata_path}\wp_profiles')

    playpause = PIL.ImageTk.PhotoImage(PIL.Image.open('button_graphics/playpause.png'))
    stop = PIL.ImageTk.PhotoImage(PIL.Image.open('button_graphics/stop.png'))
    save = PIL.ImageTk.PhotoImage(PIL.Image.open('button_graphics/save.png'))
    trash = PIL.ImageTk.PhotoImage(PIL.Image.open('button_graphics/trash.png'))

    # widget creation & placement
    num_rows = 9
    vert_spacing = 26

    populate_open_menu()
    b_open.place(x=10, y=vert_spacing*0, anchor=NW)

    e_profile = Entry(root, textvariable=SV_profile, relief='sunken', bd=2, width=18)
    e_profile.place(x=41, y=vert_spacing*0, anchor=NW)

    b_save = Button(root, image=save, command=save_profile, relief='flat')
    b_save.place(x=window_width-45, y=vert_spacing*0, anchor=NW)

    b_trash = Button(root, image=trash, command=trash_profile, relief='flat')
    b_trash.place(x=window_width-23, y=vert_spacing*0, anchor=NW)

    l_duration = Label(root, text='Duration:')
    l_duration.place(x=window_width/2, y=vert_spacing*1, anchor=NE)
    e_duration = Entry(root, textvariable=SV_duration, relief='sunken', bd=2, width=10)
    e_duration.place(x=window_width/2, y=vert_spacing*1, anchor=NW)

    b_play = Button(root, image=playpause, command=play_pause, relief='flat')
    b_play.place(x=window_width/2, y=vert_spacing*2-8, anchor=NE)
    b_stop = Button(root, image=stop, command=finish, relief='flat')
    b_stop.place(x=window_width/2, y=vert_spacing*2-8, anchor=NW)

    b_progress.config(image=time_elapsed, command=progress_mode, relief='flat')
    b_progress.place(x=window_width/2, y=vert_spacing*3-2, anchor=NE)

    e_progress.config(textvariable=SV_time_passed, relief='sunken', bd=2, width=5)
    e_progress.place(x=window_width/2, y=vert_spacing*3, anchor=NW)

    l_4a = Label(root, text="Waypoints")
    l_4a.place(x=35, y=vert_spacing*4, anchor=NW)
    # e_waypoints = Text(root, height=50, width=20, relief='sunken')
    e_waypoints.place(x=20, y=vert_spacing*5, anchor=NW)

    # e_start_time.focus()
    # root.bind(sequence='<Return>', func=graphic_window)
    # root.bind(sequence='<Return>', func=save_profile)

    # starts loop to scan for triggers outside mainloop
    root.after(2000, trigger_scanner)
    # starts mainloop
    root.mainloop()


def play_pause(event=''):
    global tokking, paused, start_time
    if not tokking:
        graphic_window(event)
        return
    paused = not paused
    if not paused:  # if JUST UN-PAUSED, due to prev line:
        if b_progress.configure()['image'][4] == 'pyimage2':  # if in time_elapsed mode
            start_time = time.time() - minsecs_str_to_secs(SV_time_passed.get())
        else:  # if in time_remaining mode
            start_time = time.time() - (
                        minsecs_str_to_secs(SV_duration.get()) - minsecs_str_to_secs(SV_time_remaining.get()))
    print(f'paused = {paused}')
    return


def graphic_window(event=''):
    """
    Graphic timer that tracks the timing of events throughout an Apex Legends BR game.
    """
    global start_time, arc, ringring, tokking, w_graphic, end_time, e_waypoints

    finish()
    w_graphic = tkinter.Toplevel()

    graphic_width = 300
    graphic_height = 300
    w_graphic.geometry(f'{graphic_width}x{graphic_height}+269+-40')
    # w_graphic.geometry(f'{graphic_width}x{graphic_height}+1920+700')

    # keep window on top
    w_graphic.wm_attributes("-topmost", True)
    # partial transparency
    w_graphic.attributes('-alpha', 0.95)

    transparent = "#efffff"
    w_graphic.attributes("-transparentcolor", transparent)
    w_graphic.overrideredirect(1)

    # start_time = time.time() - minsecs_str_to_secs(SV_start_time.get())

    if b_progress.configure()['image'][4] == 'pyimage2':    # if in time_elapsed mode
        start_time = time.time() - minsecs_str_to_secs(SV_time_passed.get())
        print("time_elapsed mode")
    else:                                                   # if in time_remaining mode
        start_time = time.time() - (minsecs_str_to_secs(SV_duration.get()) - minsecs_str_to_secs(SV_time_remaining.get()))

    ringring = Canvas(w_graphic, width=300, height=300, bg=transparent)
    coords = 350-(300*timer_scale), 350-(300*timer_scale), (300*timer_scale)-50, (300*timer_scale)-50
    arc = ringring.create_arc(coords, start=90, extent=0, fill='#4477ff', style=ARC, outline='#4477ff', width=20)

    l_elapsed = Label(w_graphic, textvariable=SV_time_passed, bg=transparent, font=DigiDismay, fg='black')

    ringring.itemconfig(arc, fill='#4477ff', extent=0)
    end_time = start_time + minsecs_str_to_secs(SV_duration.get())
    if not tokking:
        tokking = True
        tock(root)

    # parse text into waypoints
    waypoints_entry_lines = re.split('\n', e_waypoints.get(1.0, "end-1c"))
    for line in waypoints_entry_lines:
        times = re.findall('(\d+(?::|\.)\d+)', line)
        if len(times) == 0:
            continue
        if len(times) == 1:
            waypoint(minsecs_str_to_secs(times[0]), duration=10, color='#d1c767', text='Care Package', width=20)
        if "+" in line:
            waypoint(minsecs_str_to_secs(times[0]), duration=minsecs_str_to_secs(times[1]), color='#ff9900')
        if "-" in line:
            waypoint(minsecs_str_to_secs(times[0]),
                     duration=minsecs_str_to_secs(times[1])-minsecs_str_to_secs(times[0]), color='#ff9900')

    # widget placement
    num_rows = 4
    vert_spacing = 26
    ringring.place(x=graphic_width/2, y=vert_spacing*0, anchor=N)
    l_elapsed.place(x=graphic_width/2, y=graphic_height/2, anchor=CENTER)

    # starts graphic window mainloop
    # root.after(2000, trigger_scanner)
    w_graphic.mainloop()


def tock(event='', window=root):
    """
    'Tick, tock, tick, tock...' Updates the timer visual.
    """
    global arc, ringring, tokking, start_time
    # if timer isn't finished, keep tocking.
    if end_time - time.time() < 0:
        finish()
    elif paused:
        # start_time += 1
        window.after(1000, tock)
    else:
        SV_time_passed.set('{:02d}:{:02d}'.format(
            int((time.time() - start_time) / 60),  # minutes
            int((time.time() - start_time) % 60)  # seconds
                ))
        SV_time_remaining.set('{:02d}:{:02d}'.format(
            int((end_time - time.time()) / 60),  # minutes
            int((end_time - time.time()) % 60)  # seconds
                ))

        ringring.itemconfig(arc, extent=-seconds_to_radians(time.time() - start_time))
        window.after(1000, tock)


def waypoint(placement, duration=5, color='#000000', width=5, text='', label_font=("Helvetica", "10", "bold italic")):
    """
    method that sets a point along the arc to mark an event.
    places a label, anchored SW for 0-90°, NW for 91-180°, etc.
    """
    coords = 350-(300*timer_scale), 350-(300*timer_scale), (300*timer_scale)-50, (300*timer_scale)-50
    waypoint_arc = ringring.create_arc(coords, fill='#4477ff', style=ARC, outline=color, width=width,
                                       start=90-seconds_to_radians(placement), extent=-seconds_to_radians(duration))


def populate_open_menu():
    b_open.menu = Menu(b_open, tearoff=0)
    b_open["menu"] = b_open.menu
    saved_profiles = os.listdir(f'{appdata_path}\wp_profiles')
    for filename in saved_profiles:
        profile = filename[:-4]
        b_open.menu.add_command(label=profile, command=lambda x=profile: load_profile(f'{x}'))
    return


def save_profile():
    with open(f'{appdata_path}\wp_profiles/{SV_profile.get()}.txt', 'w') as file:
        file.write(f'Duration: {SV_duration.get()}\n{e_waypoints.get(1.0, "end-1c")}')
    populate_open_menu()
    return


def load_profile(profile=SV_profile.get()):
    SV_profile.set(profile)
    e_waypoints.delete(1.0, "end")
    with open(f'{appdata_path}\wp_profiles/{profile}.txt', 'r') as file:
        content = file.read()
        duration = re.findall("Duration: (\d+(?::|\.)\d+)\n", content)
        content = re.sub("Duration: \d+(?::|\.)\d+\n", "", content)
        if duration:
            SV_duration.set(duration.pop())
        e_waypoints.insert(INSERT, content)

    return


def trash_profile():
    if messagebox.askokcancel('Delete Profile', f'Are you sure you want to delete {SV_profile.get()}?\n'
                                                f'It will be gone forever!'):
        os.remove(f'{appdata_path}\wp_profiles/{SV_profile.get()}.txt')
        e_waypoints.delete(1.0, "end")
        SV_profile.set('')
        populate_open_menu()
    return


def minsecs_str_to_secs(minsecs_str='00:00'):
    minsecs = re.findall('\d+', minsecs_str)    # minutes and seconds
    seconds = 0
    if minsecs:
        seconds = int(minsecs[0]) * 60  # convert minutes to seconds
        if len(minsecs) > 1:
            seconds += int(minsecs[1])
    return seconds


def trigger_scanner():
    """
    Loop that runs alongside tkinter mainloop, checking for on-screen triggers.
    """
    # check for "00" initial countdown timer
    # if locateOnScreen('apex_timer_trigger.jpg', region=(950, 230, 60, 70), confidence=0.9) is not None:
    if locateOnScreen('apex_timer_trigger.jpg', region=(950, 230, 100, 100), confidence=0.8) is not None:
        root.after(1000, trigger_scanner)
        graphic_window()
        # print('theres the start!')
    # check for "space, continue" prompt to notice when game returns to main menu.
    elif locateOnScreen('timer_close_trigger.jpg', region=(840, 960, 230, 65), confidence=0.8) is not None:
        root.after(1000, trigger_scanner)
        finish()
        # print('theres the end!')
    else:
        # print(0)
        # continue looping the check
        root.after(1000, trigger_scanner)


def finish(event=''):
    global end_time, w_graphic, tokking
    w_graphic.destroy()
    end_time = 0
    SV_time_passed.set('00:00')
    SV_time_remaining.set(SV_duration.get())
    tokking = False


def progress_mode():
    # print(b_progress.configure().keys())
    # print(b_progress.configure()['image'])
    if b_progress.configure()['image'][4] == 'pyimage3':    # swap to time_elapsed mode
        b_progress.config(image=time_elapsed)
        e_progress.config(textvariable=SV_time_passed)
    else:                                                   # swap to time_remaining mode
        b_progress.config(image=time_remaining)
        e_progress.config(textvariable=SV_time_remaining)
    return


def seconds_to_radians(seconds):
    time_percent = seconds / minsecs_str_to_secs(SV_duration.get())  # percentage of 22 minutes (1320 seconds)
    return time_percent * 360


if __name__ == '__main__':
    main()
