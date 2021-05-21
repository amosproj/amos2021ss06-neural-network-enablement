import unittest

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
        # TODO: test the preprocess function e.g. the output size etc.
        self.assertTrue(True)

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


class IntegrationTest(unittest.TestCase):
    """
    This class contains tests for the complete pipeline.
    (i.e. the function pipeline.colorize_image)
    """

    def test_complete_colorize_image(self):
        """
        Integration test to test the complete colorizing process
        """
        # TODO
        from pipeline import colorize_image
        path_input = "test_image.png"
        path_output = "colorized_image.png"
        ret = colorize_image(path_input, path_output)
        self.assertEqual(ret, SUCCESS)
        # TODO
        # check if the image and the path exist
        import os
        ret = os.path.exists(path_output)
        self.assertEqual(ret, SUCCESS)
        ret = os.path.isfile(path_output)
        self.assertEqual(ret, SUCCESS)
        # check if the image in output path is colorized
        import cv2
        img = cv2.imread(path_output)
        ret = len(img.shape)
        self.assertGreaterEqual(3, ret)
        ret = img.shape[2]
        self.assertNotEqual(ret, 1)
        (b, g, r) = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        ret = (b == g).all() and (b == r).all()
        self.assertFalse(ret)

