import tkinter
import tkinter.font
from tkinter import *
import pyglet as pyglet
from pyautogui import *
import time

root = Tk()
root.title('Waypoint Timer')
window_width = 200
window_height = 350
root.geometry(f'{window_width}x{window_height}+2220+300')
# root.geometry(f'{window_width}x{window_height}+1500+100')
root.attributes('-alpha', 0.95)

ringring = Canvas(root, width=300, height=300, bg='#999999')
arc = ringring.create_arc(50, 50, 200, 200)  # start=0, extent=0, fill='#4477ff', style=ARC)

IV_start_time = IntVar()
IV_start_time.set(0)
RV_map = IntVar()
SV_time_passed = StringVar()
SV_time_remaining = StringVar()
DV_radial_degree = DoubleVar()
DV_radial_degree.set(0)

start_time = 0
end_time = 60 * 22  # 22 minutes for the ring to close completely

tokking = False

w_graphic = tkinter.Toplevel()

pyglet.font.add_file('Digital_Dismay.otf')  # Your TTF file name here
DigiDismay = tkinter.font.Font(family='Digital Dismay', size=30, weight='normal')

# TODO: This shit broke, rounds too strongly. Fix it.
timer_scale = 0.9


def main():
    """
    Window that launches the graphic timer when the trigger is met.
    """
    w_graphic.destroy()

    # widget creation
    l_row1 = Label(root, text='Start time (s):')
    e_start_time = Entry(root, textvariable=IV_start_time, relief='sunken', bd=5, width=10)

    b_start = Button(root, text='Start Timer', command=graphic_window)
    b_end = Button(root, text='End Timer', command=finish)

    l_2a = Label(root, text='Time Passed:')
    l_2b = Label(root, textvariable=SV_time_passed)

    l_3a = Label(root, text='Time Remaining:')
    l_3b = Label(root, textvariable=SV_time_remaining)

    l_4a = Radiobutton(root, variable=RV_map, value=0, text="Kings Canyon")
    l_5a = Radiobutton(root, variable=RV_map, value=1, text="World's Edge")
    l_6a = Radiobutton(root, variable=RV_map, value=2, text="Olympus")
    l_7a = Radiobutton(root, variable=RV_map, value=3, text="Storm Point")

    l_8a = Label(root, text="""
    While this window is open, the
    timer is scanning your screen
    for match start/end triggers.
    Closing this window exits
    the application. Minimizing
    this window will not interfere
    with the program's function.""")

    # widget placement
    num_rows = 4
    vert_spacing = 26
    l_row1.place(x=window_width/2, y=vert_spacing*0, anchor=NE)
    e_start_time.place(x=window_width/2, y=vert_spacing*0, anchor=NW)
    b_start.place(x=window_width/2, y=vert_spacing*1, anchor=NE)
    b_end.place(x=window_width/2, y=vert_spacing*1, anchor=NW)
    l_2a.place(x=window_width/2, y=vert_spacing*2, anchor=NE)
    l_2b.place(x=window_width/2, y=vert_spacing*2, anchor=NW)
    l_3a.place(x=window_width/2, y=vert_spacing*3, anchor=NE)
    l_3b.place(x=window_width/2, y=vert_spacing*3, anchor=NW)
    l_4a.place(x=35, y=vert_spacing*4, anchor=NW)
    l_5a.place(x=35, y=vert_spacing*5, anchor=NW)
    l_6a.place(x=35, y=vert_spacing*6, anchor=NW)
    l_7a.place(x=35, y=vert_spacing*7, anchor=NW)
    l_8a.place(x=window_width/2, y=vert_spacing*8, anchor=N)

    # e_start_time.focus()
    root.bind(sequence='<Return>', func=graphic_window)

    # starts loop to scan for triggers outside mainloop
    root.after(2000, trigger_scanner)
    # starts mainloop
    root.mainloop()


def graphic_window(event=''):
    """
    Graphic timer that tracks the timing of events throughout an Apex Legends BR game.
    """
    global start_time, arc, ringring, tokking, w_graphic, end_time

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

    start_time = time.time() - IV_start_time.get()
    ringring = Canvas(w_graphic, width=300, height=300, bg=transparent)
    coords = 350-(300*timer_scale), 350-(300*timer_scale), (300*timer_scale)-50, (300*timer_scale)-50
    arc = ringring.create_arc(coords, start=90, extent=0, fill='#4477ff', style=ARC, outline='#4477ff', width=20)

    l_elapsed = Label(w_graphic, textvariable=SV_time_passed, bg=transparent, font=DigiDismay, fg='black')

    ringring.itemconfig(arc, fill='#4477ff', extent=0)
    end_time = start_time + (60 * 22)
    if not tokking:
        tokking = True
        tock(root)

    waypoint(5*60+20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
    waypoint(12*60+16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
    # waypoint(15*60+0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00

    if RV_map.get() == 0:
        waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        waypoint(15 * 60 + 0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00
        # King's Canyon
        waypoint(3*60+50, duration=3*60+40, color='#ff9900', text='Round 1 Ring')  # 3:50,to 3:40 duration
        waypoint(10*60+25, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # 10:25 to, 1:15 seconds
        waypoint(15*60, duration=45, color='#ff9900', text='Round 3 Ring')  # , 45 seconds
        waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # to , 40 seconds
        waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # to , 40 seconds
        waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # to , 2 minute duration
    elif RV_map.get() == 1:
        waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        waypoint(15*60+0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00
        # World's Edge
        waypoint(3*60+54, duration=4*60+16, color='#ff9900', text='Round 1 Ring')  # ,to 4:16 duration
        waypoint(10*60+30, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # 10:30 to 11:45 1:15 seconds
        waypoint(15*60, duration=45, color='#ff9900', text='Round 3 Ring')  # , 45 seconds
        waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # to , 40 seconds
        waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # to , 40 seconds
        waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # to , 2 minutes
    elif RV_map.get() == 2:
        waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        waypoint(15*60+0, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:00
        # Olympus
        waypoint(4*60+5, duration=4*60+16, color='#ff9900', text='Round 1 Ring')  # ,to 4:16 duration
        waypoint(11*60+20, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # to, 1:15 seconds
        waypoint(14*60+15, duration=45, color='#ff9900', text='Round 3 Ring')  # 14:15, 45 seconds
        waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # to , 40 seconds
        waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # to , 40 seconds
        waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # to , 2 minutes
    elif RV_map.get() == 3:
        waypoint(5 * 60 + 20, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 5:20
        waypoint(12 * 60 + 16, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 12:16
        waypoint(15*60+45, duration=10, color='#d1c767', text='Care Package', width=20)  # care package 15:45
        # Storm Point
        waypoint(3*60+54, duration=4*60+16, color='#ff9900', text='Round 1 Ring')  # 3:54 to 8:10, 4:16 duration
        waypoint(11*60+20, duration=1*60+15, color='#ff9900', text='Round 2 Ring')  # 11:20 to 12:35, 1:15 seconds
        waypoint(15*60, duration=45, color='#ff9900', text='Round 3 Ring')  # 15:00 to 15:45, 45 seconds
        waypoint(17*60+45, duration=40, color='#ff9900', text='Round 4 Ring')  # 17:45(18:00?) to 16:04, 40 seconds
        waypoint(19*60+10, duration=40, color='#ff9900', text='Round 5 Ring')  # 19:10(?) to 19:50, 40 seconds
        waypoint(20*60, duration=2*60, color='#ff9900', text='Final Ring')  # 20:00(?) to 22:00, 2 minutes

    # widget placement
    num_rows = 4
    vert_spacing = 26
    ringring.place(x=graphic_width/2, y=vert_spacing*0, anchor=N)
    l_elapsed.place(x=graphic_width/2, y=graphic_height/2, anchor=CENTER)

    # starts graphic window mainloop
    # root.after(2000, trigger_scanner)
    w_graphic.mainloop()


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
    time_percent = seconds / 1320  # percentage of 22 minutes (1320 seconds)
    return time_percent * 360


if __name__ == '__main__':
    main()
