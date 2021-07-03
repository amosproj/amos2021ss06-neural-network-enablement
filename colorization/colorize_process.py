import numpy as np
import cv2
from .acl_resource import AclResource
from .model_processor import ModelProcessor

# constant variables
FAILED = 1
SUCCESS = 0


def preprocess(image_file):
    """
    This function downsizes the input image to modelWidth*modelHeight
    and extracts L_channel from the image.

    Parameters:
    -----------
    input:
    image_file : numpy array
        An image that is loaded from the specified file.

    return value : numpy array
        L channel of the image subtracted by the 50 for mean-centering.
    """
    mat = image_file

    if np.any(mat) is None:  # if matrix is empty, every term is none
        return FAILED

    mat = mat.astype(np.float32)

    resize_mat = cv2.resize(mat, (224, 224))

    # deal image
    resize_mat = 1.0 * resize_mat / 255
    resize_mat = cv2.cvtColor(resize_mat, cv2.COLOR_BGR2Lab)

    # pull out L channel and subtract 50 for mean-centering
    # channel[0] = L, [1] = A, [2] = B
    channels = cv2.split(resize_mat)

    print(f'{len(channels)} channels')

    return channels[0] - 50


def inference(model_path, input_image):
    """
    This function activate the model process after preprocess,
    and get result back.
    Parameters:
    -----------
    model_path: str
        the path of offline model(*.om file)
    input_image: numpy array
        resized image with L_channel obtained from preprocess.

    result : numpy array
        ab channels of the preprocessed image.
    """
    # initialize acl runtime
    # since AclResource is a singleton, the init is only called at the initial creation
    acl_resource = AclResource()

    # parameters for model path and model inputs
    model_parameters = {
        'model_dir': model_path,
        'width': 224,  # model input width
        'height': 224,  # model input height
    }
    model_processor = ModelProcessor(acl_resource, model_parameters)
    canvas = model_processor.predict(input_image)
    return canvas


def postprocess(input_image_path, inference_result):
    """This function converts LAB image to BGR image (colorization).
     It combines L channel obtained from source image and ab channels
     from Inference result.

     Parameters:
    -----------
    input_image_path : str
        the path of the (gray) image to obtain L channel

    inference_result : str
        Path to the .npy file containing the output of the inference function.
        (Consisting of ab channels)

    return value : numpy array
        Colorized image.
    """

    # load the result from the colorization
    a_channel = inference_result[0, :, :]
    b_channel = inference_result[1, :, :]

    # pull out L channel in original/source image
    mat = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    print(mat.shape)
    resize_mat = mat.astype(np.float32)
    resize_mat = 1.0 * resize_mat / 255
    resize_mat = cv2.cvtColor(resize_mat, cv2.COLOR_BGR2Lab)
    channels = cv2.split(resize_mat)
    l_channel = channels[0]

    # resize to match the size of original image L
    rows = mat.shape[0]
    cols = mat.shape[1]
    print(rows)
    a_channel_resize = cv2.resize(a_channel, (cols, rows))
    b_channel_resize = cv2.resize(b_channel, (cols, rows))

    # result Lab image
    result_image = cv2.merge([l_channel, a_channel_resize, b_channel_resize])
    print(result_image.shape)

    # convert back to rgb
    output_image = cv2.cvtColor(result_image, cv2.COLOR_Lab2BGR)
    return output_image * 255
