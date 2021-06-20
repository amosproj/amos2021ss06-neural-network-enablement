import os
import cv2
import numpy as np
import argparse
import sys

sys.path.append('../')

from acl_model import Model

heatmap_width = 92
heatmap_height = 92


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

    def predict(self, img_original):
        
        #preprocess image to get 'model_input'
        model_input = self.preprocess(img_original)

        # execute model inference
        result = self.model.execute([model_input])[0]
#        np.save('test.npy', result)
        
        canvas = result[0]
        print(result[0].shape)

        print(result.dtype)

        # postprocessing: use the heatmaps (the second output of model) to get the joins and limbs for human body
        # Note: the model has multiple outputs, here we used a simplified method, which only uses heatmap for body joints
        #       and the heatmap has shape of [1,14], each value correspond to the position of one of the 14 joints. 
        #       The value is the index in the 92*92 heatmap (flatten to one dimension)
        # calculate the scale of original image over heatmap, Note: image_original.shape[0] is height

        return canvas

    def preprocess(self,img_original):
        '''
        preprocessing: resize image to model required size, and normalize value between [0,1]
        '''

        mat = img_original

        if np.any(mat) is None:  # if matrix is empty, every term is none
            return FAILED

        mat = mat.astype(np.float32)

        reiszeMat = cv2.resize(mat, (self._model_width, self._model_height))

        # deal image
        reiszeMat = 1.0 * reiszeMat / 255
        reiszeMat = cv2.cvtColor(reiszeMat, cv2.COLOR_BGR2Lab)

        # pull out L channel and subtract 50 for mean-centering
        # channel[0] = L, [1] = A, [2] = B
        channels = cv2.split(reiszeMat)
        
        print(f'{len(channels)} channels')
        return channels[0] - 50


