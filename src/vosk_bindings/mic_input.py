#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def record_and_infer(device=sd.default.device, samplerate=16000):
    try:
        model = "src/vosk_bindings/model"
    
        if not os.path.exists(model):
            print ("Please download a model for your language from https://alphacephei.com/vosk/models")
            print ("and unpack as 'model' in folder: {}".format(model))
            exit(0)
        device_info = sd.query_devices(device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])
    
        model = vosk.Model(model)
    
    
        with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=device, dtype='int16',
                                channels=1, callback=callback):
                print('#' * 80)
                print('Press Ctrl+C to stop the recording')
                print('#' * 80)
    
                rec = vosk.KaldiRecognizer(model, samplerate)
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        print(rec.Result())

    except KeyboardInterrupt:
        print('\nDone')
        sys.exit(0)
    except Exception as e:
        sys.exit(type(e).__name__ + ': ' + str(e))

if __name__ == "__main__":
    record_and_infer()       