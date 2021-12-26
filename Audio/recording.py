import pyaudio
import wave
from numpy.core.fromnumeric import mean
import sounddevice as sd
import threading
from threading import Thread
import numpy as np
from numpy_ringbuffer import RingBuffer


#  Stores information about the audio environment
class env:
   curr_vol = RingBuffer(capacity=50, dtype=float)
   init_duration = 5000 #in milliseconds
   ambient = 0.0
   frames=[]
   start_hyperparameter=2 # the bigger the hyperparameter, the louder the env has to be to start
   stop_hyperparameter=0.25 # the bigger the hyperparameter, louder it will be to stop

   def get_vol():
      return mean(env.curr_vol)
   
   def valid_to_start():
      return (env.get_vol() > (env.ambient * env.start_hyperparameter))       
   def valid_to_stop(hyperparamVolume = 2):
      return (env.get_vol() < (env.ambient + env.stop_hyperparameter))

   def set_vol(initialize=False, duration=init_duration):
      stream = sd.InputStream(callback=env._audio_callback)
      with stream:
         sd.sleep(duration)  
      if initialize:      
         env.ambient = env.get_vol()

   def _audio_callback(indata, frames, time, status):
      volume_norm = np.linalg.norm(indata) * 10
      env.curr_vol.append(volume_norm)




def record_finish(event):
   filename = "Assets/recorded.wav"
   chunk = 1024
   FORMAT = pyaudio.paInt16
   channels = 1
   sample_rate = 16000
   record_seconds = 5 # max length
   p = pyaudio.PyAudio()
   # open stream object as input & output
   stream = p.open(format=FORMAT,
                   channels=channels,
                   rate=sample_rate,
                   input=True,
                   output=True,
                   frames_per_buffer=chunk)
   frames = env.frames
   for i in range(int(16000 / chunk * record_seconds)):
      if event.is_set():
            break
      data = stream.read(chunk)
      frames.append(data)
   stream.stop_stream()
   stream.close()
   p.terminate()
   wf = wave.open(filename, "wb")
   wf.setnchannels(channels)
   wf.setsampwidth(p.get_sample_size(FORMAT))
   wf.setframerate(sample_rate)
   wf.writeframes(b"".join(frames))
   wf.close()
   print("finished recording")       


def record_intermed(bf_stop):
   frames = []
   while(True):
      chunk = 1024
      FORMAT = pyaudio.paInt16
      channels = 1 # mono, change to 2 if you want stereo
      sample_rate = 16000
      record_seconds = 10
      p = pyaudio.PyAudio()
      stream = p.open(format=FORMAT,
                     channels=channels,
                     rate=sample_rate,
                     input=True,
                     output=True,
                     frames_per_buffer=chunk)
      
      for i in range(int(16000 / chunk * record_seconds)):
         data = stream.read(chunk)
         frames.append(data)
      env.frames = frames 

      stream.stop_stream()
      stream.close()
      p.terminate()
      if bf_stop.is_set():
         return



def record_one_phrase():
   background_listener_stop = threading.Event()
   background_listener = Thread(target=record_intermed, args=[background_listener_stop])

   currentlyRecording = False
   stop_event = threading.Event()

   background_listener.start()

   print(f'{env.ambient=}{env.get_vol()=}')
   while(True):
      # print(f'{env.ambient=}{get_vol()=}')

      env.set_vol(initialize=False, duration=10)

      if env.valid_to_start() and not currentlyRecording:
         if background_listener.is_alive():
            print("joining")
            background_listener_stop.set()
         main_recorder = Thread(target=record_finish, args=[stop_event])
         
         # spawn thread 
         print("starting recording thread")
         main_recorder.start()
         currentlyRecording = True
      elif env.valid_to_stop() and currentlyRecording:
         # send signal to stop
         print("stopping recording thread. *************** Finished Word")
         stop_event.set()
         env.frames = []
         currentlyRecording = False
         return
      

if __name__== "__main__":
   env.set_vol(initialize=True)
   record_one_phrase()

