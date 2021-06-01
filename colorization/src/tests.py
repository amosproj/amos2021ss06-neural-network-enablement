import unittest

import os
import cv2
import numpy
from colorize_process import ColorizeProcess
from pipeline import colorize_image

FAILED = 1
SUCCESS = 0


# The test shall be run on an Atlas Board.


class PipelineTests(unittest.TestCase):
    """
    This class contains tests for each part of the pipeline
    See https://docs.python.org/3/library/unittest.html for more information.
    """

    def setUp(self):
        cwd = os.path.abspath(os.path.dirname(__file__))

        self.model_path = os.path.join(cwd, '../../model/colorization.om')

        # path of the gray input image to process in test
        self.input_image_path = os.path.join(cwd, 'test_data/input_image_2.png')

        # path of result of the inference to be used for testing postprocess
        self.inference_output_path = os.path.join(cwd, 'test_data/inference_output_2.npy')

        # output image will be written to this path on success
        self.output_image_path = os.path.join(cwd, 'test_data/output_image_2.png')

    def tearDown(self):
        print('tear down called')
        if os.path.isfile(self.output_image_path):
            os.remove(self.output_image_path)

    def test_step_preprocess_image(self):
        """
        Unit-Test to test the preprocessing of an image
        """
        # creat a new ColorizeProcess object namme proc
        kModelWidth = numpy.uint32(224)
        kModelHeight = numpy.uint32(224)

        proc = ColorizeProcess(self.model_path, kModelWidth, kModelHeight)
        ret = proc.Init()
        self.assertEqual(ret, SUCCESS)

        # test: input a existing and right file, should return SUCCESS
        result = proc.Preprocess(self.input_image_path)

        self.assertEqual(result, SUCCESS)
        proc.DestroyResource()

    def test_step_colorize_image(self):
        """
        Unit-Test to test the colorizing of an image
        """
        # TODO test the colorizing
        self.assertTrue(True)

    def test_step_postprocess_image(self):
        """
        Unit-Test to test the postprocessing of an image
        """

        # check that the inference output npy file is available
        self.assertTrue(os.path.isfile(self.inference_output))

        # TODO test the postprocessing
        ret = ColorizeProcess.postprocess(self.input_image_path,
                                          self.output_image_path, self.model_output)
        if self.model_output is None:
            self.assertEqual(ret, FAILED)
        if self.model_output is not None:
            self.assertEqual(ret, SUCCESS)


class FunctionalTest(unittest.TestCase):
    """
    This class contains tests for the complete pipeline.
    (i.e. the function pipeline.colorize_image)
    """

    def setUp(self):
        # TODO: inits path variables
        pass

    def tearDown(self):
        # TODO: cleanup files, that were created in the
        # test_complete_colorize_image test run
        pass

    def test_complete_colorize_image(self):
        """
        Functional test to test the complete colorizing process
        """
        path_input = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  'test_data/input_image_1.png')
        path_output = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   'test_data/output_image_1.png')
        ret = colorize_image(path_input, path_output)
        self.assertEqual(ret, SUCCESS)
        # if the input path does not exist, expect FAILED:
        path_input = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  '../../Data/notexist.png')
        ret = colorize_image(path_input, path_output)
        self.assertEqual(ret, FAILED)
        # check if the colorized image and the path exist
        ret = os.path.isfile(path_output)
        self.assertTrue(ret)
        # check if the image in output path is colorized
        img = cv2.imread(path_output)
        ret = len(img.shape)
        self.assertGreaterEqual(3, ret)
        ret = img.shape[2]
        self.assertNotEqual(ret, 1)
        (b, g, r) = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        ret = (b == g).all() and (b == r).all()
        self.assertFalse(ret)
