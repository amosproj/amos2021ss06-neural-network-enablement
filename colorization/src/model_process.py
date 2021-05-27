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

* File model_process.py
* Description: handle model process
"""


import logging
import acl
import acl_constants


class Modelprocess:
    def __init__(self, loadflag=False, modelId=0, modelMemPtr=None, modelMemSize=0,
                 modelWeightPtr=None, modelWeightSize=0, modelDesc=None, input=None,
                 output=None):
        self.loadflag = loadflag
        self.modelId = modelId  # int, ID of the model to be inferred.
        self.modelMemPtr = modelMemPtr
        self.modelMemSize = modelMemSize  # int, model data length, in bytes
        self.modelWeightPtr = modelWeightPtr  # int, pointer of the model weight memory
        # (for storing weight data) on the device
        self.modelWeightSize = modelWeightSize
        self.modelDesc = modelDesc  # Description of the model.
        self.input = input  # int, pointer object of the input data of model inference
        self.output = output  # int, pointer object of the output data of model inference.

    def __del__(self):  # Calling destructor
        self.Unload()
        self.DestroyDesc()
        self.DestroyInput()
        self.DestroyOutput()

    def LoadModelFromFileWithMem(self, modelPath):

        """ Function usage: Loads offline model data (adapted to the Ascend AI processor)
        from a file.
        The offline model file is the *.om file that adapts to the Ascend AI processor
        Input Args: model_path: str, path for storing the offline model file. The file
        name is contained in the path.
        Returns: model_id: model ID generated after the model is loaded.
                 ret: int, error code.
                 0 indicates success.
                 Other values indicate failure. """

        if self.loadflag:
            logging.error("has already loaded a model")
            return 1
        work_size, weight_size, ret = acl.mdl.query_size(modelPath)
        if ret != acl_constants.ACL_ERROR_NONE:
            logging.error("query model failed, model file is %s", modelPath)
            return 1
        #self.modelMemSize = acl.mdl.get_num_outputs(self.modelDesc)
        ret = acl.rt.malloc(work_size, acl_constants.ACL_MEM_MALLOC_HUGE_FIRST)

        if ret != acl_constants.ACL_ERROR_NONE:
            logging.error("malloc buffer for mem failed, require size is %i",
                          work_size)
            return 1
        ret = acl.rt.malloc(weight_size, acl_constants.ACL_MEM_MALLOC_HUGE_FIRST)
        if ret != acl_constants.ACL_ERROR_NONE:
            logging.error("malloc buffer for weight failed, require size is %i",
                          weight_size)
            return 1
        model_id, ret = acl.mdl.load_from_file_with_mem(modelPath,
                                                        self.modelMemPtr,
                                                        self.modelMemSize,
                                                        self.modelWeightPtr,
                                                        self.modelWeightSize)
        if ret != acl_constants.ACL_ERROR_NONE:
            logging.error("load model from file failed, model file is %s", modelPath)
            return 1
        self.loadflag = True
        logging.info("load model %s success", modelPath)
        return 0

    def CreateDesc(self):

        """ Function Usage: Creates data of the aclmdlDesc type.
            Input Args: NONE
            returns:  int, error code.
                     0 indicates success.
                     1 indicates failure. """

        self.modelDesc = acl.mdl.create_desc()
        if self.modelDesc is None:
            logging.error("create model description failed")
            return 1
        ret = acl.mdl.get_desc(self.modelDesc, self.modelId)
        if ret is not None:
            logging.error("get model description failed")
            return 1
        logging.info("create model description success")
        return 0

    def DestroyDesc(self):

        """ Function Usage: Destroys data of the aclmdlDesc type.
            Input Args: None
            returns: int, error code.
                     0 indicates success.
                     1 indicates failure. """

        if self.modelDesc is not None:
            acl.mdl.destroy_desc(self.modelDesc)
            self.modelDesc = None

    def CreateInput(self, inputDataBuffer, bufferSize):

        """ Function Usage: Creates data of the aclmdlDataset type.
            Input Args: inputDataBuffer:
                        bufferSize
            returns: int, error code.
                     0 indicates success.
                     1 indicates failure. """

        self.input = acl.mdl.create_dataset()
        if self.input is None:
            logging.error("can't create data buffer, create input failed")
            return 1
        inputData = acl.create_data_buffer(inputDataBuffer, bufferSize)
        if inputData is None:
            logging.error("can't create data buffer, create input failed")
            return 1
        dataset, ret = acl.mdl.add_dataset_buffer(self.input, inputData)
        if inputData is None:
            logging.error("can't add data buffer, create input failed")
            acl.destroy_data_buffer(inputData)
            inputData = None
            return 1
        return 0

    def DestroyInput(self):
        """Function Usage:
           Input Args: None
           returns: None"""
        if self.input is None:
            return
        for i in range(0, acl.mdl.get_dataset_num_buffers(self.input)):
            dataBuffer = acl.mdl.get_dataset_buffer(self.input, i)
            acl.destroy_data_buffer(dataBuffer)
        acl.mdl.destroy_dataset(self.input)
        self.input = None

    def CreateOutput(self):
        """Function Usage:
           returns: int, error code.
                    0 indicates success.
                    1 indicates failure."""
        if self.modelDesc is None:
            logging.error("no model description, create output failed")
            return 1
        self.output = acl.mdl.create_dataset()
        if self.output is None:
            logging.error("cannot create dataset,create output failed")
            return 1
        outputSize = acl.mdl.get_num_outputs(self.modelDesc)
        for i in range(0, outputSize):
            buffer_size = acl.mdl.get_output_size_by_index(self.modelDesc, i)
            outputBuffer = None
            ret = acl.rt.malloc(buffer_size, acl_constants.ACL_MEM_MALLOC_NORMAL_ONLY)
            if ret != acl_constants.ACL_ERROR_NONE:
                logging.error("can't malloc buffer, size is %zu, create output failed",
                              buffer_size)
                return 1
            outputData = acl.create_data_buffer(outputBuffer, buffer_size)
            if ret != acl_constants.ACL_ERROR_NONE:
                logging.error("can't create data buffer, create output failed")
                acl.rt.free(outputBuffer)
                return 1
            ret = acl.mdl.add_dataset_buffer(self.output, outputData)
            if ret != acl_constants.ACL_ERROR_NONE:
                logging.error("can't add data buffer, create output failed")
                acl.rt.free(outputBuffer)
                acl.destroy_data_buffer(outputData)
                return 1
        logging.info("create model output success")
        return 0

    def DestroyOutput(self):
        """Function Usage:
           Input Args: None
           returns: None """
        if self.output is None:
            return
        for i in range(0, acl.mdl.get_dataset_num_buffers(self.output)):
            dataBuffer = acl.mdl.get_dataset_buffer(self.output, i)
            data = acl.get_data_buffer_addr(dataBuffer)
            acl.rt.free(data)
            acl.destroy_data_buffer(dataBuffer)
        acl.mdl.destroy_dataset(self.output)
        self.output = None

    def Execute(self):
        """Function usage: Executes model inference until the result is returned.
           Input Args: None
           Returns: ret: int, error code.
                    0 indicates success.
                    Other values indicate failure."""
        ret = acl.mdl.execute(self.modelId, self.input, self.output)
        if ret != acl_constants.ACL_ERROR_NONE:
            logging.error("execute model failed, modelId is %u", self.modelId)
            return 1
        logging.info("model execute success")
        return 0

    def Unload(self):
        """ Function Usage: DestroyDesc
            Input Args: None
            returns: None """
        if not self.loadflag:
            return
        ret = acl.mdl.unload(self.modelId)
        if ret != acl_constants.ACL_ERROR_NONE:
            logging.error("unload model failed, modelId is %u", self.modelId)
        if self.modelDesc is not None:
            acl.mdl.destroy_desc(self.modelDesc)
            self.modelDesc = None
        if self.modelMemPtr is not None:
            acl.rt.free(self.modelMemPtr)
            self.modelMemPtr = None
            self.modelMemSize = 0
        if self.modelWeightPtr is not None:
            acl.rt.free(self.modelWeightPtr)
            self.modelWeightPtr = None
            self.modelWeightSize = 0
        self.loadflag = False
        logging.info("unload model success, modelId is %u", self.modelId)

    def GetModelOutputData(self):
        """Function Usage: Returns the output value
           Input Args: None
           returns: output"""
        return self.output
