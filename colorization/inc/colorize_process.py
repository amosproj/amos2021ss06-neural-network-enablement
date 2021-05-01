'''
Copyright 2020 Huawei Technologies Co., Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

File sample_process.h
Description: handle acl resource
'''

#pragma once #让所在的文件在一个单独的编译中只被包含一次
#include <memory>

import utils #//另一个已定义的头文件
import pyACL # tollkit library
import model_process #//另一个已定义的头文件

class ColorizeProcess(object):
    int32_t deviceId_ # type: int32_t
    ModelProcess model_ # type: ModelProcess
    modelPath_ # type: const char*
    modelWidth_ # type: uint32_t
    modelHeight_ # type: uint32_t
    inputDataSize_ # type: uint32_t
    inputBuf_ # type: void*
    runMode_ # type: aclrtRunMode
    isInited_ # type: boolean

    def __init__(self, modelPath, modelWidth, modelHeight):
        self.modelPath = modelPath
        self.modelWidth = modelWidth
        self.modelHeight = modelHeight
    def __del__(self):
    def Init(self) # return type:no，parameter:no
    def Preprocess(imageFile)# return type: Result. parameter: const string& imageFile
        return Result
    def Inference(inferenceOutput) # return type: Result. parameter:aclmdlDataset*& inferenceOutput
        return Result
    def Postprocess(origImageFile, modelOutput) # return type:Result，parameter:const string& origImageFile,aclmdlDataset* modelOutput
        return Result

    def InitResource(self) # return type:Result，parameter:no
        return Result
    def InitModel(omModelPath)  # return type:Result，parameter: const char* omModelPath
        return Result
    def GetInferenceOutputItem(itemDataSize, inferenceOutput) # return type:no，parameter: uint32_t& itemDataSize, aclmdlDataset* inferenceOutput
    def SaveImage(origImageFile, image) # return type:no，parameter:const string& origImageFile, cv::Mat& image
    def DestroyResource(self) # return type:no，parameter:no
