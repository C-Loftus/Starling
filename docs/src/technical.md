## Technical Background
Starling has five main parts of its technical design.
* Non-blocking sound recording
* Speech to text decoding 
* Parsing commands from decoded text
* The command runner
* The system tray appindicator program

### Non-blocking sound recording
There are two implementations of sound recording depending upon which  speech to text model you are using
#### Vosk
Vosk records using an ffmpeg stream. It continuously feeds this stream to the model and  only outputs text once it has reached a confidence threshold that indicates the end of a word.

#### Nvidia Nemo
 I experimented with an alternative solution for passing sound to nemo.  in my solution, I begin by spawning a background thread.  This thread gets the ambient volume of the environment.  I then spawn a listener thread. This thread continuously records sound updates to a small buffer. It checks to see if there has been a increase from the ambient volume. If there has been, it will begin recording audio from the user.  it will stop recording once the volume drops  back near the ambient volume. 

 In this implementation, I used a buffer since you cannot simply start recording when the volume goes high. If you do that,  the start of the first word that is spoken will be partially cut off due to latency. The buffer allows you two go back slightly in time before the ambient volume difference check was triggered. 
### Speech to Text
Starling is built upon the [Vosk speech recognition toolkit](https://alphacephei.com/vosk/). The model used is the [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models). This model is 40M is size and its vocabulary can be dynamically changed during runtime. This allows me to switch the vocabulary  depending upon the currently focused application. 

You can install Nvidia's nemo toolkit if you want an alternative speech to text backend and prefer not to use Vosk. As of right now, this is for testing purposes and Vosk  should be preferred.
```bash
# run the following command from the project makefile
# downloads model and installs nemo_toolkit[all]
make dev
```