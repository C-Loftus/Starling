################VV## user targets ##VV###############
apt: vosk python
	sudo apt install gir1.2-appindicator3-0.1 libxosd2 xosd-bin xdotool xprintidle

ubuntu: apt 
mint: apt 
debian: apt 
pop-os: apt

uninstall:
	rm -rf src/nvidia/*.nemo
	pipenv uninstall
	rm -rf src/vosk-api/model

####################################################

nemo:
	wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_ctc_medium/versions/1.0.0/zip -O src/nvidia/stt_en_conformer_ctc_medium_1.0.0.zip
	unzip src/nvidia/stt_en_conformer_ctc_medium_1.0.0.zip -d src/nvidia/.
	rm src/nvidia/stt_en_conformer_ctc_medium_1.0.0.zip
vosk:
	wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip
	unzip vosk-model-small-en-us-0.15.zip
	mv vosk-model-small-en-us-0.15 src/vosk-api/model
	rm vosk-model-small-en-us-0.15.zip

python:
	pip3 install --upgrade pip
	pip3 install --user --upgrade --upgrade-strategy eager pipenv wheel setuptools
	pipenv install

dev: python
	pipenv install --dev

# make -B
docs:
	mdbook build docs
	ln docs/book/* ../StarlingBook/
