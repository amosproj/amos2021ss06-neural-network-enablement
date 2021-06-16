import unittest
import os
import cv2
import numpy
import shutil
import videodata
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
        self.input_image_path = os.path.join(cwd, 'test_data/input_image_2.jpg')

        # output of the inference will be written to this path on success
        self.temp_inference_output_path = os.path.join(
            cwd, 'test_data/inference_output_1.npy')

        # path of result of the inference to be used for testing postprocess
        self.inference_output_path = os.path.join(cwd, 'test_data/inference_output_2.npy')

        # output image will be written to this path on success
        self.output_image_path = os.path.join(cwd, 'test_data/output_image_2.jpg')
        self.kModelWidth = numpy.uint32(224)
        self.kModelHeight = numpy.uint32(224)

    def tearDown(self):
        print('tear down called')
        if os.path.isfile(self.output_image_path):
            os.remove(self.output_image_path)
        if os.path.isfile(self.temp_inference_output_path):
            os.remove(self.temp_inference_output_path)

    def test_step_preprocess_image(self):
        """
        Unit-Test to test the preprocessing of an image
        """
        # creat a new ColorizeProcess object name proc

        proc = ColorizeProcess(self.model_path, self.kModelWidth,
                               self.kModelHeight)
        ret = proc.Init()
        self.assertEqual(ret, SUCCESS)

        self.assertTrue(os.path.isfile(self.input_image_path))

        # test: input a existing and right file, should return SUCCESS
        result = proc.Preprocess(self.input_image_path)

        self.assertEqual(result, SUCCESS)

    def test_step_colorize_image(self):
        """
        Unit-Test to test the colorizing of an image
        """
        # creat a new ColorizeProcess object name proc

        proc = ColorizeProcess(self.model_path, self.kModelWidth,
                               self.kModelHeight)
        ret = proc.Init()
        self.assertEqual(ret, SUCCESS)

        self.assertTrue(os.path.isfile(self.input_image_path))

        # test: input a existing and right file, should return SUCCESS
        result = proc.Preprocess(self.input_image_path)

        self.assertEqual(result, SUCCESS)

        # test the colorizing
        ret = proc.inference(self.temp_inference_output_path)
        self.assertEqual(ret, SUCCESS)
        # check that the inference output npy file is saved
        self.assertTrue(os.path.isfile(self.temp_inference_output_path))

    def test_step_postprocess_image(self):
        """
        Unit-Test to test the postprocessing of an image
        """

        # check that the inference output npy file is available
        self.assertTrue(os.path.isfile(self.inference_output_path))

        # TODO test the postprocessing

        proc = ColorizeProcess(self.model_path, self.kModelWidth,
                               self.kModelHeight)
        ret = proc.Init()
        self.assertEqual(ret, SUCCESS)

        self.assertTrue(os.path.isfile(self.input_image_path))
        self.assertTrue(os.path.isfile(self.inference_output_path))
        # test: input a existing and right file, should return SUCCESS
        result = proc.postprocess(self.input_image_path,
                                  self.inference_output_path,
                                  self.output_image_path)
        self.assertEqual(result, SUCCESS)

class PipelineTestsForVideo(unittest.TestCase):
    """
    This class contains tests for the pipeline of video
    """
    def test_step_video2frames_video(self):
        """
        Unit-Test to test the video2frames function of a video
        """




class SplitAndMergeTestsForVideo(unittest.TestCase):
    """
    This class contains tests for the split and merge tests of video
    """
    def test_step_video2frames(self):
        """
        Unit-Test to test the video2frames function of a video
        """
        # Test1: for right video and path
        # current path
        cwd = os.path.abspath(os.path.dirname(__file__))
        # video path
        video_input_path = os.path.join(cwd, 'test_data/greyscaleVideo.mp4')
        # split_frames path
        image_output_folder_path = os.path.join(cwd, 'test_data/split_frames')
        # creat split_frames path folder
        os.mkdir(image_output_folder_path)
        # split the video
        ret = videodata.video2frames(video_input_path, image_output_folder_path)
        self.assertEqual(ret, SUCCESS)

        # Test2: for wrong path (as a picture)
        video_input_path2 = os.path.join(cwd, 'test_data/input_image_2.jpg')
        # split the video
        ret2 = videodata.video2frames(video_input_path2,
                                      image_output_folder_path)
        self.assertEqual(ret2, FAILED)

    def test_step_frames2video(self):
        """
        Unit-Test to test the frames2video function of a video
        """
        # current path
        cwd = os.path.abspath(os.path.dirname(__file__))
        # input frames path
        image_output_folder_path = os.path.join(cwd, 'test_data/split_frames')
        # output video path
        video_output_path = os.path.join(cwd, 'test_data/merged_video')
        # creat the output video folder
        os.mkdir(video_output_path)
        # merge the video
        ret = videodata.frames2video(image_output_folder_path,
                                     video_output_path)
        # prblems
        self.assertEqual(ret, SUCCESS)
        # destroy the frames folder and video folder after test
        shutil.rmtree(image_output_folder_path)
        shutil.rmtree(video_output_path)


class FunctionalTest(unittest.TestCase):
    """
    This class contains tests for the complete pipeline.
    (i.e. the function pipeline.colorize_image)
    """

    def setUp(self):
        # init path variables
        self.input_image_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/input_image_1.png')
        self.output_image_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/output_image_1.png')
        self.fake_input_image_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), '../../Data/notexist.png')

    def tearDown(self):
        # cleanup files, that were created in the
        # test_complete_colorize_image test run
        print('tear down called')
        if os.path.isfile(self.output_image_path):
            os.remove(self.output_image_path)

    def test_complete_colorize_image(self):
        """
        Functional test to test the complete colorizing process
        """
        ret = colorize_image(self.input_image_path, self.output_image_path)
        self.assertEqual(ret, SUCCESS)
        # if the input path does not exist, expect FAILED:
        ret = colorize_image(self.fake_input_image_path, self.output_image_path)
        self.assertEqual(ret, FAILED)
        # check if the colorized image and the path exist
        ret = os.path.isfile(self.output_image_path)
        self.assertTrue(ret)
        # check if the image in output path is colorized
        img = cv2.imread(self.output_image_path)
        ret = len(img.shape)
        self.assertGreaterEqual(3, ret)
        ret = img.shape[2]
        self.assertNotEqual(ret, 1)
        (b, g, r) = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        ret = (b == g).all() and (b == r).all()
        self.assertFalse(ret)
