# Motion Platfrom Virtual Reality(MPVR) Motion Filtering
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
│   configure.py
|   threedi.py
|   CalQ.cs
|   PlayMenu.cs
|───mpvr
│   |───datamanager
│   |   |─datamanager.py
│   |   |─threedi.py
│   |   |─UOS2018.py
│   |───process
│   |   |─process.py
│   └───etc
│       |─ssq.py
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

### Procedure Abstraction

1. subsampling Motion of Platform(**MoP**)  
   Raw data of MoP which is sampled as 3hz  
&#8594;   Making lookup-table by scanning all motion in simulation(a video; E.g. probably there are 2 MoP in S1_pitch, up and down)   
&#8594;   At frame level, take probability of the frame's probability with the lookup table  
&#8594;   Save probability as json; **Motion Probability** as *json*,  
2. Subsampling optical flow  
   Raw data of optical flow which is sampled as 3hz  
&#8594;   Polarization all optical flow  
&#8594;   Making lookup-table by scanning all optical flows in simulation(a video) at frames and all pixels in frames(pixels in frame\*frames in simulation; E.g. 1024\*768\*60 at 20s simulation)  
&#8594;   At frame level, take probability of the polarized pixel's optical flow with the lookup table  
&#8594;   Store **Optical Probability** in *memory*.
3. Calculate KLD and entropy of optical flow   
   With **Motion Probability** as *json* and **Optical Probability** in *memory*  
&#8594;   Make KLD at a frame and entropy of optical flow at a frame  
&#8594;   Save it as figure(.jpg)

### Project Files

- preprocess_motion.py  

Subsampling(3hz) raw motion data of txt file to probability of all motion vector in experiment as json and excel file

- preprocess_video.py **--FIXME--**  

Subsampling(3hz) raw video, however 1024*768 pixel probability are hard to save as json or other format.For now, it used to import optical flow data in processing.py.

- processing.py **--FIXME--**  

From subsampled data by preprocess_video.py and preprocess_motion.py, this module calculate KLD and Entropy of optical flow and save it as jpg.

- make_video_with_SSQ.py  

To analysis when VR sickness at simulation, it visualize optical flow of video and highlight SSQ


###### For search which function currently used in project please see # HERE! in project


## Usage example
- process raw data of motion of platform to probability density
```sh
python preprocecess_motion.py
```

- process raw data of video and preprocessed MoP to KLD and Entropy of Optical Flow
```sh
python processing.py
```

## TO-DO:
- [ ] comment project
- [ ] add calculate probability of optical flow in video at frame level and export data
- [ ] modulize processing.py
