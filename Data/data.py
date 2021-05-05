import cv2
import os

def loadimage(inputImageDir):
    if os.path.isdir(inputImageDir):
        return inputImageDir
    else:
        return "path not found"

def storeimage(directory,colorized_data):
    newpath = os.path.join(directory, "Saved_images")
    os.makedirs(newpath)
    image = cv2.imread(colorized_data)
    cv2.imwrite(os.path.join(newpath, "Saved_image.png"), image)   # Saving images
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return newpath

def processVideo(path,videoName):
    videoName = os.path.join(path,videoName)
    video = cv2.VideoCapture(videoName)
    if (video.isOpened() == False):
        print("Error opening video")
    FPS = 60
    video.set(cv2.CAP_PROP_FPS, FPS)
    currentFrame = 0
    while (video.isOpened()):
        ret,frame = video.read()
        if ret == True:
            folder_name = os.path.join(path,'saved_frames', str(currentFrame) + '.png')
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
    return folder_name
