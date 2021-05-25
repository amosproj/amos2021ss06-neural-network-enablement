import os
import unittest
# from flask import json
from app import app
import json
from io import BytesIO

# change into a test folder
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/webtest/"


class BasicTests(unittest.TestCase):
    """
    Unit-Test of Webservice
    """

    def setUp(self):
        """
        Set up web app for unit test, create temporary folder for operating on test
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
        tear down web app for unit test, remove temporary folder for operating on test
        pictures
        """
        os.rmdir(UPLOAD_FOLDER)

    def test_main_page(self):
        """
        Unit-Test on the availability of main page of web application
        """
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_upload_image(self):
        """
        Unit-Test on the
            upload images
            colorize images
            delete images
            check return urls of pictures
        """
        # call all(), get amount of urls
        rsp_all = self.client.get('/all/')
        urls_before = json.loads(rsp_all.data)
        len_before = len(urls_before)

        # check upload images
        test_img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     'test_img.png')
        with open(test_img_path, 'rb') as test_img:
            test_img_io = BytesIO(test_img.read())

        rsp_upload = self.client.post('/upload/',
                                      content_type='multipart/form-data',
                                      data={'file': (test_img_io, 'test_img.png')},
                                      follow_redirects=True)
        self.assertEqual(rsp_upload.status_code, 200)

        # check amount of urls added by 1 after uploading img
        rsp_all_2 = self.client.get('/all/')
        urls_after = json.loads(rsp_all_2.data)
        len_after = len(urls_after)
        self.assertEqual(len_before + 1, len_after)

        # check colorize process
        filename = urls_after[0].rsplit('/', 1)[1]
        rsp_color = self.client.post('/colorize/', json={'name': filename})
        self.assertEqual(rsp_color.status_code, 200)

        # check the colorized pic exists
        rsp_result = self.client.post('/result/', json={'name': filename})
        self.assertEqual(rsp_result.status_code, 200)

        urls_result = json.loads(rsp_result.data)
        self.assertIn('colorized', urls_result)
        self.assertIn('origin', urls_result)
        self.assertIsNotNone(urls_result['colorized'])
        self.assertIsNotNone(urls_result['origin'])

        # check delete images
        rsp_delete = self.client.post('/delete/', json={'name': filename})
        self.assertEqual(rsp_delete.status_code, 200)

        # check files&folders is not there anymore
        d_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.', 1)[0])
        self.assertEqual(os.path.exists(d_path), False)
