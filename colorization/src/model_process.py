import logging
import acl

class Modelprocess:
    def __init__(self,loadflag=False,modelId=0,modelMemPtr=None,modelMemSize=0,modelWeightPtr=None,modelWeightSize=0,modelDesc=None,input=None,output=None):
        self.loadflag = loadflag
        self.modelId = modelId             # int, ID of the model to be inferred.
        self.modelMemPtr = modelMemPtr
        self.modelMemSize = modelMemSize  # int, model data length, in bytes
        self.modelWeightPtr = modelWeightPtr   # int, pointer of the model weight memory (for storing weight data) on the device. The pointer is managed by users.
        self.modelWeightSize = modelWeightSize   # int, size of the weight memory required by the model, in bytes
        self.modelDesc = modelDesc # Description of the model.
        self.input = input  # int, pointer object of the input data of model inference
        self.output = output    # int, pointer object of the output data of model inference.

    def LoadModelFromFileWithMem(self,modelPath):

        """ Function usage: Loads offline model data (adapted to the Ascend AI processor) from a file.
        The offline model file is the *.om file that adapts to the Ascend AI processor
        Input Args: model_path: str, path for storing the offline model file. The file name is contained in the path.
        Returns: model_id: model ID generated after the model is loaded.
                 ret: int, error code.
                 0 indicates success.
                 Other values indicate failure. """

        if self.loadflag:
            logging.error("has already loaded a model")
            return 1
        work_size, weight_size, ret = acl.mdl.query_size(modelPath,self.modelMemSize,self.modelWeightSize)
        if ret != ACL_ERROR_None:
            logging.error("query model failed, model file is %s", modelPath)
            return 1
        model_id, ret = acl.mdl.load_from_file_with_mem(modelPath, self.modelId, self.modelMemPtr, self.modelMemSize,self.modelWeightPtr,self.modelWeightSize)
        if ret != ACL_ERROR_NONE:
            logging.error("load model from file failed, model file is %s", modelPath)
            return 1
        self.loadflag = True
        logging.info("load model %s success", modelPath)
        return 0

    def CreateDesc(self):
        self.modelDesc = acl.mdl.create_desc()
        if self.modelDesc is None:
            logging.error("create model description failed")
            return 1
        ret = acl.mdl.get_desc(self.modelDesc,self.modelId)
        if ret != None:
            logging.error("get model description failed")
            return 1
        logging.info("create model description success")
        return 0

    def DestroyDesc(self):
        if self.modelDesc != None:
            acl.mdl.destroy_desc(self.modelDesc)
            self.modelDesc = None

    def CreateInput(self,inputDataBuffer,bufferSize):
        self.input = acl.mdl.create_dataset()
        if self.input is None:
            logging.error("can't create data buffer, create input failed")
            return 1
        inputData = acl.create_data_buffer(inputDataBuffer,bufferSize)
        if inputData is None:
            logging.error("can't create data buffer, create input failed")
            return 1
        dataset,ret = acl.mdl.add_dataset_buffer(self.input,inputData)
        if inputData is None:
            logging.error("can't add data buffer, create input failed")
            acl.destroy_data_buffer(inputData)
            inputData = None
            return 1
        return 0

    def DestroyInput(self):
        if self.input is None:
            return
        for i in range(0,acl.mdl.get_dataset_num_buffers(self.input)):
            dataBuffer = acl.mdl.get_dataset_buffer(self.input,i)
            acl.destroy_data_buffer(dataBuffer)
        acl.mdl.destroy_dataset(self.input)
        self.input = None

    def CreateOutput(self):
        if self.modelDesc is None:
            logging.error("no model description, create output failed")
            return 1
        self.output = acl.mdl.create_dataset()
        if self.output is None:
            logging.error("cannot create dataset,create output failed")
            return 1
        outputSize = acl.mdl.get_num_outputs(self.modelDesc)
        for i in range(0,outputSize):
            buffer_size = acl.mdl.get_output_size_by_index(self.modelDesc,i)
            outputBuffer = None
            ret = acl.rt.malloc(outputBuffer,buffer_size,ACL_MEM_MALLOC_NORMAL_ONLY)
            if ret != ACL_ERROR_NONE:
                logging.error("can't malloc buffer, size is %zu, create output failed",buffer_size)
                return 1
            outputData = acl.create_data_buffer(outputBuffer,buffer_size)
            if ret != ACL_ERROR_NONE:
                logging.error("can't create data buffer, create output failed")
                acl.rt.free(outputBuffer)
                return 1
            ret = acl.mdl.add_dataset_buffer(self.output,outputData)
            if ret != ACL_ERROR_NONE:
                logging.error("can't add data buffer, create output failed")
                acl.rt.free(outputBuffer)
                acl.destroy_data_buffer(outputData)
                return 1
        logging.info("create model output success")
        return 0

    def DestroyOutput(self):
        if self.output is None:
            return
        for i in range(0,acl.mdl.get_dataset_num_buffers(self.output)):
            dataBuffer = acl.mdl.get_dataset_buffer(self.output,i)
            data = acl.get_data_buffer_addr(dataBuffer)
            acl.rt.free(data)
            acl.destroy_data_buffer(dataBuffer)
        acl.mdl.destroy_dataset(self.output)
        self.output = None

    def Execute(self):
        """Function usage: Executes model inference until the result is returned.
           Returns: ret: int, error code.
            0 indicates success.
            Other values indicate failure."""
        ret = acl.mdl.execute(self.modelId, self.input, self.output)
        if ret != ACL_ERROR_NONE:
            logging.error("execute model failed, modelId is %u", self.modelId)
            return 1
        logging.info("model execute success")
        return 0

    def Unload(self):
        if not self.loadflag:
            return
        ret = acl.mdl.unload(self.modelId)
        if ret != ACL_ERROR_NONE:
            logging.error("unload model failed, modelId is %u", self.modelId)
        if self.modelDesc != None:
            acl.mdl.destroy_desc(self.modelDesc)
            self.modelDesc = None
        if self.modelMemPtr != None:
            acl.rt.free(self.modelMemPtr)
            self.modelMemPtr = None
            self.modelMemSize = 0
        if self.modelWeightPtr != None:
            acl.rt.free(self.modelWeightPtr)
            self.modelWeightPtr = None
            self.modelWeightSize = 0
        self.loadflag = False
        logging.info("unload model success, modelId is %u", self.modelId)






