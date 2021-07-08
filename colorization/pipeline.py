from .colorize_process import preprocess, inference, postprocess
import os
import cv2
import tempfile
from .videodata import video2frames, \
    frames2video, split_audio_from_video, merge_audio_and_video
from moviepy.editor import VideoFileClip
import shutil

# error codes
FAILED = 1
SUCCESS = 0


# This file combines all of the single tasks to a complete working pipeline
# It does NOT contain the code of each task!
# The code for each task should be written seperate file and the function imported:
# see e.g. the postprocess function in postprocess.py


def colorize_image(image_input_path, image_output_path):
    """
    This function does the complete processing of a given image.
    It combines all of the subtasks together:
       - preprocess the image
       - colorize the image
       - postprocess the image

    This function is called by the webservice.

    Parameters:
    -----------
    image_input_path : str
        the path of the (gray) image to be processed

    image_output_path : str
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
    if not os.path.isfile(image_input_path):
        print("input path is not a file.")
        return FAILED

    #  check if the path for model is valid
    if not os.path.isfile(KMODELPATH):
        print("model path is not a file.")
        return FAILED

    #  load image located at <image_path_input> & preprocess, end image to device
    img = cv2.imread(image_input_path, cv2.IMREAD_COLOR)
    image_preprocessed = preprocess(img)

    #  inference & colorize
    inference_result = inference(KMODELPATH, image_preprocessed)

    #  postprocess & save image
    image_postprocessed = postprocess(image_input_path, inference_result)
    cv2.imwrite(image_output_path, image_postprocessed)
    print('Successfully saved')
    return SUCCESS


def colorize_video(video_input_path, video_output_path):
    """
    This function does the complete processing of a given video.
    It combines all of the subtasks together:
      - split video into images
      - colorize each image
      - combine images to a video
      - if the original video has audio, add the audio to colorized video

    This function is called by the webservice.


    Parameters:
    -----------
    video_input_path : str
        the path of the (gray) video to be processed

    video_output_path : str
        the path of the (colorized) video after processing

    return value : int
        on success this function returns 0
        on failure this function returns 1
    """
    #  check if the input path is valid
    if not os.path.isfile(video_input_path):
        print("input path is not a file.")
        return FAILED

    # split video into images
    my_tmp_path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '../tmp')

    # hack to fix problem when the tmp folder is not found
    # I suspect this is due to the colorization folder beeing
    # used through a symlink in the webservice
    if my_tmp_path.endswith('webservice/colorization/../tmp'):
        my_tmp_path = my_tmp_path.replace('webservice/colorization/../tmp', 'tmp')

    # print("tmp folder path:", my_tmp_path)

    tmpdir = tempfile.mkdtemp(suffix="_split_and_merge",
                              prefix="tp_images_and_audio_", dir=my_tmp_path)
    image_output_folder_path = tmpdir
    video_intermediate_path = os.path.join(tmpdir, 'merged_images.webm')
    audio_path = os.path.join(tmpdir, 'split_audio.ogg')
    ret = video2frames(video_input_path, image_output_folder_path)
    if ret != SUCCESS:
        print("split video into images failed")
        shutil.rmtree(tmpdir)
        return FAILED
    # call colorize_image on each image
    images = os.listdir(image_output_folder_path)
    for i in range(len(images)):
        image_path = os.path.join(image_output_folder_path, images[i])
        ret = colorize_image(image_path, image_path)
        if ret != SUCCESS:
            print("colorize video failed")
            shutil.rmtree(tmpdir)
            return FAILED

    # combine to video and save at <video_path_output>
    if VideoFileClip(video_input_path).audio is None:
        ret = frames2video(image_output_folder_path, video_output_path)
        if ret != SUCCESS:
            print("merge images back to video failed")
            shutil.rmtree(tmpdir)
            return FAILED
    else:
        ret = frames2video(image_output_folder_path, video_intermediate_path)
        if ret != SUCCESS:
            print("merge images back to video failed")
            shutil.rmtree(tmpdir)
            return FAILED
        ret = split_audio_from_video(video_input_path, audio_path)
        if ret != SUCCESS:
            print("split audio from original video failed")
            shutil.rmtree(tmpdir)
            return FAILED
        ret = merge_audio_and_video(video_intermediate_path,
                                    audio_path, video_output_path)
        if ret != SUCCESS:
            print("merge audio back to colorized video failed")
            shutil.rmtree(tmpdir)
            return FAILED

    # cleanup and return success code
    shutil.rmtree(tmpdir)
    return SUCCESS
