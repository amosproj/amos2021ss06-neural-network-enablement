import os
import unittest
from flask import json
from app import app

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/uploaded/"


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.secret_key = b'wu8QvPtCDIM1/9ceoUS'
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # TODO: upload(), upload image
    def test_upload_image(self):
        # check return code and msg
        # check the uploaded file exists


    # TODO: all(), get list of urls of gray pictures
    def test_all_urls(self):
        # check return
        # anything else? colored pictures excluded? amount of urls == amount of folders?
        pass

    # TODO: result()
    def test_result(self):
        # check return data and code
        # and ?
        pass

    # TODO: delete()
    def test_delete(self):
        # check return code and msg
        # check files&folders is not there anymore
        pass

    # TODO: colorize()
    def test_colorize(self):
        # check return code and msg
        # check input and output path are both file
        pass

if __name__ == "__main__":
    unittest.main()
