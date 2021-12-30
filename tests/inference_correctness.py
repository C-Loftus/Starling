import sys
import os
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
  

from Audio.recording import *
from nvidia.transcribe_speech import *
from setup_conf import application_config

def init_conf_and_env():
    env.set_vol(initialize=True)
    config_path = "config.yaml"
    application_config(config_path)
    t = init_transcribe_conf(TranscriptionConfig)
    return t
    

def infer_5():
    model = init_conf_and_env()

    TORCH_CAST = model[0]
    ASR_MODEL = model[1]
    FILEPATHS = model[2]
    BATCH_SIZE = model[3]


    transcriptions = run_inference(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE)
    print(transcriptions)

if __name__ == '__main__':
    a =os.path.abspath(__file__)
    print(a)
    infer_5()