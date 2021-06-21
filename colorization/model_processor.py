import os
import sys
sys.path.append('../')
from acl_model import Model # noqa


class ModelProcessor:

    def __init__(self, acl_resource, params):
        self._acl_resource = acl_resource
        self.params = params
        self._model_width = params['width']
        self._model_height = params['height']

        if 'model_dir' not in params or params['model_dir'] is None:
            raise AssertionError('Param: "model_dir" not provided')

        if not os.path.exists(params['model_dir']):
            raise AssertionError(f"Model not found at {params['model_dir']}")

        # load model from path, and get model ready for inference
        self.model = Model(acl_resource, params['model_dir'])

    def predict(self, model_input):
        # execute model inference
        result = self.model.execute([model_input])[0]
        canvas = result[0]
        print(result[0].shape)
        print(result.dtype)
        return canvas
