import numpy
import copy
import acl
import cv2
import utils
import acl_constants
import os
from model_process import Modelprocess

"""
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
"""

# constant variables
FAILED = 1
SUCCESS = 0


class ColorizeProcess:

    def __init__(self, modelPath, modelWidth=numpy.uint32(224),
                 modelHeight=numpy.uint32(224),
                 deviceId=0, inputBuf=None, isInit=False, run_mode=0):
        """
        This function does the initiation of variables of colorize process


        Parameters:
        -----------
        modelPath : str
            the model path for colorization (incl. filename)
        modelWidth : numpy.uint32(224)
            the width a image should have, in order to be colorized
        modelHeight : numpy.uint32(224)
            the height a image should have, in order to be colorized
        deviceID : int
            the ID of the device
        inputBuf : int
            pointer to allocated memory
        isInited : boolean
            Ture: the object is inited
            False: the object is not inited yet
        run_mode : int
            the mode of run.
            0: ACL_DEVICE
            1: ACL_HOST


        return value : None
        """

        self.modelPath = modelPath
        self.modelWidth = modelWidth
        self.modelHeight = modelHeight
        self.inputDataSize = int(4 * modelWidth * modelHeight)
        self.deviceId = deviceId
        self.inputBuf = inputBuf
        self.isInited = isInit
        self.run_mode = run_mode
        self.model = Modelprocess()

        self.itemDataSize = 0

    def __del__(self):
        self.DestroyResource()

    def InitResource(self):
        """
        This function does the initiation of resource.
        Set and get features through acl.


        Parameters:
        -----------
        input : none

        return value : int
            on success this function returns 0
            on failure this function returns 1
        """
        #  ACLCONFIGPATH = os.path.join(
        #      os.path.abspath(os.path.dirname(__file__)), './acl.json')
        #  ret = acl.init(ACLCONFIGPATH)
        ret = acl.init()  # no configuration.info as argument
        if ret != acl_constants.ACL_ERROR_NONE:
            print("Acl init failed")
            return FAILED
        print("Acl init success")

        # open device
        ret = acl.rt.set_device(self.deviceId)
        if ret != acl_constants.ACL_ERROR_NONE:
            print("Acl open device ", self.deviceId, " failed.")
            return FAILED
        print("Open device ", self.deviceId, " success.")

        (self.run_mode, ret) = acl.rt.get_run_mode()
        if ret != acl_constants.ACL_ERROR_NONE:
            print("acl get_run_mode failed.")
            return FAILED
        return SUCCESS

    def InitModel(self, OMMODELPATH):
        """
        This function does the initiation of model.


        Parameters:
        -----------
        OMMODELPATH : constant str
            the model path for colorization

        return value : int
            on success this function returns 0
            on failure this function returns 1
        """

        ret = self.model.LoadModelFromFileWithMem(OMMODELPATH)
        if ret != SUCCESS:
            print("execute LoadModelFromFileWithMem failed")
            return FAILED

        ret = self.model.CreateDesc()
        if ret != SUCCESS:
            print("execute CreateDesc failed")
            return FAILED
        ret = self.model.CreateOutput()
        if ret != SUCCESS:
            print("execute CreateOutput failed")
            return FAILED

        (self.inputBuf, ret) = acl.rt.malloc(self.inputDataSize,
                                             acl_constants.
                                             ACL_MEM_MALLOC_HUGE_FIRST)
        if self.inputBuf is None:
            print("Acl malloc image buffer failed.")
            return FAILED

        ret = self.model.CreateInput(self.inputBuf, self.inputDataSize)
        if ret != SUCCESS:  # check return value
            print("Create mode input dataset failed")
            return FAILED
        return SUCCESS

    def Init(self):
        """
        This function does the initiation of model.


        Parameters:
        -----------
        input: none

        return value : int
            on success this function returns 0
            on failure this function returns 1
        """

        if self.isInited:
            print("Classify instance is inited already!")
            return SUCCESS

        ret = self.InitResource()
        if ret != SUCCESS:
            print("Init acl resource failed")
            return FAILED

        ret = self.InitModel(self.modelPath)
        if ret != SUCCESS:
            print("Init model failed")
            return FAILED
        self.isInited = True
        return SUCCESS

    def Preprocess(self, imageFile):
        """
        This function reads the imageFile as a float-Matrix;
        downsize to modelWidth*modelHeight;
        if the process run in Atlas, copys the picture data to the device;
        copys the L channel into the malloc memory location.

        Parameters:
        -----------
        input:
        imageFile : str
            the path of the picture

        return value : int
            on success this function returns 0
            on failure this function returns 1
        """
        # read image using OPENCV
        mat = cv2.imread(imageFile, cv2.IMREAD_COLOR)
        if numpy.any(mat) is None:  # if matrix is empty, every term is none
            return FAILED
        mat = mat.astype(numpy.float32)

        # resize
        reiszeMat = cv2.resize(mat, (self.modelWidth, self.modelHeight))

        # deal image
        reiszeMat = 1.0 * reiszeMat / 255
        reiszeMat = cv2.cvtColor(reiszeMat, cv2.COLOR_BGR2Lab)

        # pull out L channel and subtract 50 for mean-centering
        # channel[0] = L, [1] = A, [2] = B
        channels = cv2.split(reiszeMat)
        reiszeMatL = acl.util.numpy_to_ptr(channels[0] - 50)

        if self.run_mode == 1:  # if run on host
            # if run in host, need to copy the picture data to the device
            # address:inputBuf
            ret = acl.rt.memcpy(self.inputBuf, self.inputDataSize, reiszeMatL,
                                self.inputDataSize,
                                acl_constants.ACL_MEMCPY_HOST_TO_DEVICE)

        else:  # if run on the device
            # 'reiszeMatL' is local variable , cant pass out of function,
            # need to copy it to the device address: inputBuf
            ret = acl.rt.memcpy(self.inputBuf, self.inputDataSize, reiszeMatL,
                                self.inputDataSize,
                                acl_constants.ACL_MEMCPY_DEVICE_TO_DEVICE)

        if ret != acl_constants.ACL_ERROR_NONE:  # ACL_ERROR_NONE will be
            # deprecated in future releases.
            # could Use ACL_SUCCESS instead.
            print("Copy resized image data to device failed.")
            return FAILED
        return SUCCESS

    def inference(self, inference_output_path):
        """
        This function activate the model process after preprocess,
        and get result back.


        Parameters:
        -----------
        input:

        inference_output_path:
            file path where the result is saved after colorization

        result : int
            on success this function returns 0
            on failure this function returns 1
        """

        ret = self.model.Execute()
        if ret != SUCCESS:
            print("Execute model inference failed")
            return FAILED

        inferenceOutput = self.model.GetModelOutputData()

        dataSize = 0
        dataPtr = self.GetInferenceOutputItem(dataSize, inferenceOutput)

        size = self.itemDataSize

        np_output_ptr, ret = acl.rt.malloc(size, acl_constants.ACL_MEM_MALLOC_NORMAL_ONLY)
        print("image ", np_output_ptr)

        ret = acl.rt.memcpy(np_output_ptr, size, dataPtr, size, 3)
        if ret != acl_constants.ACL_ERROR_NONE:
            print("Copy image to np array failed for memcpy error ", ret)
            return FAILED

        data = copy.deepcopy(acl.util.ptr_to_numpy(np_output_ptr, (size, ),
                                                   acl_constants.NPY_BYTE))

        numpy.save(inference_output_path, data)

        return SUCCESS

    def postprocess(self, input_image_path, inference_output_path, output_image_path):
        """This function converts LAB image to BGR image (colorization)
        and save it.
         It combines L channel obtained from source image and ab channels
         from Inference result.

         Parameters:
        -----------
        input_image_path : str
            the path of the (gray) image to obtain L channel

        inference_output_path : str
            Path to the .npy file containing the output of the inference function.
            (Consisting of ab channels)

        output_image_path : str
            the path of the (colorized) image to save after processing

        return value :
            on success this function returns 0
            on failure this function returns 1
        """

        # get a and b channel result data
        if not os.path.isfile(inference_output_path):
            print('Output of inference not found.')
            return FAILED

        print('SUCCESS!!')

        # load the result from the colorization
        inference_result = numpy.load(inference_output_path)
        inference_result = numpy.reshape(inference_result, (int(self.modelWidth/2),
                                                            int(self.modelHeight/2), 2))
        a_channel, b_channel = cv2.split(inference_result)

        # pull out L channel in original/source image
        input_image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
        input_image = numpy.float32(input_image)
        input_image = 1.0 * input_image / 255  # Normalizing
        bgrtolab = cv2.cvtColor(input_image, cv2.COLOR_BGR2LAB)
        (L, A, B) = cv2.split(bgrtolab)

        # resize to match the size of original image L
        rows = input_image.shape[0]
        cols = input_image.shape[1]
        a_channel = a_channel.astype('float32')
        b_channel = a_channel.astype('float32')
        a_channel_resize = cv2.resize(a_channel, (cols, rows))
        b_channel_resize = cv2.resize(b_channel, (cols, rows))

        # result Lab image
        result_image = cv2.merge((L, a_channel_resize, b_channel_resize))
        print(result_image.shape)

        # convert back to rgb
        output_image = cv2.cvtColor(result_image, cv2.COLOR_Lab2BGR)
        output_image = output_image * 255
        cv2.imwrite(output_image_path, output_image)
        # self.SaveImage(imageFile, output_image)
        return SUCCESS

    def SaveImage(self, origImageFile, image):
        """This function saves the colorized image in a specified path
           Parameters:
           -----------
           origImageFile: str
              the path of original image file
           image: image
              colorized image obtained from postprocess
           returns: None"""
        newpath = os.path.join(origImageFile, "Saved_images")
        os.makedirs(newpath)
        image = cv2.imread(image)
        cv2.imwrite(os.path.join(newpath, "Saved_image.png"), image)  # Saving
        # images
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def GetInferenceOutputItem(self, itemDataSize, inferenceOutput):
        """This function obtains the first Buffer
        of inferenceOutput in dataBuffer;
        obtains the address object of data of the dataBuffer;
        obtains the memory size of data of the dataBuffer in bytes

        Parameters:
        -----------
        input:
        itemDataSize: int
            data size
        inferenceOutput: aclmdlDataset
            pointer of the result saved after colorization

        return value :
        data: int
        the dataset buffer address from model inference output
        """
        dataBuffer = acl.mdl.get_dataset_buffer(inferenceOutput, 0)
        if dataBuffer is None:
            print("Get the dataset buffer from model inference output failed")
            return None

        dataBufferDev = acl.get_data_buffer_addr(dataBuffer)
        if dataBufferDev is None:
            print(
                "Get the dataset buffer address from model inference output "
                "failed")
            return None

        bufferSize = acl.get_data_buffer_size(dataBuffer)
        if bufferSize == 0:
            print("The dataset buffer size of model inference output is 0 ")
            return None
        data = None
        if self.run_mode == acl_constants.ACL_HOST:
            data = utils.CopyDataDeviceToHost(dataBufferDev, bufferSize)
            if data is None:
                print("Copy inference output to host failed")
                return None
        else:
            data = dataBufferDev

        self.itemDataSize = bufferSize
        return data

    def DestroyResource(self):
        """
        This function uninstalls the model and releases resources after the
        model inference is complete; destroys data of the aclmdlDesc type;
        destroys input and output data; resets the computing device and
        releases the resources (including the default context and stream,
        and all streams created in the default context) on the device;
        deinitializes ACL before the application processends;
        frees the memory on the device allocated by acl.rt.malloc.

        Parameters:
        -----------
        input:
        self: class ColorizeProcess

        return value :
        None
        """

        print('called destroy resource of colorize_process')
        if (self.inputBuf is None) or (self.inputDataSize == 0):
            print("Release image abnormaly, data is None")
            return FAILED

        acl.rt.free(self.inputBuf)

        self.inputBuf = None
        self.inputDataSize = 0
        print('finished destroy resource of colorize_process')
