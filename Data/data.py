import cv2
import os

class Colorizer:
    def __init__(self):
        pass

    def processImage(self,path,imgName):
        imgName = os.path.join(path,imgName)
        self.img = cv2.imread(imgName,cv2.IMREAD_GRAYSCALE)
        cv2.imshow("image",self.img)
        filename = os.path.join(path,'saved_images','savedImage.jpg')
        cv2.imwrite(filename, self.img)   # saving image
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
                name = os.path.join(path,'saved_frames', str(currentFrame) + '.png')
                print('Creating...' + name)
                cv2.imshow('Frame', frame)
                cv2.imwrite(name, frame)
                currentFrame += 1
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        self.video.release()
        cv2.destroyAllWindows()


