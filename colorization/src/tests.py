import unittest
from pipeline import colorize_image
from colorize_process import Preprocess
import os
import cv2

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

    def test_step_preprocess_image(self):
        """
        Unit-Test to test the preprocessing of an image
        """
        # test1: input a not existing file, should return FAILED
        imageFile = "/home/ke/Pictures/notexisting.jpg"
        result = Preprocess(self, imageFile)
        self.assertEqual(result, FAILED)
        # test2: input a existing and right file, should return SUCCESS
        imageFile2 = "/home/ke/amos-ss2021-neural-network-enablement/Data/dog" \
                     ".png "
        result2 = Preprocess(self, imageFile2)
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
        self.assertTrue(True)


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
