import cv2
import os

def video2frames(video_input_path, image_output_folder_path):
    '''This function is used to convert video into images.
     Args:
        video_input_path: filename of the video.
        image_output_folder_path: Output folder path containing images
     Returns:
        0 on success.
     '''
    video = cv2.VideoCapture(video_input_path)
    if (video.isOpened() is False):
        print("Error opening video")
    FPS = 60  # frames per second
    video.set(cv2.CAP_PROP_FPS, FPS)
    currentFrame = 0
    while (video.isOpened()):
        ret, frame = video.read()
        if ret is True:
            folder_name = os.path.join(image_output_folder_path, str(currentFrame) + '.png')
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
    return 0

# frames2video function :
# (image_input_folder_path, video_output_path)
# input path is a folder, output path includes the filename


def frames2video(image_input_folder_path, video_output_path):
    filelist = os.listdir(image_input_folder_path)
    FPS = 60  # adopted from above, maybe change into a lower value?
    fourcc = cv2.VideoWriter_fourcc("I", "4", "2", "0")
    video = cv2.VideoWriter(video_output_path, fourcc, FPS, (224, 224))
    for item in filelist:
        item = os.path.join(image_input_folder_path, item)
        img = cv2.imread(item)
        video.write(img)
    video.release()
