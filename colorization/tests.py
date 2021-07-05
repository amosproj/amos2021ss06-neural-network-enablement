import unittest
import os
import cv2
import numpy as np
import shutil
import colorization.videodata as videodata
from colorization.colorize_process import preprocess, inference, postprocess
from colorization.pipeline import colorize_image, colorize_video

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

        self.model_path = os.path.join(cwd, '../model/colorization.om')

        # path of the gray input image to process in test
        self.input_image_path = os.path.join(cwd, 'test_data/dog.jpg')

        # path of result of the inference to be used for testing postprocess
        self.inference_output_path = os.path.join(cwd, 'test_data/dog.npy')

        # output image will be written to this path on success
        self.output_image_path = os.path.join(cwd, 'test_data/dog_colorized.jpg')
        self.kModelWidth = np.uint32(224)
        self.kModelHeight = np.uint32(224)

    def tearDown(self):
        print('tear down called')
        if os.path.isfile(self.output_image_path):
            os.remove(self.output_image_path)

    def test_step_preprocess_image(self):
        """
        Unit-Test to test the preprocessing of an image
        """
        # creat a new ColorizeProcess object name proc
        self.assertTrue(os.path.isfile(self.input_image_path))

        # test: input a existing and right file, should return SUCCESS
        input_image = cv2.imread(self.input_image_path, cv2.IMREAD_COLOR)
        result = preprocess(input_image)
        self.assertEqual(result.shape, (224, 224))

    def test_step_colorize_image(self):
        """
        Unit-Test to test the colorizing of an image
        """
        # create a new ColorizeProcess object name proc

        self.assertTrue(os.path.isfile(self.input_image_path))

        # test: input a existing and right file, should return SUCCESS
        input_image = cv2.imread(self.input_image_path, cv2.IMREAD_COLOR)
        result = preprocess(input_image)
        self.assertEqual(result.shape, (224, 224))

        # test the colorizing
        model_output = inference(self.model_path, result)
        self.assertEqual(model_output.shape, (2, 56, 56))

    def test_step_postprocess_image(self):
        """
        Unit-Test to test the postprocessing of an image
        """

        # check that the inference output npy file is available
        self.assertTrue(os.path.isfile(self.inference_output_path))
        self.assertTrue(os.path.isfile(self.input_image_path))

        # test: input a existing and right file, should return SUCCESS
        inference_output = np.load(self.inference_output_path)
        result = postprocess(self.input_image_path, inference_output)

        input_image = cv2.imread(self.input_image_path, cv2.IMREAD_COLOR)
        self.assertEqual(result.shape, input_image.shape)


class SplitAndMergeTestsForVideo(unittest.TestCase):
    """
    This class contains tests for the split and merge tests of video
    """

    def setUp(self):
        # init path variables
        self.video_input_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/greyscaleVideo.mp4')
        self.video_input_path_with_audio = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/test_video_with_voice.mp4')
        self.audio_output_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/audio_from_video.ogg')
        self.audio_input_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/audio_for_video.ogg')
        self.video_with_audio_output_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/merged_video_with_audio.webm')

    def tearDown(self):
        # cleanup files, that were created in this class
        print('tear down called')
        if os.path.isfile(self.audio_output_path):
            os.remove(self.audio_output_path)
        if os.path.isfile(self.video_with_audio_output_path):
            os.remove(self.video_with_audio_output_path)

    def test_step_video2frames_frames2video(self):
        """
        Unit-Test to test the video2frames and frames2video function of a video
        """
        # Test1: for right video and path
        # current path
        cwd = os.path.abspath(os.path.dirname(__file__))
        # split_frames path
        image_output_folder_path = os.path.join(cwd, 'test_data/split_frames')
        # create split_frames path folder
        os.mkdir(image_output_folder_path)
        # split the video
        ret = videodata.video2frames(self.video_input_path, image_output_folder_path)
        self.assertEqual(ret, SUCCESS)

        # Test2: for wrong path (as a picture)
        video_input_path2 = os.path.join(cwd, 'test_data/dog.jpg')
        # split the video
        ret = videodata.video2frames(video_input_path2,
                                     image_output_folder_path)
        self.assertEqual(ret, FAILED)

        # Test3: test to merge the frames
        # output video path
        video_output_path = os.path.join(cwd, 'test_data/merged_video.webm')
        # create the output video folder
        os.mkdir(video_output_path)
        # merge the video
        ret = videodata.frames2video(image_output_folder_path,
                                     video_output_path)
        self.assertEqual(ret, SUCCESS)
        # destroy the frames folder and video folder after test
        shutil.rmtree(video_output_path)

    def test_step_split_audio_from_video(self):
        """
        Unit-Test to test the split_audio_from_video function
        """
        self.assertTrue(os.path.isfile(self.video_input_path_with_audio))
        ret = videodata.split_audio_from_video(
            self.video_input_path_with_audio, self.audio_output_path)
        self.assertEqual(ret, SUCCESS)
        self.assertTrue(os.path.isfile(self.audio_output_path))

    def test_step_merge_audio_and_video(self):
        """
        Unit-Test to test the merge_audio_and_video function
        """
        self.assertTrue(os.path.isfile(self.video_input_path_with_audio))
        self.assertTrue(os.path.isfile(self.audio_input_path))
        ret = videodata.merge_audio_and_video(
            self.video_input_path_with_audio, self.audio_input_path,
            self.video_with_audio_output_path)
        self.assertEqual(ret, SUCCESS)
        self.assertTrue(os.path.isfile(self.video_with_audio_output_path))


class FunctionalTest(unittest.TestCase):
    """
    This class contains tests for the complete pipeline.
    (i.e. the function pipeline.colorize_image)
    """

    def setUp(self):
        # init path variables
        self.input_image_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/lena.png')
        self.output_image_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/lena_colorized.png')
        self.fake_input_image_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), '../../Data/notexist.png')
        self.input_video_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/greyscaleVideo.mp4')
        self.output_video_path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'test_data/colorized_video.webm')

        self.input_video_path_with_audio = \
            os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'test_data/test_video_with_voice.mp4')
        self.output_video_path_with_audio = os.path.join(os.path.abspath(
            os.path.dirname(__file__)),
            'test_data/colorized_video_with_audio.webm')

    def tearDown(self):
        # cleanup files, that were created in the
        # test_complete_colorize_image test run
        print('tear down called')
        if os.path.isfile(self.output_image_path):
            os.remove(self.output_image_path)
        if os.path.isfile(self.output_video_path):
            os.remove(self.output_video_path)
        if os.path.isfile(self.output_video_path_with_audio):
            os.remove(self.output_video_path_with_audio)

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

    def test_colorize_twice(self):
        """
        Functional test to test the colorization of two images in single session
        """

        ret = colorize_image(self.input_image_path, self.output_image_path)
        self.assertEqual(ret, SUCCESS)

        os.remove(self.output_image_path)

        ret = colorize_image(self.input_image_path, self.output_image_path)
        self.assertEqual(ret, SUCCESS)

    def test_colorize_video(self):
        """
        Functional test to test the colorization of two images in single session
        """

        ret = colorize_video(self.input_video_path, self.output_video_path)
        self.assertEqual(ret, SUCCESS)
        self.assertTrue(os.path.isfile(self.output_video_path))

        ret = colorize_video(self.input_video_path_with_audio,
                             self.output_video_path_with_audio)
        self.assertEqual(ret, SUCCESS)
        self.assertTrue(os.path.isfile(self.output_video_path_with_audio))
