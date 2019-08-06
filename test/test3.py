import cv2
import numpy as np
import pandas as pd

cap = cv2.VideoCapture('./3DI.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
out = cv2.VideoWriter('./output.mp4', fourcc, fps, (352, 240))
data = pd.read_csv('./data/processed/table/MPentropy/3DI.csv')

frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
frame_num = 0
while (frame_num < frame_max):
    ret, frame = cap.read();
    video_time = frame_num / fps
    data_time = np.where(data['time'].values > video_time)[0]
    if len(data_time) > 0:
        index = np.min(data_time)
    else:
        break
    font = cv2.FONT_HERSHEY_SIMPLEX
    mp_entropy = data['MPentropy/'].values[index]
    if  mp_entropy > 4000:
        color = (150, 170, 255)
        size = 2
    else:
        color = (255, 150, 170)
        size = 1

    cv2.putText(frame, '{0:.1f}'.format(mp_entropy), (140, 200), font, 0.4, color, size)
    frame_num += 1
    out.write(frame)
cap.release()
out.release()
