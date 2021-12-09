from os import kill
import numpy as np
from numpy.core.fromnumeric import mean
import sounddevice as sd
import collections
import audio
import threading
from threading import Thread
import time
import numpy as np
from numpy_ringbuffer import RingBuffer

class audio_environment:
   # curr_vol = collections.deque(maxlen=100)

   curr_vol = RingBuffer(capacity=100, dtype=np.float)


   init_duration = 2000 #in milliseconds
   ambient = 0

   def record_one_phrase():
      currentlyRecording = False
      stop_event = threading.Event()
      t = Thread(target=audio.record, args=[stop_event])

      while(1):

         audio_environment.set_vol(initialize=False, duration=10)

         if audio_environment.valid_to_start(currentlyRecording):
            # spawn thread 
            print("starting recording thread")
            t.start()
            currentlyRecording = True
         elif audio_environment.valid_to_stop(currentlyRecording):
            # send signal to stop
            stop_event.set()
            currentlyRecording = False

   def valid_to_start(inProgress, hyperparamVolume = 1):
      return (inProgress == False and \
         (audio_environment.get_vol() > (audio_environment.ambient + hyperparamVolume)))       
   def valid_to_stop(inProgress, hyperparamVolume = 1):
          return (inProgress and \
         (audio_environment.get_vol() < audio_environment.ambient))  

   def set_vol(initialize=False, duration=init_duration):
      stream = sd.InputStream(callback=audio_environment._audio_callback)
      with stream:
         sd.sleep(duration)  
      if initialize:           
         audio_environment.ambient = audio_environment.get_vol()         

   def get_vol():
      return mean(audio_environment.curr_vol)

   def _audio_callback(indata, frames, time, status):
      volume_norm = np.linalg.norm(indata) * 10
      audio_environment.curr_vol.append(volume_norm)

if __name__== "__main__":
   audio_environment.set_vol(initialize=True)
   print(audio_environment.get_vol())
   audio_environment.record_one_phrase()
