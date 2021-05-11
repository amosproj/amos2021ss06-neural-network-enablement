
import sys
import numpy
import acl
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

firstObject = colorize_process.ColorizeProcess("/home/ke/amos-ss2021-neural-network-enablement/Data/dog.png",
                                               modelWidth, modelHeight)

print(firstObject.modelWidth)

print(firstObject.deviceId)

success_or_not = firstObject.Preprocess("/home/ke/amos-ss2021-neural-network-enablement/Data/dog.png")
print(success_or_not)