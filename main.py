from Desktop.gnome import make_gnome_timer
from multiprocessing import Lock
import model
from Audio.recording import *

timer_lock = Lock()

set_vol(initialize=True, duration=2000 )

while True:
    print("mainthread")
    record_one_phrase()

    output = model.runModel("Assets/recorded.wav")


    for i in output:
        i = (i.decode("utf-8"))
        print(i, "\n")
        if 'time' in i:
            print("****************** STARTING TIMER ******************")
            p = make_gnome_timer(timer_lock, title="Timer", seconds=5*60)


    if 'time' in output:
        p = make_gnome_timer(timer_lock, title="Timer", seconds=5*60)




