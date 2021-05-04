import cv2
import os

def loadimage(self,inputImageDir):
    self.inputImageDir = inputImageDir
    if os.path.isdir(self.inputImageDir):
        return self.inputImageDir
    else:
        return "path not found"

def storeimage(self,path,colorized_data):
    filename = os.path.join(path,'saved_images','savedImage.jpg')
    cv2.imwrite(filename, colorized_data)  # saving image
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return filename

def processVideo(self,path,videoName):
    videoName = os.path.join(path,videoName)
    self.video = cv2.VideoCapture(videoName)
    if (self.video.isOpened() == False):
        print("Error opening video")
    FPS = 60
    self.video.set(cv2.CAP_PROP_FPS, FPS)
    currentFrame = 0
    while (self.video.isOpened()):
        ret,frame = self.video.read()
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
    self.video.release()
    cv2.destroyAllWindows()
    return folder_name


