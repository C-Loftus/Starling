from Audio.audio import record
from Desktop.gnome import make_gnome_timer
from multiprocessing import Lock
import model
from Audio.audio import audio_environment

timer_lock = Lock()

audio_environment.set_vol(initialize=True)

while True:
    print("mainthread")
    audio_environment.record_one_phrase()


    output = model.runModel("Assets/recorded.wav")
    for i in output:
        print(i)

    if b'timer' in output:
        p = make_gnome_timer(timer_lock, title="Timer", seconds=5*60)




