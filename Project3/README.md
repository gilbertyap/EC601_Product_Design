# Project 3 - Major Open-Source Project Case Study

## Requirements
* Tested on **Windows 10 1909** and **Ubuntu 20.04.1** (May work on MacOS but untested). Performance on Windows 10 is much slower than Ubuntu when using pretrained pyannote-audio pipline.
* **Python** (3.8.5 used), libraries can be installed as outlined below.

## Installation
* `git clone git@github.com:gilbertyap/EC601_Product_Design.git`
* `cd ./EC601_Product_Design/SharedResources/pyannote-audio/`, `git checkout develop`, then `git install .`. This will install `pyannote-audio` into Python's packages.
* `cd ../../EC601_Product_Design/Project3/`
* `pip install -r requirements.txt` - This will install almost all Python requirements.
* Install [PyTorch](https://pytorch.org/).

## Example Files
* `Sample_Video.m4v`
* `reference_scores.txt`

## Citations
**pyannote-audio**
```
@inproceedings{Bredin2020,
  Title = {{pyannote.audio: neural building blocks for speaker diarization}},
  Author = {{Bredin}, Herv{\'e} and {Yin}, Ruiqing and {Coria}, Juan Manuel and {Gelly}, Gregory and {Korshunov}, Pavel and {Lavechin}, Marvin and {Fustes}, Diego and {Titeux}, Hadrien and {Bouaziz}, Wassim and {Gill}, Marie-Philippe},
  Booktitle = {ICASSP 2020, IEEE International Conference on Acoustics, Speech, and Signal Processing},
  Address = {Barcelona, Spain},
  Month = {May},
  Year = {2020},
```
}

**VoxConverse Dataset**
```
@article{chung2020spot,
  title={Spot the conversation: speaker diarisation in the wild},
  author={Chung, Joon Son and Huh, Jaesung and Nagrani, Arsha and Afouras, Triantafyllos and Zisserman, Andrew},
  journal={arXiv preprint arXiv:2007.01216},
  year={2020}
}
```

## Summary

### Phase 1

The goal of Project 3 is to utilize a major open-source library that relates to our term project. In my case, this was using `pyannote-audio` to see how well it performs speaker diarization. `pyannote-audio` is a modular, neural network system focused on trainable speech activity detection, speaker change detection, overlapped speech detection, and speaker embedding components. For the purpose of Phase 1, I used their pre-trained pipeline (trained on the DIHARD challenge set) to get baseline performance against the `VoxConverse` development dataset. I believed that `pyannote-audio` would be a good choice for testing since each of its components are trainable, meaning for Phase 2, I am hoping to see the benefits of training the system against the `VoxConverse` dataset and seeing how the accuracy increases or decreases.

The reason that I chose the `VoxConverse` dataset was because it provided the simplest means of testing; the University of Oxford/Naver Corporation provided timestamp files (`.rttm`) for all corresponding audio files, meaning I could generate the Diarization Error Rate (DER) without first having to make the timestamp files by hand. The `VoxConverse` data set consists of political debates and news segments, sometimes including non-speech portions. The `VoxConverse` dataset did NOT come with the necessary `.uem` files that would tell the `pyannote-audio` pipeline which portions of the file are speech or non-speech, so the system assumed the entire file was speech. This may have affected some of the results negatively. For Phase 2, I am hoping to either create the `.uem` files by hand or have them automatically generated (using something like [py-webrtcvad](https://github.com/wiseman/py-webrtcvad)).

`pyannote-audio` was actually a software library that I wanted to test in Project 1, but at the time I was experiencing issues with using it. However, once I installed a non-virtual Linux system, I found that the issues I was experiencing in Project 1 was perhaps Windows-only issues.

## How to Run
~~Put one of your feet in front of your other in a very quick motion, repeat for other foot~~
* For Phase 1: `cd EC601_Product_Design/Project3/Phase1`
* `python phase1.py`. A successful run of this file will generate `reference.scp` and `score.scp`.
* If the last command executed without any issues, use `python ../../SharedResources/dscore/score.py -R reference.scp -S score.scp` in Linux to run the scoring. You can then compare the results to `reference_scores.txt`. You should get the following DER values:

| Filename | DER |
|-----|-----|
| abjxc | 4.46 |
| afjiv | 22.96 |
| ahnss | 18.54 |
| aisvi | 21.03 |
| akthc | 23.41 |
| OVERALL | 19.45 |

### Issues

* For some reason, the performance of the pre-trained models in Windows was significantly slower than in Linux. I am not sure if this has to do with how PyTorch is installed differently in Windows than it is in Linux.
* I have noticed some issues with installing PyTorch as of October 8th, 2020. I was able to install version 1.6.0 sometime before this but lately, running `pip install torch torchvision` or even the longer command `pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html` seems to always return an error now. Not sure if this is an issue with the hosting of PyTorch on PyPi or not.
