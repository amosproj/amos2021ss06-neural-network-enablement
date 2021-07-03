from .colorize_process import preprocess, inference, postprocess
import os
import cv2
import tempfile
from .videodata import video2frames, frames2video, \
    split_audio_from_video, merge_audio_and_video
from moviepy.editor import  VideoFileClip

# error codes
FAILED = 1
SUCCESS = 0


# This file combines all of the single tasks to a complete working pipeline
# It does NOT contain the code of each task!
# The code for each task should be written seperate file and the function imported:
# see e.g. the postprocess function in postprocess.py


def colorize_image(image_path_input, image_path_output):
    """
    This function does the complete processing of a given image.
    It combines all of the subtasks together:
       - preprocess the image
       - colorize the image
       - postprocess the image

    This function is called by the webservice.

    Parameters:
    -----------
    image_path_input : str
        the path of the (gray) image to be processed

    image_path_output : str
        the path of the (colorized) image after processing


    return value : int
        on success this function returns 0
        on failure this function returns 1


    Example call:
    -------------
    colorize_image('/home/user/xyz/Pictures/pic1.jpg',
                   '/home/user/xyz/Pictures/pic1_colorized.jpg')

    The directories already exists, and the image can be directly
    written to the given output path.
    """

    KMODELPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              "../model/colorization.om")

    #  check if the input path is valid
    if not os.path.isfile(image_path_input):
        print("input path is not a file.")
        return FAILED

    #  check if the path for model is valid
    if not os.path.isfile(KMODELPATH):
        print("model path is not a file.")
        return FAILED

    #  load image located at <image_path_input> & preprocess, end image to device
    img = cv2.imread(image_path_input, cv2.IMREAD_COLOR)
    image_preprocessed = preprocess(img)

    #  inference & colorize
    inference_result = inference(KMODELPATH, image_preprocessed)

    #  postprocess & save image
    image_postprocessed = postprocess(image_path_input, inference_result)
    cv2.imwrite(image_path_output, image_postprocessed)
    print('Successfully saved')
    return SUCCESS


def colorize_video(video_path_input, video_path_output):
    """
    This function does the complete processing of a given video.
    It combines all of the subtasks together:
      - split video into images
      - colorize each image
      - combine images to a video

    This function is called by the webservice.


    Parameters:
    -----------
    video_path_input : str
        the path of the (gray) video to be processed

    video_path_output : str
        the path of the (colorized) video after processing
    """
    #  check if the input path is valid
    if not os.path.isfile(video_path_input):
        print("input path is not a file.")
        return FAILED

    # split video into images
    tmpdir = tempfile.mkdtemp(suffix="_split_and_merge",
                              prefix="tp_images_and_audio_", dir="/tmp")
    image_output_folder_path = tmpdir
    video_intermediate_path = os.path.join(tmpdir, 'merged_images.mp4')
    audio_path = os.path.join(tmpdir, 'split_audio.mp3')
    ret = video2frames(video_path_input, image_output_folder_path)
    if ret != SUCCESS:
        print("split video into images failed")
        tmpdir.cleanup()
        return FAILED
    # call colorize_image on each image
    images = os.listdir(image_output_folder_path)
    for i in range(len(images)):
        image_path = os.path.join(image_output_folder_path, images[i])
        ret = colorize_image(image_path, image_path)
        if ret != SUCCESS:
            print("colorize video failed")
            tmpdir.cleanup()
            return FAILED
    # combine to video
    ret = frames2video(image_output_folder_path, video_intermediate_path)
    if ret != SUCCESS:
        print("merge images back to video failed")
        tmpdir.cleanup()
        return FAILED

    # save at <video_path_output>
    if VideoFileClip(video_path_input).audio is not None:
        ret = split_audio_from_video(video_path_input, audio_path)
        if ret != SUCCESS:
            print("split audio from original video failed")
            tmpdir.cleanup()
            return FAILED
        ret = merge_audio_and_video(video_intermediate_path,
                                    audio_path, video_path_output)
        if ret != SUCCESS:
            print("merge audio back to colorized video failed")
            tmpdir.cleanup()
            return FAILED

    # return success code -> talk with webservice people
    tmpdir.cleanup()
    return SUCCESS
