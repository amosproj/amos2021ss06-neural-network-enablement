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

