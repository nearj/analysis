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
3. Calculate MP Entropy and entropy of optical flow   
   With **Motion Probability** and **Optical Probability**  
&#8594;   Make MP Entropy at a frame and entropy of optical flow at a frame  

### Project Files

- main.py  
Subsampling(3hz) raw motion data of csv file to probability of all motion vector in experiment as csv file
To analysis when VR sickness at simulation, it visualize optical flow of video and highlight SSQ


## Usage example
```sh
python3 main.py motion_file(csv) video_file(mp4) output_file_name(csv) [--mute_svg] [--mute_acr] [--mute_norm]
```
main.py calculate take inputs as two file of csv format - motion data file and video file - and makes output_file_name.csv which contains categorized MP Entropy. By default the result of main.py contains normalization on MP Entropy with Absolutely Category Rating(ACR) and savitzky golay filtering (window size 9 and order 2) on motion signal of Motion Platform. It means the values of MP Entropy are categorized by 5 levels, which menas upper level is more comportable for the users. See [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky–Golay_filter) and [Absolute Category Rating](https://en.wikipedia.org/wiki/Absolute_Category_Rating).
 

options on usage
### --mute_svg
mute savitzky golay filtering option
### --mute_acr
mute Absolute Category Rating
### --mute_svg
mute normalization

