import cv2
import os


# expected function:
# (video_input_path, image_output_folder_path)
# input path includes filename, output path is just a folder
def video2frames(videopath, videoName):
    '''This function is used to convert video into images.
     Args:
        videopath: path to the video.
        videoName: name of the video eg. greyscalevideo.mp4
     Returns:
        path to the splitted images.
     '''
    videoName = os.path.join(videopath, videoName)
    video = cv2.VideoCapture(videoName)
    if (video.isOpened() is False):
        print("Error opening video")
    FPS = 60  # frames per second
    video.set(cv2.CAP_PROP_FPS, FPS)
    currentFrame = 0
    newpath = os.path.join(videopath, "Saved_frames")
    while (video.isOpened()):
        ret, frame = video.read()
        if ret is True:
            folder_name = os.path.join(newpath, str(currentFrame) + '.png')
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
    return newpath

# frames2video function :
# (image_input_folder_path, video_output_path)
# input path is a folder, output path includes the filename


def frames2video(image_input_folder_path, video_output_path):
    filelist = os.listdir(image_input_folder_path)
    FPS = 60  # adopted from above
    fourcc = cv2.VideoWriter_fourcc("I", "4", "2", "0")
    video = cv2.VideoWriter(video_output_path, fourcc, FPS, (224, 224))
    for item in filelist:
        item = os.path.join(image_input_folder_path, item)
        img = cv2.imread(item)
        video.write(img)
    video.release()
