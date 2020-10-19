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
* Acquire the "fine-tuned" `pyannote-audio` models trained on VoxConverse at [this link](https://drive.google.com/drive/folders/1GV_74JOU5_g-qxmNsXYs0QFEE4eiN2ro?usp=sharing). Place the individual folders into `EC601_Product_Design/Project3/Phase2/training/`.

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

### Phase 2

For Phase 2, students who were using a machine learning framework were tasked with training their system against the dataset that they intend to use for their term project. I am using the `VoxConverse` dataset, and as such, followed these instructions ([1](https://github.com/pyannote/pyannote-audio/tree/develop/tutorials/finetune) and [2](https://github.com/pyannote/pyannote-audio/tree/develop/tutorials/pipelines/speaker_diarization)) from `pyannote-audio`'s GitHub page to "fine-tune" their pre-trained models. The difference between "fine-tuning" and "training" is that ""fine-tuning" simply runs a small number of epochs on a pre-trained model, but with a separate dataset. Full "training" would involve developing the configuration parameters and running 100s to 1000s of epochs on the dataset until the optimal settings were reached.

The reason that I chose to "fine-tune" `pyannote-audio`'s pre-trained models as opposed to locally training was due to initial difficulties in understanding how their database `.yml` files worked. By the time the path issues were resolved, I only had a few days to complete the training on my local desktop. I ran the machine learning training on my local desktop with the following components: Intel i5-4590, 16GB RAM, and an NVIDIA GTX1070. While the training was not "slow" by most measures, it took about half a day to run the training on each of the neural network modules of `pyannote-audio`. Because of how long this took, I was only able to make tweaks to the training of the system 1 or 2 times prior to the October 19th due date.

If I were to run this training again, which I plan to for the term project, I would definitely use Boston University's SCC. One thing that held me back from using BU's SCC was that I thought there was a file storage limit of 10GB, based on [this link](https://www.bu.edu/tech/support/research/system-usage/using-scc/managing-files/). The total size of my training data was 17 GB, so I thought I was well over that limit. However, I have just found out that there is actually ~200GB of storage space for the ec601 project folder, so for the term project, I will be moving my resources onto the SCC and trying the training again.

I was actually shocked to see that almost all of the DER values for the test files became much worse than before. I believe this to be due to the differences between the DIHARD and VoxConverse datasets; although both are comprised of many news broadcasts and interviews, the spectral and spatial content of both are perhaps different enough that attempting to "fine-tune" the pre-trained models resulted in parameters that were overall worse. This also could be due to the low number of epochs I ran for "fine-tuning". The `pyannote-audio` tutorial for SAD "fine-tuning" actually only said to run for 5 epochs, but there were no values given for SCD, OVL, or Speaker Embedding tuning. When I looked at their tutorials that specified the number of epochs for full "training", they were significantly larger than even the full "training" for SAD. The amount of epochs for SAD training was 250, while something like SCD training used 2000 epochs.

Overall, I learned a lot about the process of neural network training and just how fickle it can be. Perhaps the higher DER values are not actually an error and this is exactly what should have happened given the amount of training I performed. It is difficult to understand neural network training since we rely on the system to train itself given a wide number of parameters. I will be more careful in the future with my training and hopefully I will see an improvement in DER values going forward.

## How to Run
~~Put one of your feet in front of your other in a very quick motion, repeat for other foot~~
### Phase 1
* `cd EC601_Product_Design/Project3/Phase1`
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

### Phase 2
* `cd EC601_Product_Design/Project3/Phase2`
* `python finetunedTest.py`. A successful run of this file will generate `reference_base.scp`, `score_base.scp`, `reference_fine.scp`, and `score_fine.scp`. There will also be some files generated in `EC601_Product_Design/SharedResources/RttmFiles/` and further subfolders.
* If the last command executed without any issues, use `python ../../SharedResources/dscore/score.py -R reference_base.scp -S score_base.scp` in Linux to run the scoring against the pre-trained model results.
* Use `python ../../SharedResources/dscore/score.py -R reference_fine.scp -S score_fine.scp` in Linux to run the scoring against the fine-tuned (tuned to VoxConverse) results. You should have the following results:

| Filename | Base DER | Fine DER |
|-----|-----|-----|
| abjxc | 4.44 | 0.75 |
| afjiv | 22.98 | 77.73 |
| ahnss | 16.25 | 57.61 |
| aisvi | 20.22 | 55.90 |
| akthc | 22.63 | 22.14 |
| OVERALL | 17.98 | 53.80 |

### Issues

### Phase 1
* For some reason, the performance of the pre-trained models in Windows was significantly slower than in Linux. I am not sure if this has to do with how PyTorch is installed differently in Windows than it is in Linux.
* I have noticed some issues with installing PyTorch as of October 8th, 2020. I was able to install version 1.6.0 sometime before this but lately, running `pip install torch torchvision` or even the longer command `pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html` seems to always return an error. Not sure if this is an issue with the hosting of PyTorch on PyPi or not.

### Phase 2
* I had some issues with `pyannote-audio` and training their "Speaker Embedding" module. I could run the training portion of the model, but when I needed the system to validate the training, I would always get `ValueError: zero-size array to reduction operation minimum which has no identity`, which meant that I could not be given the best parameters generated by the training. This lead to me having to use the pre-trained model in my `finetuneTest.py` testing.
