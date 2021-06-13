import os
import videodata

# split the video
cwd = os.path.abspath(os.path.dirname(__file__))
video_input_path = os.path.join(cwd, 'test_data/input_image_2.jpg')
image_output_folder_path = os.path.join(cwd, 'test_data/split_frames')
#os.mkdir(image_output_folder_path)
videodata.video2frames(video_input_path, image_output_folder_path)


# merge the video
cwd = os.path.abspath(os.path.dirname(__file__))
image_output_folder_path = os.path.join(cwd, 'test_data/split_frames')
video_output_path = os.path.join(cwd, 'test_data/merged_video')
#os.mkdir(video_output_path)
videodata.frames2video(image_output_folder_path, video_output_path)
