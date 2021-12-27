# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import glob
import json
import os
from dataclasses import dataclass
from typing import Optional

import pytorch_lightning as pl
import torch
from omegaconf import OmegaConf

from nemo.collections.asr.metrics.rnnt_wer import RNNTDecodingConfig
from nemo.collections.asr.models import ASRModel
from nemo.core.config import hydra_runner
from nemo.utils import logging, model_utils
from torch._C import TupleType, autocast_decrement_nesting


"""
Transcribe audio file on a single CPU/GPU. Useful for transcription of moderate amounts of audio data.
# Arguments
  model_path: path to .nemo ASR checkpoint
  pretrained_name: name of pretrained ASR model (from NGC registry)
  audio_dir: path to directory with audio files
  dataset_manifest: path to dataset JSON manifest file (in NeMo format)
  
  output_filename: Output filename where the transcriptions will be written
  batch_size: batch size during inference
  
  cuda: Optional int to enable or disable execution of model on certain CUDA device.
  amp: Bool to decide if Automatic Mixed Precision should be used during inference
  audio_type: Str filetype of the audio. Supported = wav, flac, mp3
  
  overwrite_transcripts: Bool which when set allowes repeated transcriptions to overwrite previous results.
  
  rnnt_decoding: Decoding sub-config for RNNT. Refer to documentation for specific values.
# Usage
ASR model can be specified by either "model_path" or "pretrained_name".
Data for transcription can be defined with either "audio_dir" or "dataset_manifest".
Results are returned in a JSON manifest file.
python transcribe_speech.py \
    model_path=null \
    pretrained_name=null \
    audio_dir="" \
    dataset_manifest="" \
    output_filename="" \
    batch_size=32 \
    cuda=0 \
    amp=True
"""


@dataclass
class TranscriptionConfig:
    # Required configs
    model_path: Optional[str] = None  # Path to a .nemo file
    pretrained_name: Optional[str] = None  # Name of a pretrained model
    audio_dir: Optional[str] = None  # Path to a directory which contains audio files
    dataset_manifest: Optional[str] = None  # Path to dataset's JSON manifest

    # General configs
    output_filename: Optional[str] = None
    batch_size: int = 32

    # Set `cuda` to int to define CUDA device. If 'None', will look for CUDA
    # device anyway, and do inference on CPU only if CUDA device is not found.
    # If `cuda` is a negative number, inference will be on CPU only.
    cuda: Optional[int] = None
    amp: bool = False
    audio_type: str = "wav"

    # Recompute model transcription, even if the output folder exists with scores.
    overwrite_transcripts: bool = True

    # Decoding strategy for RNNT models
    rnnt_decoding: RNNTDecodingConfig = RNNTDecodingConfig()


# @hydra_runner(config_name="TranscriptionConfig", schema=TranscriptionConfig)
def init_transcribe_conf(cfg: TranscriptionConfig):
    logging.info(f'Hydra config: {OmegaConf.to_yaml(cfg)}')

    if cfg.model_path is None and cfg.pretrained_name is None:
        raise ValueError("Both cfg.model_path and cfg.pretrained_name cannot be None!")
    if cfg.audio_dir is None and cfg.dataset_manifest is None:
        raise ValueError("Both cfg.audio_dir and cfg.dataset_manifest cannot be None!")

    # setup GPU
    if cfg.cuda is None:
        if torch.cuda.is_available():
            cfg.cuda = 0  # use 0th CUDA device
        else:
            cfg.cuda = -1  # use CPU

    device = torch.device(f'cuda:{cfg.cuda}' if cfg.cuda >= 0 else 'cpu')

    # setup model
    if cfg.model_path is not None:
        # restore model from .nemo file path
        model_cfg = ASRModel.restore_from(restore_path=cfg.model_path, return_config=True)
        classpath = model_cfg.target  # original class path
        imported_class = model_utils.import_class_by_path(classpath)  # type: ASRModel
        logging.info(f"Restoring model : {imported_class.__name__}")
        asr_model = imported_class.restore_from(restore_path=cfg.model_path, map_location=device)  # type: ASRModel
        model_name = os.path.splitext(os.path.basename(cfg.model_path))[0]
    else:
        # restore model by name
        asr_model = ASRModel.from_pretrained(model_name=cfg.pretrained_name, map_location=device)  # type: ASRModel
        model_name = cfg.pretrained_name

    # trainer = pl.Trainer(gpus=[cfg.cuda] if cfg.cuda >= 0 else 0)
    # asr_model.set_trainer(trainer)
    asr_model = asr_model.eval()


    # Setup decoding strategy
    if hasattr(asr_model, 'change_decoding_strategy'):
        asr_model.change_decoding_strategy(cfg.rnnt_decoding)

    # get audio filenames
    if cfg.audio_dir is not None:
        filepaths = list(glob.glob(os.path.join(cfg.audio_dir, f"*.{cfg.audio_type}")))
    else:
        # get filenames from manifest
        filepaths = []
        with open(cfg.dataset_manifest, 'r') as f:
            for line in f:
                item = json.loads(line)
                filepaths.append(item['audio_filepath'])
    logging.info(f"\nTranscribing {len(filepaths)} files...\n")

    # setup AMP (optional)
    if cfg.amp and torch.cuda.is_available() and hasattr(torch.cuda, 'amp') and hasattr(torch.cuda.amp, 'autocast'):
        logging.info("AMP enabled!\n")
        autocast = torch.cuda.amp.autocast
    else:

        @contextlib.contextmanager
        def autocast():
            yield

    return autocast, asr_model, filepaths, cfg.batch_size


def run_inference(autocast, asr_model, filepaths, batch_size):
    with autocast():
        with torch.no_grad():
            transcriptions = asr_model.transcribe(filepaths, batch_size=batch_size)
    return transcriptions


if __name__ == '__main__':
    TranscriptionConfig.model_path = "nvidia/stt_en_conformer_ctc_medium.nemo"
    TranscriptionConfig.pretrained_name = "stt_en_conformer_ctc_medium"
    TranscriptionConfig.cuda = -1
    TranscriptionConfig.audio_dir = "Assets/"
    TranscriptionConfig.audio_type = "wav"
    TranscriptionConfig.batch_size=128

    out = init_transcribe_conf(TranscriptionConfig)  
    transcriptions = run_inference(out[0], out[1], out[2], out[3])
    print(transcriptions)
    transcriptions = run_inference(out[0], out[1], out[2], out[3])
    print(transcriptions)
    transcriptions = run_inference(out[0], out[1], out[2], out[3])
    print(transcriptions)
    transcriptions = run_inference(out[0], out[1], out[2], out[3])
    print(transcriptions)