################VV## user targets ##VV###############
apt: vosk python
	sudo apt install gir1.2-appindicator3-0.1 libxosd2 xosd-bin xdotool xprintidle wmctrl

#### run make TARGET to build for your distro. ####
ubuntu: apt 
mint: apt 
debian: apt 
pop-os: apt
mint: apt
elementary: apt

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
	mv $(CURDIR)/vosk-model-small-en-us-0.15 $(CURDIR)/src/vosk_bindings/model
	rm vosk-model-small-en-us-0.15.zip

python:
	pip3 install --upgrade pip
	pip3 install --user --upgrade --upgrade-strategy eager wheel setuptools
	sudo -H pip install -U pipenv
	sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
	sudo apt install portaudio19-dev
	sudo apt install gir1.2-appindicator3-0.1 python3-gi
	sudo apt-get install python3-tk
	pipenv install
### run pip3 uninstall virtualenv if there is an issue building distuil

# referenece the following if there is an issue with "virtualenv-seed-embed"
### https://stackoverflow.com/questions/63491221/modulenotfounderror-no-module-named-virtualenv-seed-embed-via-app-data-when-i

dev: python nemo
	pipenv install --dev

	

# make -B
# cd newIWVoice/; make -B docs; cd ../StarlingDocs/; fgc updated; cd ../
docs: 
	mdbook build docs
	cp -r docs/book/* ../StarlingDocs/