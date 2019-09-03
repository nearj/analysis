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
│   main.py
|   test.csv
|───mpvr
│   |───datamodule
│   |   |─manager.py
│   |   |─motion_device_2018.py
│   |   |─threedi_2018.py
│   |   |─_fig_preset.py
│   |───utils
│   |   |─correlation_analysis.py
│   |   |─process.py
│   └───etc
│       |─ssq.py
|
|───data
│   |───raw
│   |   |─motion < from unity synchronized with video, 3hz sample rate
│   |   |─video < from unity synchronized with motion, 3hz sample rate
│   └───processed
│       |───MotionDevice_2018
│       |   |───incidence
│       |   |───motion
│       |   |───timestamp
│       └───THREEDI_2018
│           |───incidence
│           |───motion
│           └───timestamp
|───config
|───csharp
|───script
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

- main.py  

Subsampling(3hz) raw motion data of csv file to probability of all motion vector in experiment as csv file

To analysis when VR sickness at simulation, it visualize optical flow of video and highlight SSQ


###### For search which function currently used in project please see # HERE! in project


## Usage example
```sh
python3 main.py [motion_path] [video_path] [output_path]
```

## TO-DO:
- [ ] comment project
