import os
import videodata

# split the video
cwd = os.path.abspath(os.path.dirname(__file__))
video_input_path = os.path.join(cwd, 'test_data/greyscaleVideo.mp4')
image_output_folder_path = os.path.join(cwd, 'test_data/split_frames')
videodata.video2frames(video_input_path, image_output_folder_path)

# merge the video
cwd = os.path.abspath(os.path.dirname(__file__))
image_output_folder_path = os.path.join(cwd, 'test_data/split_frames')
video_output_path = os.path.join(cwd, 'test_data/merged_video')
videodata.frames2video(image_output_folder_path, video_output_path)
