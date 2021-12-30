import pyaudio
import wave
from numpy.core.fromnumeric import mean
import sounddevice as sd
import threading
from threading import Thread
import numpy as np
from numpy_ringbuffer import RingBuffer
from playsound import playsound 
import queue

#  Stores information about the audio environment
class env:
   curr_vol = RingBuffer(capacity=100, dtype=float)
   init_duration = 5000 #in milliseconds
   ambient = 0.0
   start_hyperparameter=2 # the bigger the hyperparameter, the louder the env has to be to start
   stop_hyperparameter=0.25 # the bigger the hyperparameter, louder it will be to stop

   # pyaudio config
   chunk = 1024
   FORMAT = pyaudio.paInt16
   channels = 1 # mono, change to 2 if you want stereo
   sample_rate = 16000

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




def record_finish(event, frames):
   filename = "Assets/recorded.wav"
   record_seconds = 3 # max length
   p = pyaudio.PyAudio()
   # open stream object as input & output
   stream = p.open(format=env.FORMAT,
                   channels=env.channels,
                   rate=env.sample_rate,
                   input=True,
                   output=True,
                   frames_per_buffer=env.chunk)
   for i in range(int(env.sample_rate / env.chunk * record_seconds)):
      if event.is_set():
         break
      data = stream.read(env.chunk)
      frames.append(data)
      print("appending frames")
   stream.stop_stream()
   stream.close()
   p.terminate()
   wf = wave.open(filename, "wb")
   wf.setnchannels(env.channels)
   wf.setsampwidth(p.get_sample_size(env.FORMAT))
   wf.setframerate(env.sample_rate)
   wf.writeframes(b"".join(frames))
   wf.close()
   print("finished recording")       


def record_background(stop_signal, q):
   while(True):
      frames = []
      record_seconds = 2 
      p = pyaudio.PyAudio()
      stream = p.open(format=env.FORMAT,
                     channels=env.channels,
                     rate=env.sample_rate,
                     input=True,
                     output=True,
                     frames_per_buffer=env.chunk)
      
      for i in range(int(env.sample_rate / env.chunk * record_seconds)):
         data = stream.read(env.chunk)
         frames.append(data)

      stream.stop_stream()
      stream.close()
      p.terminate()
      if stop_signal.is_set():
         q.put(frames)
         return frames



def record_one_phrase():
   q = queue.Queue()
   background_listener_stop = threading.Event()
   background_listener = Thread(target=record_background, args=[background_listener_stop, q])
   # background_listener.setDaemon(True)

   currentlyRecording = False
   stop_event = threading.Event()

   background_listener.start()

   print(f'{env.ambient=}{env.get_vol()=}')
   while(True):

      env.set_vol(duration=10)

      if env.valid_to_start() and not currentlyRecording:
         if background_listener.is_alive():
            print("joining background thread")
            background_listener_stop.set()
            # background_listener.join() # causes to return {} ?
         frames = q.get()
         main_recorder = Thread(target=record_finish, args=[stop_event, frames])
         
         # spawn thread 
         print("starting recording thread")
         main_recorder.start()
         currentlyRecording = True
      elif env.valid_to_stop() and currentlyRecording:
         # send signal to stop
         print("stopping recording thread. *************** Finished Word")
         stop_event.set()
         main_recorder.join()
         currentlyRecording = False
         return
      

if __name__== "__main__":
   env.set_vol(initialize=True)
   record_one_phrase()
   import time
   time.sleep(1)
   playsound("Assets/recorded.wav")

