import tkinter
import tkinter.font
from tkinter import *
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
root.geometry(f'{window_width}x{window_height}+2220+300')
# root.geometry(f'{window_width}x{window_height}+1500+100')
root.attributes('-alpha', 0.95)

ringring = Canvas(root, width=300, height=300, bg='#999999')
arc = ringring.create_arc(50, 50, 200, 200)  # start=0, extent=0, fill='#4477ff', style=ARC)

SV_profile = StringVar()
SV_profile.set('Default')
SV_start_time = StringVar()
SV_start_time.set('00:00')
SV_duration = StringVar()
SV_duration.set('22:00')
RV_map = IntVar()
SV_time_passed = StringVar()
SV_time_remaining = StringVar()
DV_radial_degree = DoubleVar()
DV_radial_degree.set(0)
SV_waypoints = StringVar()
e_waypoints = Text(root, height=50, width=20, relief='sunken')

openpng = PIL.ImageTk.PhotoImage(PIL.Image.open('./open.png'))
b_open = Menubutton(root, direction='right', relief='flat', image=openpng)


start_time = 0
end_time = 60 * 22  # 22 minutes for the ring to close completely

tokking = False

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

    playpause = PIL.ImageTk.PhotoImage(PIL.Image.open('./playpause.png'))
    stop = PIL.ImageTk.PhotoImage(PIL.Image.open('./stop.png'))
    save = PIL.ImageTk.PhotoImage(PIL.Image.open('./save.png'))

    # widget creation
    populate_open_menu()
    e_profile = Entry(root, textvariable=SV_profile, relief='sunken', bd=2, width=20)
    b_save = Button(root, image=save, command=save_profile, relief='flat')
    b_trash = Button(root, image=save, command=save_profile, relief='flat')

    l_duration = Label(root, text='Duration:')
    e_duration = Entry(root, textvariable=SV_duration, relief='sunken', bd=2, width=10)

    b_play = Button(root, image=playpause, command=graphic_window, relief='flat')
    b_stop = Button(root, image=stop, command=finish, relief='flat')

    l_2a = Label(root, text='Time Passed:')
    e_2b = Entry(root, textvariable=SV_start_time, relief='sunken', bd=2, width=5)

    l_3a = Label(root, text='Remaining:')
    l_3b = Label(root, textvariable=SV_time_remaining)

    l_4a = Label(root, text="Waypoints")
    # e_waypoints = Text(root, height=50, width=20, relief='sunken')

    # widget placement
    num_rows = 9
    vert_spacing = 26
    b_open.place(x=10, y=vert_spacing*0, anchor=NW)
    e_profile.place(x=45, y=vert_spacing*0, anchor=NW)
    b_save.place(x=window_width-23, y=vert_spacing*0, anchor=NW)

    l_duration.place(x=window_width/2, y=vert_spacing*1, anchor=NE)
    e_duration.place(x=window_width/2, y=vert_spacing*1, anchor=NW)
    b_play.place(x=window_width/2, y=vert_spacing*2-8, anchor=NE)
    b_stop.place(x=window_width/2, y=vert_spacing*2-8, anchor=NW)
    l_2a.place(x=window_width/2, y=vert_spacing*3, anchor=NE)
    e_2b.place(x=window_width/2, y=vert_spacing*3, anchor=NW)
    l_3a.place(x=window_width/2, y=vert_spacing*4, anchor=NE)
    l_3b.place(x=window_width/2, y=vert_spacing*4, anchor=NW)
    l_4a.place(x=35, y=vert_spacing*5, anchor=NW)
    e_waypoints.place(x=20, y=vert_spacing*6, anchor=NW)

    # e_start_time.focus()
    # root.bind(sequence='<Return>', func=graphic_window)
    # root.bind(sequence='<Return>', func=save_profile)

    # starts loop to scan for triggers outside mainloop
    root.after(2000, trigger_scanner)
    # starts mainloop
    root.mainloop()
    # e_waypoints.insert(INSERT, "5:20\n"
    #                            "12:16\n"
    #                            "15:45\n"
    #                            "3:54-8:10\n"
    #                            "11:20-12:35\n"
    #                            "15:00-15:45\n"
    #                            "17:45-16:04\n"
    #                            "19:10-19:50\n"
    #                            "20:00-22:00")


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

    start_time = time.time() - minsecs_str_to_secs(SV_start_time.get())

    ringring = Canvas(w_graphic, width=300, height=300, bg=transparent)
    coords = 350-(300*timer_scale), 350-(300*timer_scale), (300*timer_scale)-50, (300*timer_scale)-50
    arc = ringring.create_arc(coords, start=90, extent=0, fill='#4477ff', style=ARC, outline='#4477ff', width=20)

    l_elapsed = Label(w_graphic, textvariable=SV_time_passed, bg=transparent, font=DigiDismay, fg='black')

    ringring.itemconfig(arc, fill='#4477ff', extent=0)
    end_time = start_time + minsecs_str_to_secs(SV_duration.get())
    if not tokking:
        tokking = True
        tock(root)

        # waypoint(5*60+20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        # waypoint(12*60+16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        # waypoint(15*60+0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00

        # if RV_map.get() == 0:
        #     waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        #     waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        #     waypoint(15 * 60 + 0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00
        #     # King's Canyon
        #     waypoint(1*60+50, duration=3*60+40, color='#ff9900', text='Round 1 Ring')  # 3:50,to 3:40 duration
        #     waypoint(10*60+25, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # 10:25 to, 1:15 seconds
        #     waypoint(15*60, duration=45, color='#ff9900', text='Round 3 Ring')  # , 45 seconds
        #     waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # to , 40 seconds
        #     waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # to , 40 seconds
        #     waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # to , 2 minute duration
        # elif RV_map.get() == 1:
        #     waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        #     waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        #     waypoint(15*60+0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00
        #     # World's Edge
        #     waypoint(3*60+54, duration=4*60+16, color='#ff9900', text='Round 1 Ring')  # ,to 4:16 duration
        #     waypoint(10*60+30, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # 10:30 to 11:45 1:15 seconds
        #     waypoint(15*60, duration=45, color='#ff9900', text='Round 3 Ring')  # , 45 seconds
        #     waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # to , 40 seconds
        #     waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # to , 40 seconds
        #     waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # to , 2 minutes
        # elif RV_map.get() == 2:
        #     waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        #     waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        #     waypoint(15*60+0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00
        #     # Olympus
        #     waypoint(4*60+5, duration=4*60+16, color='#ff9900', text='Round 1 Ring')  # ,to 4:16 duration
        #     waypoint(11*60+20, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # to, 1:15 seconds
        #     waypoint(14*60+15, duration=45, color='#ff9900', text='Round 3 Ring')  # 14:15, 45 seconds
        #     waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # to , 40 seconds
        #     waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # to , 40 seconds
        #     waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # to , 2 minutes
        # elif RV_map.get() == 3:
        #     waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        #     waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        #     waypoint(15*60+45, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:45
        #     # Storm Point
        #     waypoint(3*60+54, duration=4*60+16, color='#ff9900', text='Round 1 Ring')  # 3:54 to 8:10, 4:16 duration
        #     waypoint(11*60+20, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # 11:20 to 12:35, 1:15 seconds
        #     waypoint(15*60, duration=45, color='#ff9900', text='Round 3 Ring')  # 15:00 to 15:45, 45 seconds
        #     waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # 17:45(18:00?) to 16:04, 40 seconds
        #     waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # 19:10(?) to 19:50, 40 seconds
        #     waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # 20:00(?) to 22:00, 2 minutes

    # parse text into waypoints
    waypoints_entry_lines = re.split('\n', e_waypoints.get(1.0, "end-1c"))
    for line in waypoints_entry_lines:
        times = re.findall('(\d+:\d+)', line)
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


def populate_open_menu():
    b_open.menu = Menu(b_open, tearoff=0)
    b_open["menu"] = b_open.menu
    saved_profiles = os.listdir('wp_profiles')
    for profile in saved_profiles:
        b_open.menu.add_command(label=profile[:-4], command=lambda x=profile[:-4]: load_profile(f'{x}'))
    return


def save_profile():
    with open(f'wp_profiles/{SV_profile.get()}.txt', 'w') as file:
        file.write(e_waypoints.get(1.0, "end-1c"))
    populate_open_menu()
    return


def load_profile(profile=SV_profile.get()):
    SV_profile.set(profile)
    e_waypoints.delete(1.0, "end")
    with open(f'wp_profiles/{profile}.txt', 'r') as file:
        e_waypoints.insert(INSERT, file.read())
    return


def trash_profile(profile=SV_profile.get()):
    return os.remove(f'wp_profiles/{profile}.txt')


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
    tokking = False


def tock(event='', window=root):
    """
    'Tick, tock, tick, tock...' Updates the timer visual.
    """
    global arc, ringring, tokking
    # if timer isn't finished, keep tocking.
    if end_time - time.time() < 0:
        finish()
    else:
        SV_time_passed.set('{:02d}:{:02d}'.format(
            int((time.time() - start_time) / 60),  # minutes
            int((time.time() - start_time) % 60)  # seconds
                ))
        SV_time_remaining.set('{:02d}:{:02d}'.format(
            int((end_time - time.time()) / 60),  # minutes
            int((end_time - time.time()) % 60)  # seconds
                ))
        SV_start_time.set('{:02d}:{:02d}'.format(
            int((time.time() - start_time) / 60),  # minutes
            int((time.time() - start_time) % 60)  # seconds
                ))

        # meter_radians = seconds_to_radians(time.time() - start_time)  # elapsed time in radians
        ringring.itemconfig(arc,
                            extent=-seconds_to_radians(time.time() - start_time))
        window.after(1000, tock)


def waypoint(placement, duration=5, color='#000000', width=5, text='', label_font=("Helvetica", "10", "bold italic")):
    """
    method that sets a point along the arc to mark an event.
    places a label, anchored SW for 0-90°, NW for 91-180°, etc.
    """
    coords = 350-(300*timer_scale), 350-(300*timer_scale), (300*timer_scale)-50, (300*timer_scale)-50
    waypoint_arc = ringring.create_arc(coords, fill='#4477ff', style=ARC, outline=color, width=width,
                                       start=90-seconds_to_radians(placement), extent=-seconds_to_radians(duration))


def seconds_to_radians(seconds):
    time_percent = seconds / minsecs_str_to_secs(SV_duration.get())  # percentage of 22 minutes (1320 seconds)
    return time_percent * 360


if __name__ == '__main__':
    main()
