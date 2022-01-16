model:
	wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_ctc_medium/versions/1.0.0/zip -O src/nvidia/stt_en_conformer_ctc_medium_1.0.0.zip
	unzip src/nvidia/stt_en_conformer_ctc_medium_1.0.0.zip -d src/nvidia/.
	rm src/nvidia/stt_en_conformer_ctc_medium_1.0.0.zip

python:
	pip3 install --upgrade pip
	pip3 install --user --upgrade --upgrade-strategy eager pipenv wheel setuptools
	pipenv install

apt: model python
	sudo apt install gir1.2-appindicator3-0.1 libxosd2 xosd-bin xdotool xprintidle

ubuntu: apt 
mint: apt 
debian: apt 
pop-os: apt

uninstall:
	rm -f src/nvidia/*.nemo
	pipenv uninstall