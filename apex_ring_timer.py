from tkinter import *
from pyautogui import *
import time
import keyboard
import win32api
import win32con
from pynput.keyboard import *
# import Pillow

root = Tk()
window_width = 300
window_height = 400
root.geometry(f'{window_width}x{window_height}+1915+269')
root.attributes('-alpha', 0.95)

ringring = Canvas(root, width=300, height=300, bg='#999999')
arc = ringring.create_arc(50, 50, 200, 200)  # start=0, extent=0, fill='#4477ff', style=ARC)

IV_start_time = IntVar()
IV_start_time.set(0)
SV_time_passed = StringVar()
SV_time_remaining = StringVar()
DV_radial_degree = DoubleVar()
DV_radial_degree.set(0)

start_time = 0
end_time = 60 * 22  # 22 minutes for the ring to close completely

tokking = False


def main():
    """
    Graphic timer that tracks the timing of events throughout an Apex Legends BR game.
    """
    global start_time, arc, ringring
    # todone: get a functioning timer- counts up to 20 min and down from 20 min.
    # todone: get a functioning circle timer

    # if keyboard.is_pressed('alt+;')

    # with Listener(on_press=press_on) as hotk:
    #     hotk.join()

    # widget creation
    l_row1 = Label(root, text='Start time (s):')
    e_start_time = Entry(root, textvariable=IV_start_time, relief='sunken', bd=5)

    b_start = Button(root, text='Start Timer', command=start)

    l_2a = Label(root, text='Time Passed:')
    l_2b = Label(root, textvariable=SV_time_passed)

    l_3a = Label(root, text='Time Remaining:')
    l_3b = Label(root, textvariable=SV_time_remaining)

    ringring = Canvas(root, width=300, height=300, bg='#999999')
    arc = ringring.create_arc(50, 50, 250, 250, start=90, extent=0, fill='#4477ff',
                              style=ARC, outline='#4477ff', width=20)

    # todo: functioning waypoints
    # waypoint(0, color='#000000', text='Round 1', size=15)
    # waypoint(405, color='#000000', text='Round 2')

    waypoint(5*60+20, duration=10, color='#d1c767', text='Care Package', size=20)  # care package 5:20
    waypoint(12*60+16, duration=10, color='#d1c767', text='Care Package', size=20)  # care package 12:16
    waypoint(15*60+0, duration=10, color='#d1c767', text='Care Package', size=20)  # care package 15:00

    # waypoint(4*60+4, duration=4*60+5, color='#ff9900', text='Round 1 Ring')  # 4:04 to 8:10
    waypoint(3*60+54, duration=4*60+16, color='#ff9900', text='Round 1 Ring')  # 3:54 to 8:10
    waypoint(11*60+20, duration=(12*60+40)-(11*60+4), color='#ff9900', text='Round 2 Ring')  # 11:04 to 12:40
    waypoint(14*60+54, duration=45, color='#ff9900', text='Round 3 Ring')  # 11:54 to ?:??
    waypoint(940, duration=(16*60+4)-940, color='#ff9900', text='Round 4 Ring')  # 14:54 to 16:04
    waypoint(19*60, duration=50, color='#ff9900', text='Round 5 Ring')  # ?:?? to 19:50
    waypoint(1130, duration=120, color='#ff9900', text='Final Ring')  # ?:?? to ?:??

    # widget placement
    num_rows = 4
    vert_spacing = 26
    l_row1.place(x=window_width/2, y=vert_spacing*0, anchor=NE)
    e_start_time.place(x=window_width/2, y=vert_spacing*0, anchor=NW)
    b_start.place(x=window_width/2, y=vert_spacing*1, anchor=N)
    l_2a.place(x=window_width/2, y=vert_spacing*2, anchor=NE)
    l_2b.place(x=window_width/2, y=vert_spacing*2, anchor=NW)
    l_3a.place(x=window_width/2, y=vert_spacing*3, anchor=NE)
    l_3b.place(x=window_width/2, y=vert_spacing*3, anchor=NW)
    ringring.place(x=window_width/2, y=vert_spacing*4, anchor=N)

    # keep window on top
    root.wm_attributes("-topmost", 1)

    # e_start_time.focus()
    root.bind(sequence='<Return>', func=start)

    # starts loop to scan for triggers outside mainloop
    root.after(2000, startcheck)
    # starts mainloop
    root.mainloop()


def startcheck():
    """
    loop that runs alongside tkinter mainloop, to check whether the conditions are right to start the timer.
    """
    # print('ears')

    # check for "00" initial countdown timer
    if locateOnScreen('apex_timer_trigger.jpg', region=(950, 200, 70, 150), confidence=0.9) is not None:
        print('there it is!')
        start()
    # else:
    #     print('its not here')

    if keyboard.is_pressed('l'):
        start()
    # continue looping the check
    root.after(1000, startcheck)


def start(event=''):
    global start_time, end_time, tokking

    start_time = time.time() - IV_start_time.get()
    ringring.itemconfig(arc, fill='#999999', extent=357)
    # ringring.itemconfig(arc, extent=0)
    ringring.itemconfig(arc, fill='#4477ff', extent=0)
    end_time = start_time + (60 * 22)
    if not tokking:
        tokking = True
        tock()


def tock(event=''):
    """
    'Tick, tock, tick, tock...' Updates the timer visual.
    """
    global arc, ringring
    SV_time_passed.set('{:02d}:{:02d}'.format(
        int((time.time() - start_time) / 60),  # minutes
        int((time.time() - start_time) % 60)  # seconds
            ))
    SV_time_remaining.set('{:02d}:{:02d}'.format(
        int((end_time - time.time()) / 60),  # minutes
        int((end_time - time.time()) % 60)  # seconds
            ))

    meter_radians = seconds_to_radians(time.time() - start_time)  # elapsed time in radians
    ringring.itemconfig(arc,
                        extent=-seconds_to_radians(time.time() - start_time))
    # if timer isn't finished, keep tocking.
    if end_time - time.time() > 0:
        root.after(1000, tock)


def waypoint(placement, duration=5, color='#000000', size=5, text='', label_font=("Helvetica", "10", "bold italic")):
    """
    method that sets a point along the arc to mark an event.
    places a label, anchored SW for 0-90°, NW for 91-180°, etc.
    """
    position = seconds_to_radians(placement)
    waypoint_arc = ringring.create_arc(50, 50, 250, 250,
                                       start=90-seconds_to_radians(placement), extent=-seconds_to_radians(duration),
                                       fill='#4477ff', style=ARC, outline=color, width=size)


def seconds_to_radians(seconds):
    time_percent = seconds / 1320  # percentage of 22 minutes (1320 seconds)
    return time_percent * 360


if __name__ == '__main__':
    main()
