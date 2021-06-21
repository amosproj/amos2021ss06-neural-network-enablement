from colorize_process import preprocess, inference, postprocess
import os
import cv2
import sys
sys.path.append('../colorization')
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
    # TODO: load video located at <video_path_input>
    # TODO: split video into images
    # TODO: call <processImage> on each image
    # TODO: combine to video
    # TODO: save at <video_path_output>

    # TODO: return success code -> talk with webservice people
    pass
