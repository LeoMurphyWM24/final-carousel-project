from tkinter import *
from tkinter import ttk

import logging
import threading
import time

from motor import *
from music import *

my_motor = Motor()
my_music = Music()

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

def thread_motor_halfstep(name):
    logging.info("Motor %s: starting", name)
    my_motor.turn_halfstep()
    logging.info("Motor %s: finishing", name)

##def thread_music(name):
##    logging.info("Music %s: starting", name)
##    my_music.on_off()
##    logging.info("Music %s: finishing", name)

def thread_music_on(name):
    logging.info("Music %s: starting", name)
    my_music.turn_on()
    logging.info("Music %s: finishing", name)


def motor_onoff():
    my_motor.on_off()
    if my_motor.is_on():
        # logging.info("Main    : before creating thread")
        x = threading.Thread(target=thread_motor_halfstep, args=(1,))
        logging.info("Main    : before running thread")
        x.start()
        # logging.info("Main    : wait for the thread to finish")
        # x.join()
        logging.info("Main    : all done")

def print_motor():
    print(str(my_motor))
    return


def music_onoff():
    if my_music.is_on():
        my_music.turn_off()
    else:
        music_on()

def music_on():
    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_music_on, args=(2,))
    logging.info("Main    : before running thread")
    x.start()
    # logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")        
        
def music_playpause():
    my_music.play_pause()

def music_skip():
    print("Before skip:", my_music.get_tune())
    my_music.advance_tune()
    print("Skipped to tune", my_music.get_tune())
    music_on()

def music_prev():
    print("Before previous:", my_music.get_tune())
    my_music.decrement_tune()
    print("Returned to tune", my_music.get_tune())
    music_on()
    

window = Tk()
window.geometry("750x500")
window.title("Welcome to Merry G'Round")
  
# Add image file
bg = PhotoImage(file="forest2.png")
canvas1 = Canvas(window, width=750, height=500)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

# Text
canvas1.create_text(390, 40, text = "Welcome", fill="#302000",
                    font="Arial 40 italic bold")
canvas1.create_text(387, 37, text = "Welcome", fill="#ffffff",
                    font="Arial 40 italic bold")
# canvas1.create_text(375, 400, text = "Motor on", fill="#302000",
#                     font="Arial 28 bold")

# Music buttons
b_music_onoff = Button(window, text="Music on/off", command=music_onoff)
cb_music_onoff = canvas1.create_window(100, 100, anchor="nw", window=b_music_onoff)
b_playpause = Button(window, text="Play/Pause", command=my_music.play_pause)
cb_playpause = canvas1.create_window(100, 150, anchor="nw", window=b_playpause)
b_skip = Button(window, text="Next tune", command=music_skip)
cb_skip = canvas1.create_window(100, 200, anchor="nw", window=b_skip)
b_prev = Button(window, text="Previous tune", command=music_prev)
cb_prev = canvas1.create_window(100, 250, anchor="nw", window=b_prev)
b_volumeup = Button(window, text="Volume up", command=my_music.volume_up)
cb_volumeup = canvas1.create_window(100, 315, anchor="nw", window=b_volumeup)
b_volumedown = Button(window, text="Volume down", command=my_music.volume_down)
cb_volumedown = canvas1.create_window(100, 350, anchor="nw", window=b_volumedown)

# Motor buttons
b_startstop = Button(window, text="Motor on/off", command=motor_onoff)
cb_startstop = canvas1.create_window(500, 100, anchor="nw", window=b_startstop)
b_reverse = Button(window, text="Reverse direction", command=my_motor.reverse)
cb_reverse = canvas1.create_window(500, 150, anchor="nw", window=b_reverse)
b_speedup = Button(window, text="Speed up", command=my_motor.speed_up)
cb_speedup = canvas1.create_window(500, 215, anchor="nw", window=b_speedup)
b_slowdown = Button(window, text="Slow down", command=my_motor.speed_down)
cb_slowdown = canvas1.create_window(500, 250, anchor="nw", window=b_slowdown)
# b_motorstatus = Button(window, text="Print motor status", command=print_motor)
# cb_motorstatus = canvas1.create_window(300, 300, anchor="nw", window=b_motorstatus)

window.mainloop()
