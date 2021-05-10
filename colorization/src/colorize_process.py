'''
* Copyright 2020 Huawei Technologies Co., Ltd
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at

* http://www.apache.org/licenses/LICENSE-2.0

* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.

* File sample_process.cpp
* Description: handle acl resource
'''


import numpy
import pyACL
import model_process
import utils
import cv2

kTopNConfidenceLevels = numpy.uint32(5)

class ColorizeProcess():
	modelPath_ = ""
	inputDataSize_ = modelWidth_ * modelHeight_ * 4 # Makro: define RGBF32_CHAN_SIZE(width, height) ((width) * (height) * 4)
	def __init__(self, modelPath, modelWidth, modelHeight):
		self.modelPath = modelpath
		self.modelWidth = modelWidth
		self.modelHeight = modelHeight
		self.deviceId_ = 0
		self.inputBuf_ = ""
		self.modelWidth_ = modelWidth
		self.modelHeight_ = modelHeight
		self.isInited_ = False
		ColorizeProcess.modelPath_ = modelPath


def InitResource():
	ACLCONFIGPATH = ".../src/acl.json"
	ret = pyACL.aclInit(ACLCONFIGPATH) # check methode in pyACL
	if ret != ACL_ERROR_NONE:
		print("Acl init failed")
		return 0
	print("Acl init success")

	# open device
	ret = pyACL.aclrtSetDevice(deviceId_) # check methode in pyACL
	if ret != ACL_ERROR_NONE:
		print("Acl open device ", deviceId_, " failed.")
		return 0
	print("Open device ", deviceId_, " success.")

	ret = pyACL.aclrtGetRunMode(runMode_) # check adresse vs. variable etc.
	if ret != ACL_ERROR_NONE:
		print("acl get run mode failed.")
		return 0

	return 1



def InitModel(OMMODELPATH): # check parameter
	ret = model_.LoadModelFromFileWithMem(OMMODELPATH)
	if ret != 1:
		print("execute LoadModelFromFileWithMem failed")
		return 0

	ret = model_.CreateDesc()
	if ret != 1:
		print("execute CreateDesc failed")
		return 0

	ret =model_.CreateOutput()
    if ret != 1:
        print("execute CreateOutput failed")
        return 0

    pyACL.aclrtMalloc(inputBuf_, inputDataSize_, ACL_MEM_MALLOC_HUGE_FIRST) # check methode and parameter in pyACL
    if inputBuf_ == "": # check return value
        print("Acl malloc image buffer failed.")
        return 0


    ret = model_.CreateInput(inputBuf_, inputDataSize_)
    if ret != 1: # check return value
        print("Create mode input dataset failed")
        return 0


    return 1

def Init():
	if isInited_:
		print("Classify instance is initied already!")
		return 1

	ret = InitResource()
    if ret != 1:
        print("Init acl resource failed")
        return 0

    ret = InitModel(modelPath_) # check parameter
    if ret != 1:
        print("Init model failed")
        return 0


    isInited_ = true
    return 1




def Preprocess(imageFile):
    # read image using OPENCV
    mat = cv2.imread(imageFile, cv2.IMREAD_COLOR)
    #resize
    reiszeMat = numpy.empty()
    reiszeMat = cv2.resize(mat, reiszeMat,None, fx = 224, fy = 224,
                            interpolation = cv2.INTER_CUBIC)

    # deal image
    reiszeMat.cv2.convertScaleAbs(reiszeMat, reiszeMat, CV_32FC3)
    reiszeMat = reiszeMat / 255
    cv2.cvtColor(reiszeMat, 44) # flag: cv::COLOR_BGR2Lab = 44,

    # pull out L channel and subtract 50 for mean-centering
    channels = cv.split(resizeMat)
    reiszeMatL = channels[0] - 50

    if mat == numpy.empty():
        return 0

    if runMode == ACL_HOST:
        #if run in AI1, need to copy the picture data to the device
        ret = aclrtMemcpy(inputBuf_, inputDataSize_, reiszeMatL,
                            inputDataSize_, ACL_MEMCPY_HOST_TO_DEVICE)
        if ret != ACL_ERROR_NONE:
            print("Copy resized image data to device failed.")
            return 0
        else:
            #reiszeMat is local variable , cant pass out of funktion, need to copy it
            memcpy(inputBuf_, reiszeMatL, inputDataSize_)

    return 1


def inference(inferenceOutput):
	ret = model_.Execute() # No idea what this model_.Execute() is, copied from c++ version
	if ret != 1: # check about the return value
		print("Execute model inerence failed")
		sys.exit(1) # should the program quit now?
	inferenceOutput = model_.GetModelOutputData() # deto check
	return 1 #The return value and quit critetia should be unified in general!!!


def postprocess(origImageFile, modelOutput):
    # reading the inference_image

    inference_result = cv2.imread(modelOutput)
    inference_result = cv2.resize(inference_result, (300, 300))
    cv2.imshow('Inference_result', inference_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # get ab channels from the model output
    a, b = cv2.split(inference_result)

    # pull out L channel in original/source image

    input_image = cv2.imread(origImageFile, cv2.IMREAD_COLOR)  # reading input image
    input_image = cv2.resize(input_image, (300, 300))
    input_image = np.float32(input_image)
    input_image = 1.0 * input_image / 255  # Normalizing the input image values
    bgrtolab = cv2.cvtColor(input_image, cv2.COLOR_BGR2LAB)
    cv2.imshow("Lab_channel", bgrtolab)
    (L, A, B) = cv2.split(bgrtolab)
    cv2.imshow("L_channel", L)
    cv2.imshow("A_channel", A)
    cv2.imshow("B_channel", B)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # resize to match the size of original image L

    height = input_image[0]
    width = input_image[1]
    a_channel = cv2.resize(a, (height, width))
    b_channel = cv2.resize(b, (height, width))

    # result Lab image

    result_image = cv2.merge(L, a_channel, b_channel)
    cv2.imshow('result_image', result_image)

    # convert back to rgb

    output_image = cv2.cvtColor(result_image, cv2.COLOR_Lab2BGR)
    output_image = output_image * 255
    cv2.imshow('output_image', output_image)

    return output_image

def saveimage(directory,colorized_data):
    newpath = os.path.join(directory, "Saved_images")
    os.makedirs(newpath)
    image = cv2.imread(colorized_data)
    cv2.imwrite(os.path.join(newpath, "Saved_image.png"), image)   # Saving images
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return newpath

def GetInferenceOutputItem(itemDataSize, inferenceOutput)  # input: uint32_t& itemDataSize, aclmdlDataset* inferenceOutput
    dataBuffer = aclmdlGetDatasetBuffer(inferenceOutput, 0)
    if dataBuffer == None:
        print("Get the dataset buffer from model inference output failed")
        return None


    dataBufferDev = aclGetDataBufferAddr(dataBuffer)
    if dataBufferDev == None:
        print("Get the dataset buffer address from model inference output failed")
        return None


    bufferSize = aclGetDataBufferSize(dataBuffer)
    if bufferSize == 0:
        print("The dataset buffer size of model inference output is 0 ")
        return None

    data = None
    if runMode_ == ACL_HOST :
        data = utils.CopyDataDeviceToHost(dataBufferDev, bufferSize)
        if data == None :
            print("Copy inference output to host failed")
            return None
    else :
        data = dataBufferDev
    itemDataSize = bufferSize
    return data


def DestroyResource()
    model_.Unload();
    model_.DestroyDesc();
    model_.DestroyInput();
    model_.DestroyOutput();

    ret = aclrtResetDevice(deviceId_)
    if ret != ACL_ERROR_NONE:
        print("reset device failed")

    print("end to reset device is %d", deviceId_)

    ret = aclFinalize()
    if ret != ACL_ERROR_NONE:
        print("finalize acl failed")

    print("end to finalize acl")
    aclrtFree(inputBuf_)
    inputBuf_ = None

