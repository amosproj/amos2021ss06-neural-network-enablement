import cv2
import os
import videodata

# split the video
cwd = os.path.abspath(os.path.dirname(__file__))
videopath = os.path.join(cwd, 'test_data')
print(videopath)
videoName = 'greyscaleVideo.mp4'
ret = videodata.video2frames(videopath, videoName)
print(ret)

# merge the video

video_output_path = os.path.join(videopath, 'merged_video')
os.makedirs(video_output_path)
print(video_output_path)
videodata.frames2video(image_input_folder_path, video_output_path)
print(ret)
