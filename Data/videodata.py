import cv2
import os


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
