import logging


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
            return


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
        pass

    def Unload(self):
        pass



