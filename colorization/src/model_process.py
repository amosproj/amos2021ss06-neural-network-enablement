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
        pass

    def DestroyDesc(self):
        pass

    def CreateInput(self,inputDataBuffer,bufferSize):
        pass

    def DestroyInput(self):
        pass

    def CreateOutput(self):
        pass


    def DestroyOutput(self):
        pass

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






