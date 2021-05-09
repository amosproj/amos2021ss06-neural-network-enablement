# import subtask functions
from postprocess import postprocess
from utils import CopyDataDeviceToHost
# import splitVideo


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
    """

    # TODO: load image located at <image_path_input>
    # TODO: preprocess (do preprocessing on the device itself?)
    # TODO: upload to device
    # TODO: colorize
    # TODO: postprocess
    # TODO: save at <image_path_output>
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
