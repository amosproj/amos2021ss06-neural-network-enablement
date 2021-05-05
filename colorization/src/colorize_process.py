'''/**
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
*/'''

import cv2
import numpy
import pyACL
import model_process
import utils

kTopNConfidenceLevels = numpy.uint32_t(5);


ColorizeProcess::ColorizeProcess(const char* modelPath,
                                 uint32_t modelWidth, uint32_t modelHeight)
:deviceId_(0), inputBuf_(nullptr),
modelWidth_(modelWidth), modelHeight_(modelHeight), isInited_(false){
    modelPath_ = modelPath;
    inputDataSize_ = RGBF32_CHAN_SIZE(modelWidth_, modelHeight_);
}

ColorizeProcess::~ColorizeProcess() {
    DestroyResource();
}

Result ColorizeProcess::InitResource() {
    // ACL init
    const char *aclConfigPath = "../src/acl.json";
    aclError ret = aclInit(aclConfigPath);
    if (ret != ACL_ERROR_NONE) {
        ERROR_LOG("Acl init failed");
        return FAILED;
    }
    INFO_LOG("Acl init success");

    // open device
    ret = aclrtSetDevice(deviceId_);
    if (ret != ACL_ERROR_NONE) {
        ERROR_LOG("Acl open device %d failed", deviceId_);
        return FAILED;
    }
    INFO_LOG("Open device %d success", deviceId_);

    ret = aclrtGetRunMode(&runMode_);
    if (ret != ACL_ERROR_NONE) {
        ERROR_LOG("acl get run mode failed");
        return FAILED;
    }

    return SUCCESS;
}

Result ColorizeProcess::InitModel(const char* omModelPath) {
    Result ret = model_.LoadModelFromFileWithMem(omModelPath);
    if (ret != SUCCESS) {
        ERROR_LOG("execute LoadModelFromFileWithMem failed");
        return FAILED;
    }

    ret = model_.CreateDesc();
    if (ret != SUCCESS) {
        ERROR_LOG("execute CreateDesc failed");
        return FAILED;
    }

    ret = model_.CreateOutput();
    if (ret != SUCCESS) {
        ERROR_LOG("execute CreateOutput failed");
        return FAILED;
    }

    aclrtMalloc(&inputBuf_, (size_t)(inputDataSize_), ACL_MEM_MALLOC_HUGE_FIRST);
    if (inputBuf_ == nullptr) {
        ERROR_LOG("Acl malloc image buffer failed.");
        return FAILED;
    }

    ret = model_.CreateInput(inputBuf_, inputDataSize_);
    if (ret != SUCCESS) {
        ERROR_LOG("Create mode input dataset failed");
        return FAILED;
    }

    return SUCCESS;
}

Result ColorizeProcess::Init() {
    if (isInited_) {
        INFO_LOG("Classify instance is initied already!");
        return SUCCESS;
    }

    Result ret = InitResource();
    if (ret != SUCCESS) {
        ERROR_LOG("Init acl resource failed");
        return FAILED;
    }

    ret = InitModel(modelPath_);
    if (ret != SUCCESS) {
        ERROR_LOG("Init model failed");
        return FAILED;
    }

    isInited_ = true;
    return SUCCESS;
}


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
        #AI1上运行时,需要将图片数据拷贝到device侧
        ret = aclrtMemcpy(inputBuf_, inputDataSize_, reiszeMatL,
                            inputDataSize_, ACL_MEMCPY_HOST_TO_DEVICE)
        if ret != ACL_ERROR_NONE:
            print("Copy resized image data to device failed.")
            return 0
        else:
            #Atals200DK上运行时,数据拷贝到本地即可.
            #reiszeMat是局部变量,数据无法传出函数,需要拷贝一份
            memcpy(inputBuf_, reiszeMatL, inputDataSize_)

    return 1


def inference(inferenceOutput):
	ret = model_.Execute() # No idea what this model_.Execute() is, copied from c++ version
	if ret != 1: # check about the return value
		print("Execute model inerence failed")
		sys.exit(1) # should the program quit now?
	inferenceOutput = model_.GetModelOutputData() # deto check
	return 1 #The return value and quit critetia should be unified in general!!!



Result ColorizeProcess::Postprocess(const string& imageFile, aclmdlDataset* modelOutput)
{
    uint32_t dataSize = 0;
    void* data = GetInferenceOutputItem(dataSize, modelOutput);
    if (data == nullptr) return FAILED;

    uint32_t size = static_cast<uint32_t>(dataSize) / sizeof(float);

    // get a channel and b channel result data
    cv::Mat mat_a(56, 56, CV_32FC1, const_cast<float*>((float*)data));
    cv::Mat mat_b(56, 56, CV_32FC1, const_cast<float*>((float*)data + size / 2));

    // pull out L channel in original image
    cv::Mat mat = cv::imread(imageFile, CV_LOAD_IMAGE_COLOR);
    mat.convertTo(mat, CV_32FC3);
    mat = 1.0 * mat / 255;
    cv::cvtColor(mat, mat, CV_BGR2Lab);
    std::vector<cv::Mat> channels;
    cv::split(mat, channels);

    // resize to match size of original image L
    int r = mat.rows;
    int c = mat.cols;
    cv::Mat mat_a_up(r, c, CV_32FC1);
    cv::Mat mat_b_up(r, c, CV_32FC1);
    cv::resize(mat_a, mat_a_up, cv::Size(c, r));
    cv::resize(mat_b, mat_b_up, cv::Size(c, r));

    // result Lab image
    cv::Mat newChannels[3] = { channels[0], mat_a_up, mat_b_up };
    cv::Mat resultImage;
    cv::merge(newChannels, 3, resultImage);

    //convert back to rgb
    cv::cvtColor(resultImage, resultImage, CV_Lab2BGR);
    resultImage = resultImage * 255;
    SaveImage(imageFile, resultImage);

    return SUCCESS;
}

void ColorizeProcess::SaveImage(const string& origImageFile, cv::Mat& image) {
    int pos = origImageFile.find_last_of("/");

    string filename(origImageFile.substr(pos + 1));
    stringstream sstream;
    sstream.str("");
    sstream << "./output/out_" << filename;

    string outputPath = sstream.str();
    cv::imwrite(outputPath, image);
}

void* ColorizeProcess::GetInferenceOutputItem(uint32_t& itemDataSize,
                                              aclmdlDataset* inferenceOutput) {
    aclDataBuffer* dataBuffer = aclmdlGetDatasetBuffer(inferenceOutput, 0);
    if (dataBuffer == nullptr) {
        ERROR_LOG("Get the dataset buffer from model "
            "inference output failed");
        return nullptr;
    }

    void* dataBufferDev = aclGetDataBufferAddr(dataBuffer);
    if (dataBufferDev == nullptr) {
        ERROR_LOG("Get the dataset buffer address "
            "from model inference output failed");
        return nullptr;
    }

    size_t bufferSize = aclGetDataBufferSize(dataBuffer);
    if (bufferSize == 0) {
        ERROR_LOG("The dataset buffer size of "
                  "model inference output is 0 ");
        return nullptr;
    }

    void* data = nullptr;
    if (runMode_ == ACL_HOST) {
        data = Utils::CopyDataDeviceToHost(dataBufferDev, bufferSize);
        if (data == nullptr) {
            ERROR_LOG("Copy inference output to host failed");
            return nullptr;
        }
    } else {
        data = dataBufferDev;
    }

    itemDataSize = bufferSize;
    return data;
}

void ColorizeProcess::DestroyResource()
{
    model_.Unload();
    model_.DestroyDesc();
    model_.DestroyInput();
    model_.DestroyOutput();
    aclError ret;

    ret = aclrtResetDevice(deviceId_);
    if (ret != ACL_ERROR_NONE) {
        ERROR_LOG("reset device failed");
    }
    INFO_LOG("end to reset device is %d", deviceId_);

    ret = aclFinalize();
    if (ret != ACL_ERROR_NONE) {
        ERROR_LOG("finalize acl failed");
    }
    INFO_LOG("end to finalize acl");
    aclrtFree(inputBuf_);
    inputBuf_ = nullptr;
}
