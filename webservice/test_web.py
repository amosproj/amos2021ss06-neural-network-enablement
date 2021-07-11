import os
import shutil
import unittest
from app import app
import json
from io import BytesIO

# change into a test folder
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/webtest/"


class BasicTests(unittest.TestCase):
    """
    Unit and Integration Test of Webservice
    """

    def setUp(self):
        """
        Set up web app for the test, create temporary folder for operating on test
        pictures
        """
        app.config['TESTING'] = True
        # change into a test folder
        os.mkdir(UPLOAD_FOLDER)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.secret_key = b'wu8QvPtCDIM1/9ceoUS'
        self.app = app
        self.client = app.test_client()

    # executed after each test
    def tearDown(self):
        """
        tear down web app for the test, remove temporary folder for operating on test
        pictures
        """
        shutil.rmtree(UPLOAD_FOLDER)

    def test_main_page(self):
        """
        Test the availability of main page of web application
        """
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_integration_image(self):
        """
        Integration Test on the
            upload images
            colorize images
            delete images
            check return urls of images
        """
        # call all(), get amount of urls
        rsp_all = self.client.get('/media/')
        urls_before = json.loads(rsp_all.data)
        len_before = len(urls_before)

        # check upload images
        test_img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     'test_img.png')
        with open(test_img_path, 'rb') as test_img:
            test_img_io = BytesIO(test_img.read())

        rsp_upload = self.client.post('/media/',
                                      content_type='multipart/form-data',
                                      data={'file': (test_img_io, 'test_img.png')},
                                      follow_redirects=True)
        self.assertEqual(rsp_upload.status_code, 200)
        self.assertIn(b'Upload successfully', rsp_upload.data)

        # check amount of urls added by 1 after uploading img
        rsp_all_2 = self.client.get('/media/')
        urls_after = json.loads(rsp_all_2.data)
        len_after = len(urls_after)
        self.assertEqual(len_before + 1, len_after)

        # check colorize process, use folder name
        foldername = urls_after[0]['id']
        rsp_color = self.client.post(f'/media/{foldername}/colorize')
        self.assertEqual(rsp_color.status_code, 200)

        # check the colorized pic exists
        # change parameter, not json
        rsp_result = self.client.get(f'/media/{foldername}')
        self.assertEqual(rsp_result.status_code, 200)

        urls_result = json.loads(rsp_result.data)
        self.assertIn('colorized', urls_result)
        self.assertIn('origin', urls_result)
        self.assertIsNotNone(urls_result['colorized'])
        self.assertIsNotNone(urls_result['origin'])

        # check delete images
        rsp_delete = self.client.delete(f'/media/{foldername}')
        self.assertEqual(rsp_delete.status_code, 200)

        # check files&folders is not there anymore
        d_path = os.path.join(app.config['UPLOAD_FOLDER'], foldername)
        self.assertEqual(os.path.exists(d_path), False)

    # TODO : def test_integration_video(self):
    def test_integration_video(self):
        """
        Integration Test on the
            upload videos
            colorize videos
            delete videos
            check return urls of videos
        """
        # call all(), get amount of urls
        rsp_all = self.client.get('/media/')
        urls_before = json.loads(rsp_all.data)
        len_before = len(urls_before)

        # check upload videos
        test_video_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                       'test_video.mp4')
        with open(test_video_path, 'rb') as test_video:
            test_video_io = BytesIO(test_video.read())

        rsp_upload_v = self.client.post('/media/',
                                        content_type='multipart/form-data',
                                        data={'file': (test_video_io, 'test_video.mp4')},
                                        follow_redirects=True)
        self.assertEqual(rsp_upload_v.status_code, 200)
        self.assertIn(b'Upload successfully', rsp_upload_v.data)

        # check amount of urls added by 1 after uploading img
        rsp_all_2 = self.client.get('/media/')
        urls_after = json.loads(rsp_all_2.data)
        len_after = len(urls_after)
        self.assertEqual(len_before + 1, len_after)
        self.assertIn('_thumbnail', urls_after)

        # # check colorize process, use folder name
        # foldername = urls_after[0]['id']
        # rsp_color = self.client.post(f'/media/{foldername}/colorize')
        # self.assertEqual(rsp_color.status_code, 200)
        #
        # # check the colorized pic exists
        # # change parameter, not json
        # rsp_result = self.client.get(f'/media/{foldername}')
        # self.assertEqual(rsp_result.status_code, 200)
        #
        # urls_result = json.loads(rsp_result.data)
        # self.assertIn('colorized', urls_result)
        # self.assertIn('origin', urls_result)
        # self.assertIn('thumbnail', urls_result)
        # self.assertIsNotNone(urls_result['colorized'])
        # self.assertIsNotNone(urls_result['origin'])
        # self.assertIsNotNone(urls_result['thumbnail'])
        #
        # # check delete video
        # rsp_delete = self.client.delete(f'/media/{foldername}')
        # self.assertEqual(rsp_delete.status_code, 200)
        #
        # # check files&folders is not there anymore
        # d_path = os.path.join(app.config['UPLOAD_FOLDER'], foldername)
        # self.assertEqual(os.path.exists(d_path), False)

    def test_delete(self):
        """
        Unit Test of the fail situation of deleting pictures
        """
        # delete a picture which not on the server
        response1 = self.client.delete('/media/2020_nonfile.png')
        self.assertEqual(response1.status_code, 400)
        self.assertIn(b'Pictures not found!', response1.data)

        # no filename as the input parameter in POST request
        response2 = self.client.delete('/media/')
        self.assertEqual(response2.status_code, 405)
        self.assertIn(b'Pictures not found!', response1.data)

    def test_colorize(self):
        """
        Unit Test of the fail situation of colorizing pictures
        """
        # no filename as the input parameter in POST request
        response1 = self.client.post('/media/colorize')
        self.assertEqual(response1.status_code, 405)

    def test_upload(self):
        """
        Unit Test of the fail situation of uploading pictures or videos
        """
        # no file in POST request
        response1 = self.client.post('/media/')
        self.assertEqual(response1.status_code, 400)
        self.assertIn(b'No upload file', response1.data)

        # the format of files are not supported
        test_img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     'test_img.png')
        with open(test_img_path, 'rb') as test_img:
            test_img_io = BytesIO(test_img.read())

        response2 = self.client.post('/media/',
                                     content_type='multipart/form-data',
                                     data={'file': (test_img_io, 'test_img.bmp')},
                                     follow_redirects=True)
        self.assertEqual(response2.status_code, 400)
        self.assertIn(b'The file format is not supported', response2.data)
