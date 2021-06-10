from colorize_process import ColorizeProcess
import numpy
import os
import tempfile
# import cv2
# from Data.data import *
# import splitVideo


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
    kModelWidth = numpy.uint32(224)
    kModelHeight = numpy.uint32(224)
    KMODELPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              "../../model.colorization.om")

    #  check if the input path is valid
    if not os.path.isfile(image_path_input):
        print("input path is not a file.")
        return FAILED

    #  check if the path for model is valid
    if not os.path.isfile(KMODELPATH):
        print("model path is not a file.")
        return FAILED

    #  call colorize process and start colorization
    colorize = ColorizeProcess(KMODELPATH, kModelWidth, kModelHeight)
    ret = colorize.Init()
    if ret == FAILED:
        print("init colorize process failed")
        return FAILED

    #  load image located at <image_path_input> & preprocess, end image to device
    if colorize.Preprocess(image_path_input) == FAILED:
        print("Read file ", image_path_input, " failed, continue to read next")
        return FAILED

    #  inference & colorize
    tmpdir = tempfile.TemporaryDirectory(suffix="_npy", prefix="tp_inference_", dir="/tmp")
    inference_output_path = tmpdir.name + '/inference_output.npy'
    ret = colorize.inference(inference_output_path)
    if ret == FAILED:
        print("Inference model inference output data failed")
        tmpdir.cleanup()
        return FAILED

    #  postprocess & save image
    ret = colorize.postprocess(image_path_input, inference_output_path, image_path_output)
    if ret == FAILED:
        print("Process model inference output data failed")
        tmpdir.cleanup()
        return FAILED
    #  return success code
    tmpdir.cleanup()
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
