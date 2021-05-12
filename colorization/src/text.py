
import sys
import numpy
#import acl
import cv2
import os
import colorization as model_
import utils
import colorize_process

kTopNConfidenceLevels = numpy.uint32(5)
modelWidth = numpy.uint32(224)
modelHeight = numpy.uint32(224)
KMODELPATH = "../model/colorization.om"
run_mode = 0
FAILED = 1
SUCCESS = 0

# test: colorize_process.init an object
firstObject = colorize_process.ColorizeProcess("/home/ke/amos-ss2021-neural-network-enablement/Data/dog.png",
                                               modelWidth, modelHeight)
# test: object firstObject 's attribut
print(firstObject.modelWidth)

# test: object firstObject 's attribut 2
print(firstObject.deviceId)

# test: utils.py 's IsPathExist
print (utils.IsPathExist("/home/ke/amos-ss2021-neural-network-enablement/Data"))           # should return true
print (utils.IsPathExist("/home/ke/amos-ss2021-neural-network-enablement/Data/dog.png"))   # should  return ture

# test: utils.py 's IsDirectory
print (utils.IsDirectory("/home/ke/amos-ss2021-neural-network-enablement/Data"))           # should return false
print (utils.IsDirectory("/home/ke/amos-ss2021-neural-network-enablement/Data/dog.png"))   # should  return ture

# test: utils.py 's GetAllFiles
print (utils.GetAllFiles("/home/ke/amos-ss2021-neural-network-enablement/Data"))           # should return all the files' names


def Preprocess(self, imageFile):
    # read image using OPENCV
    mat = cv2.imread(imageFile, cv2.IMREAD_COLOR)
    # test: imshow the mat
    cv2.imshow("the pic", mat)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    # resize
    reiszeMat = numpy.zeros(modelWidth, numpy.float32)
    reiszeMat = cv2.resize(mat, (modelWidth, modelHeight), cv2.INTER_CUBIC)


    # deal image
    reiszeMat = cv2.convertScaleAbs(reiszeMat, cv2.CV_32FC3)
    reiszeMat = 1.0 * reiszeMat / 255
    # test: imshow the reiszeMat
    cv2.imshow("reiszeMat", reiszeMat)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    reiszeMat = numpy.float32(reiszeMat)
    reiszeMat = cv2.cvtColor(reiszeMat, cv2.COLOR_BGR2Lab)
    # test: imshow the reiszeMat after cvtColor
    cv2.imshow("cvtColor", reiszeMat)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    (L, A, B) = cv2.split(reiszeMat)
    cv2.imshow("L_channel", L)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    cv2.imshow("A_channel", A)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    cv2.imshow("B_channel", B)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    # pull out L channel and subtract 50 for mean-centering
    channels = cv2.split(reiszeMat)
    reiszeMatL = channels[0] - 50


    if numpy.any(mat) == None: #if (mat is empty)all ture return true, one false return false
        print("an empty mat")
        return FAILED
    else:
        print("not an empty mat")


Preprocess(firstObject, "/home/ke/amos-ss2021-neural-network-enablement/Data/dog.png")