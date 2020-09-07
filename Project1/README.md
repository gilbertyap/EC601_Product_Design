# Project 1 - Product and Research Review

## Requirements 
* **Windows 10**

* **Python** (3.8.5 used)

* **pyBK**: Python libraries required - numpy, scipy, scikit-learn,librosa, webrtcvad

* **Perl**: For running the .rttm evaluation script

## Libraries Used
(Sourced libraries are in the SharedResources folder)

pyBK: https://github.com/josepatino/pyBK

```
@inproceedings{Bredin2020,
  Title = {{pyannote.audio: neural building blocks for speaker diarization}},
  Author = {{Bredin}, Herv{\'e} and {Yin}, Ruiqing and {Coria}, Juan Manuel and {Gelly}, Gregory and {Korshunov}, Pavel and {Lavechin}, Marvin and {Fustes}, Diego and {Titeux}, Hadrien and {Bouaziz}, Wassim and {Gill}, Marie-Philippe},
  Booktitle = {ICASSP 2020, IEEE International Conference on Acoustics, Speech, and Signal Processing},
  Address = {Barcelona, Spain},
  Month = {May},
  Year = {2020},
}
```

## Video Sample

https://www.youtube.com/watch?v=NznMbYuaf9Q - Audio sample from 0:00 to 3:00.

The choice of video sample was chosen for time length convenience, number of speakers, and speaker clarity. The choice should not be taken as a reflection of my own opinions or political leanings. 

## Summary
The purpose of Project 1 is to investigate current research on a specific topic. The topic that was chosen for this project was "multiple speaker identification". The main principle behind this topic is called "speaker diarization" and is implemented by many major companies in their products. Speaker diarization at a glance is the act of segmenting and clustering speech within an audio stream to identify multiple speakers and associate periods of speech to a specific identity. 

Google's Cloud Speech-To-Text, Amazon's Transcribe, and IBM's Watson Speech-To-Text API all feature their own speaker diarization method that can be utilized by developers. However, for this project open-source GitHub repositories were investigated, along with their corresponding research papers, to quickly become acquianted with the methodologies and differences in speaker diarization offerings.

The library that was tested for this project was **pyBK**. pyBK uses a binary key model that does not require model training, so this made for a quick prototyping candidate. To test the efficiency of the binary key model, a random audio sample was taken from YouTube. This audio sample is from a CNN panel discussion with 7 participants. This audio sample may be challenging for speaker diarization systems since there are instances of overlapping speech. 

Bundled with the pyBK repository is the [dscore evaluation tool](https://github.com/nryant/dscore) that was used to check the Diarization Error Rate (DER). This check is done by comparing two Rich Transcription Time Marked (RTTM) files: one reference file and one generated file. The reference `.rttm` file was manually transcribed and thus may contain some amount of human error. Various configurations were tested to see the effects of changing the cluster number selection method,increasing starting clusters, reducing frame size, or increasing the number of Mel-frequency cepstral coefficients.

## How to run

The file `pyBK_test.py` can be run from the command line with no arguements. This will output a `.rttm` file into the `pyBKFiles/out/` folder. The `pyBKFiles/run_eval.bat` batch file can then be used to compare a reference the reference .rttm file to one generated within the `pyBKFiles/out/` folder. The dscore information will then be printed to the command line window. Please see the GitHub page for dscore and pyBK for more information about the RTTM format and scoring.