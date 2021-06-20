import os
import sys
sys.path.append('../')
from acl_model import Model


class ModelProcessor:
    
    def __init__(self, acl_resource, params):
        self._acl_resource = acl_resource
        self.params = params
        self._model_width = params['width']
        self._model_height = params['height']

        assert 'model_dir' in params and params['model_dir'] is not None, 'Review your param: model_dir'
        assert os.path.exists(params['model_dir']), "Model directory doesn't exist {}".format(params['model_dir'])
            
        # load model from path, and get model ready for inference
        self.model = Model(acl_resource, params['model_dir'])

    def predict(self, model_input):
        # execute model inference
        result = self.model.execute([model_input])[0]
        canvas = result[0]
        print(result[0].shape)
        print(result.dtype)
        return canvas


