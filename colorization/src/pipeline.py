
from colorize_process import *
from utils import CopyDataDeviceToHost
import numpy
import cv2
from Data.data import *
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
    """

    kModelWidth = numpy.uint32(224)
    kModelHeight = numpy.uint32(224)
    KMODELPATH = "../model/colorization.om"
    colorize = ColorizeProcess(KMODELPATH, kModelWidth, kModelHeight)
    colorize.Init()
    # TODO: load image located at <image_path_input> -- delete, already in preprocess
    # image_path_input = loadimage(image_path_input)
    # if image_path_input == "path not found":
    #     return FAILED
    # TODO: preprocess (do preprocessing on the device itself?) -- load image, preprocess, upload to device
    if colorize.Preprocess(image_path_input) == FAILED:
        print("Read file ", image_path_input, " failed, continue to read next")
        return FAILED
    # TODO: inference ?? wait to check, should use model_process(self,modelPath) or inference(inferenceOutput)?
    (inferenceOutput, ret) = colorize.inference()
    if ret == FAILED:
        print("Inference model inference output data failed")
        return FAILED
    # TODO: colorize
    # TODO: postprocess
    # check the return value of postprocess with Raj
    image = colorize.postprocess(image_path_input, inferenceOutput)
    cv2.imwrite(image_path_output, image)
    # sprich mit R und S

    # TODO: return success code -> talk with webservice people
    pass


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
