import unittest


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
        self.assertTrue(False)


    def test_step_colorize_image(self):
        """
        Unit-Test to test the colorizing of an image
        """
        # TODO test the colorizing
        self.assertTrue(False)


    def test_step_postprocess_image(self):
        """
        Unit-Test to test the postprocessing of an image
        """
        # TODO test the postprocessing
        self.assertTrue(False)


class IntegrationTest(unittest.TestCase):
    """
    This class contains tests for the complete pipeline.
    (i.e. the function pipeline.colorize_image)
    """

    def test_complete_colorize_image(self):
        """
        Integration test to test the complete colorizing process
        """
        # TODO test the complete pipeline. e.g. colorize an example image
        self.assertTrue(False)

