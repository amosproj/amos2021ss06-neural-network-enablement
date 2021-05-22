import os
import unittest
#from flask import json
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
        # check the test data would not influence the Webservice
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # TODO: upload() + all(), upload image
    def test_upload_image(self):
        # check return code and msg, all conditions
        # check return all urls of pictures
        pass

    # TODO: result() + colorize()
    def test_colorized_result(self):
        # check return data and code
        # check colorize process return and code
        # and result['origin'],result['colorized']
        pass

    # TODO: delete() + all(), similar to test_upload_image()
    def test_delete(self):
        # check return code and msg
        # check files&folders is not there anymore
        pass

