import cv2
import os
import acl_constants
import numpy
import shutil


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
    type = os.path.splitext(video_input_path)[-1]
    if (video.isOpened() is False) or (not (type == '.mp4')):
        print("Error opening video")
        return acl_constants.FAILED
    FPS = 60  # frames per second
    video.set(cv2.CAP_PROP_FPS, FPS)
    currentFrame = 0
    while (video.isOpened()):
        ret, frame = video.read()
        if ret is True:
            folder_name = os.path.join(image_output_folder_path,
                                       str(currentFrame) + '.png')
            print('Creating...' + folder_name)
            cv2.imshow('Frame', frame)
            cv2.imwrite(folder_name, frame)
            currentFrame += 1
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()
    return acl_constants.SUCCESS


def frames2video(image_input_folder_path, video_output_path):
    '''This function is used to convert images into a video.
    Args:
        image_input_folder_path: path to the split images.
        video_output_path: path to the merged video
    Returns:
        0 for SUCCESS.
        1 for FAILED.
    '''
    mat = cv2.imread(os.path.join(image_input_folder_path + '/0.png'),
                     cv2.IMREAD_COLOR)
    print(os.path.join(image_input_folder_path + '/0.png'))
    if numpy.any(mat) is None:
        return acl_constants.FAILED
    size = mat.shape[:2]
    FPS = 60
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video = cv2.VideoWriter(os.path.join(video_output_path, "out01.avi"),
                            fourcc, FPS, (size[1], size[0]))
    files = os.listdir(image_input_folder_path)
    length = len(files)
    for i in range(0, length):
        index = str(i)
        item = image_input_folder_path + '/' + index + '.png'
        print(item)
        img = cv2.imread(item)
        video.write(img)
    video.release()
    # after merged video delate the image_input_folder_path folder
    shutil.rmtree(image_input_folder_path)
    return acl_constants.SUCCESS
