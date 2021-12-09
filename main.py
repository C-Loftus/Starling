from Audio.audio import record
from Desktop.gnome import make_gnome_timer
from multiprocessing import Lock
import Audio
import model

timer_lock = Lock()


while True:
    print("mainthread")
    wf = record()
    output = model.runModel("Assets/recorded.wav")
    
    if b'timer' in output:
        p = make_gnome_timer(timer_lock, title="Timer", seconds=5*60)
        # p.join()




