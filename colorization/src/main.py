'''
/**
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

* File main.cpp
* Description: dvpp sample main func
*/
'''

import cv2
import sys
import numpy
import 印度妹子的程序 # THE PROGRAMM FOR LOAD AND STORE FILE， IS MISSING
import colorize_process
import pyACL
import utils


kModelWidth = numpy.uint32(224);
kModelHeight = numpy.uint32(224);
KMODELPATH = "../model/colorization.om"

'''检查应用程序执行时的输入,程序执行要求输入图片目录参数'''
'''Getting a folder path, in which the original pictured are stored'''
inputImageDir = 印度妹子的程序.传我一个路径() #THE LOAD AND STORE PROGRAM SHOULD PASS ME A FOLDER PATH
if not inputImageDir:
	print("path is wrong")
	sys.exit(1)

'''实例化分类推理对象,参数为分类模型路径,模型输入要求的宽和高'''
'''Instantiate the classification reasoning (colorize_process) object, the parameters are the path of the classification model (KMODELPATH), 
and the width (kModelWidth) and height (kModelHeight) required by the model input'''
colorize = colorize_process.ColorizeProcess(KMODELPATH, kModelWidth, kModelHeight)

'''初始化分类推理的acl资源, 模型和内存'''
'''Initialize the acl resources, models and memory for classification inference'''
ret = colorize.Init()
if ret != 1: #check in the colorize_process.py, what is the return value
	print("Classification Init resource failed")
	sys.exit(0)
	
'''获取图片目录下所有的图片文件名'''
'''Get the names of all stored images in the folder path'''
'''ATTENTION!!! The atributes of function Utils.GetAllFiles(inoutImageDir) should be reduced! It should return a string list: fileVec'''
fileVec = utils.GetAllFiles(inputImageDir) #talk with utils.py responsor about the input and output value (fileVec = [], global fileVec?)
if len(fileVec) == 0:
	print("Failed to deal all empty path=", inputImageDir)
	sys.exit(0)
	
'''逐张图片推理'''
'''Inference the pictures one by one'''
for imageFile in fileVec:
	"""预处理图片:读取图片,将图片缩放到模型输入要求的尺寸"""
	"""preprocess: read the picture, reset to required size"""
	ret = colorize.Preprocess(imageFile)
	if ret != 1: # Check in colorize_process.py, what is the return value
		print("Read file ", imageFile, " failed, continue to read next")
		continue
	"""将预处理的图片送入模型推理,并获取推理结果"""
	"""send the picture into inference model and get the result back"""
	inferenceOutput = []
	ret = colorize.Inference(inferenceOutput)
	if ret != 1 or inferenceOutput == []: # check the return value
		print("Inference model inference output data failed")
		sys.exit(0)
	"""解析推理输出,并将推理得到的物体类别标记到图片上"""
	"""analyze the output and mark the type onto the picture"""
	ret = colorize.Postprocess(imageFile, inferenceOutput)
	if ret != 1: # check the return value
		print("Process model inference output data failed")
		sys.exit(0)

print("Execute sample success")
sys.exit(1)
