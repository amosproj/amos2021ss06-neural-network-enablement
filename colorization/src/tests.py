import unittest
import os
import cv2
import numpy
from colorize_process import ColorizeProcess
from pipeline import colorize_image

FAILED = 1
SUCCESS = 0

# import colorize_process
# import acl

# ^
# |
# |
# these imports would also work here (The test shall be run on an Atlas Board)


class PipelineTests(unittest.TestCase):
    """
    This class contains tests for each part of the pipeline
    See https://docs.python.org/3/library/unittest.html for more information.
    """

    def setUp(self):
        self.input_image_path = 'input_image.jpg'
        self.output_image_path = 'output_image.jpg'
        self.model_output = ''

    def test_step_preprocess_image(self):
        """
        Unit-Test to test the preprocessing of an image
        """
        # creat a new ColorizeProcess object namme proc
        kModelWidth = numpy.uint32(224)
        kModelHeight = numpy.uint32(224)
        # the KMODELPATH is not in main
        KMODELPATH = img_path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                              '../../model/colorization.om')
        proc = ColorizeProcess(KMODELPATH, kModelWidth, kModelHeight)
        ret = proc.Init()
        self.assertEqual(ret, SUCCESS)
        # test1: input a not existing file, should return FAILED
        img_path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../Data/notexist.png')
        result = proc.Preprocess(img_path1)
        self.assertEqual(result, FAILED)
        # test2: input a existing and right file, should return SUCCESS
        img_path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../Data/dog.png')
        result2 = proc.Preprocess(img_path2)
        self.assertEqual(result2, SUCCESS)

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

    def test_complete_colorize_image(self):
        """
        Functional test to test the complete colorizing process
        """
        path_input = "test_image.png"
        path_output = "colorized_image.png"
        ret = colorize_image(path_input, path_output)
        self.assertEqual(ret, SUCCESS)
        # check if the image and the path exist
        ret = os.path.exists(path_output)
        self.assertTrue(ret)
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
