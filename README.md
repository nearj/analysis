# Motion Sickness Quantification
> ETRI SW콘텐츠연구소 차세대콘텐츠연구본부 및 서울시립대 연구과제

모션 플랫폼에서 발생하는 VR멀미 정량화 및 저감 연구

## dependencies
see requirements.txt

```sh
pip install -r requirements.txt
```

## File Structures
```
project
│   README.md
│   preprocess_video.py
|   preprocess_motion.py
|   processing.py
|   make_video_with_SSQ.py
|   CalQ.cs
|   PlayMenu.cs
|
|───data
│   |───raw
│   |   |─motion < from unity synchronized with video, 3hz sample rate
│   |   |─video < from unity synchronized with motion, 3hz sample rate
│   |───preprocessed 
│   |   |─motion < preprocess_motion.py; probability of motion in simulation level
│   └───processed
│       |─video < make_video_with_SSQ.py; highlight SSQ and optical flows
│       |─table < processing.py; pending currently
│       |─graph < processing.py < preprocess_video.py
│───old
|───test

```

## Explanation
- preprocess_motion.py  

Subsampling(3hz) raw motion data of txt file to probability of all motion vector in experiment as json and excel file

- preprocess_video.py **--FIXME--**  

Subsampling(3hz) raw video, however 1024*768 pixel probability are hard to save as json or other format.For now, it used to import optical flow data in processing.py.

- processing.py **--FIXME--**  

From subsampled data by preprocess_video.py and preprocess_motion.py, this module calculate KLD and Entropy of optical flow and save it as jpg.

- make_video_with_SSQ.py  

To analysis when VR sickness at simulation, it visualize optical flow of video and highlight SSQ


## Usage example
- process raw data of motion of platform(MoP) to probability density
```sh
python preprocecess_motion.py -use_default
```

- process raw data of video and preprocessed MoP to KLD and Entropy of Optical Flow
```sh
main(1) // S4 ~ S6
main(2) // heave motion on S1~S3
main(0) // else
in python
```

## TO-DO:
- [ ] comment project
- [ ] add calculate probability of optical flow in video at frame level and export data
- [ ] modulize processing.py
