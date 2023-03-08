# Whisper

Local automatic voice recognition module to avoid dependency on internet connection for human-robot interaction.


## Description

The program is based in the interaction of 3 nodes:
- ```checkamplitude:``` is in charge of detecting amplitudes over a determined threshold, and silences longer than an established duration. 
- ```audiorecorder:``` is in charge of recording wakeup call and command audios.
- ```whisperlogic:``` is in charge of generating the audio's transcriptions, and identifying valid wakeup and exit calls.

In the following flowchart each block is distinguished according to the node that executes the determined process, by the upper right corner colour code.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://i.postimg.cc/fRpbD88R/darkflowchart.png">
  <source media="(prefers-color-scheme: light)" srcset="https://i.postimg.cc/d0bJPgNq/flowchart.png">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://i.postimg.cc/d0bJPgNq/flowchart.png">
</picture>

Detailed flowcharts of each node:

- [checkamplitude flowchart](https://i.postimg.cc/wTKbsj1g/checkamplitudeflow.png)
- [audiorecorder flowchart](https://i.postimg.cc/nzgS2HTK/audioflow.png)
- [whisperlogic flowchart](https://i.postimg.cc/sfGNXhDT/whisperflow.png)


## Installation

Install from terminal
```bash
sudo apt-get install libasound2-dev
sudo apt-get install portaudio19-dev
sudo apt update && sudo apt install ffmpeg
```
Create and activate a virtual environment, then use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary libraries from the file 'requirements.txt'
```bash
pip install -r requieremnts.txt
```

## Usage

```setup.launch:``` Will launch all required nodes for the module to work. The following parameters can be modified through this file:

- ```THRESHOLD_HIGH:``` Amplitude threshold for speaking.
- ```THRESHOLD_LOW:``` Amplitude threshold for silence.


## Acknowledgment
OpenAi [Whisper](https://openai.com/research/whisper)