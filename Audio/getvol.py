import numpy as np
from numpy.core.fromnumeric import mean
import sounddevice as sd
import collections


class audio_environment:
   curr_vol = collections.deque(maxlen=100)
   init_duration = 2 #in seconds
   init_values = {
      "ambient": 0,
   }

   def record_volume(initialize):
      stream = sd.InputStream(callback=audio_environment._audio_callback)
      if not initialize:
         while(1):
            if audio_environment.get_vol() > audio_environment.init_values["ambient"] + 1:
               import audio
               audio.record()
      if initialize:
         with stream:
           sd.sleep(audio_environment.init_duration * 1000)             
         audio_environment.init_values["ambient"] = audio_environment.get_vol()

   def get_vol():
      return mean(audio_environment.curr_vol)

   def _audio_callback(indata, frames, time, status):
      volume_norm = np.linalg.norm(indata) * 10
      audio_environment.curr_vol.append(volume_norm)

if __name__== "__main__":
   audio_environment.record_volume(True)
   print(audio_environment.get_vol())

