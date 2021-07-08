import cv2
import os
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
from moviepy.video.io import ImageSequenceClip

SUCCESS = 0
FAILED = 1
FPS = 60


def video2frames(video_input_path, image_output_folder_path):
    """This function is used to convert video into images.
     Args:
        video_input_path: filename of the video.
        image_output_folder_path: Output folder path containing images
     Returns:
        1 on fail.
        0 on success.
     """
    video = cv2.VideoCapture(video_input_path)
    video_type = os.path.splitext(video_input_path)[-1]
    if (video.isOpened() is False) or (not (video_type == '.mp4')):
        print("Input path is not a video")
        return FAILED
    global FPS
    FPS = int(video.get(cv2.CAP_PROP_FPS))
    currentframe = 0
    while video.isOpened():
        ret, frame = video.read()
        if ret is True:
            folder_name = os.path.join(image_output_folder_path,
                                       str(currentframe) + '.png')
            cv2.imwrite(folder_name, frame)
            currentframe += 1
        else:
            break
    video.release()
    return SUCCESS


def frames2video(image_input_folder_path, video_output_path):
    """This function is used to convert images into a video.
    Args:
        image_input_folder_path: path to the split images.
        video_output_path: path to the merged video
    Returns:
        0 for SUCCESS.
        1 for FAILED.

    """
    files = os.listdir(image_input_folder_path)
    frames_path = [image_input_folder_path+'/'+str(i)+'.png' for i in range(len(files))]
    clip = ImageSequenceClip.ImageSequenceClip(frames_path, fps=FPS)
    clip.write_videofile(video_output_path, codec='libvpx', bitrate="50000k")
    clip.close()
    return SUCCESS


def split_audio_from_video(video_input_path, audio_output_path):
    """This function is used to extract voice from a video.
    Args:
        video_input_path: path of the origin video
        audio_output_path: path to the voice file
    Returns: int
        on success this function returns 0
        on failure this function returns 1
    """
    if not os.path.isfile(video_input_path):
        print("invalid video path")
        return FAILED
    my_audio_clip = AudioFileClip(video_input_path)
    my_audio_clip.write_audiofile(audio_output_path, codec='libvorbis')
    if not os.path.isfile(audio_output_path):
        print("invalid output path")
        my_audio_clip.close()
        return FAILED
    my_audio_clip.close()
    return SUCCESS


def merge_audio_and_video(video_input_path, audio_input_path, video_output_path):
    """This function is used to mge voice with a video merged from images.
    Args:
        video_input_path: path of the origin video
        audio_input_path: path of the voice file
        video_output_path: path to the result video
    Returns: int
        on success this function returns 0
        on failure this function returns 1
    """
    if not os.path.isfile(video_input_path):
        print("invalid video path")
        return FAILED
    if not os.path.isfile(audio_input_path):
        print("invalid audio path")
        return FAILED
    my_video_clip = VideoFileClip(video_input_path)
    my_audio_clip = AudioFileClip(audio_input_path)
    video = my_video_clip.set_audio(my_audio_clip)
    video.write_videofile(video_output_path, codec='libvpx')
    if not os.path.isfile(video_output_path):
        print("invalid output path")
        my_audio_clip.close()
        my_video_clip.close()
        return FAILED
    my_audio_clip.close()
    my_video_clip.close()
    return SUCCESS
