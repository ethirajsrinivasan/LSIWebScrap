from web_scrapper_controller import *
import unittest 
import json
class ScrapTests(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/fetch_from_google', query_string=dict(query='google')) 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 

    def test_home_data_count(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/fetch_from_google', query_string=dict(query='google')) 
        str_response = result.data.decode('utf-8')
        obj = json.loads(str_response)
        response_count = len(obj)
        # assert the response data
        self.assertEqual(response_count, 5)

    def test_home_data_count_for_rare_case(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/fetch_from_google', query_string=dict(query='zxczxccvbmvcsadfasdasdasd')) 
        str_response = result.data.decode('utf-8')
        obj = json.loads(str_response)
        response_count = len(obj)
        # assert the response data
        self.assertEqual(response_count, 1)

    def test_home_data_count_for_null_case(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/fetch_from_google', query_string=dict(query='')) 
        str_response = result.data.decode('utf-8')
        obj = json.loads(str_response)
        response_count = len(obj)
        # assert the response data
        self.assertEqual(response_count, 1)

    def test_home_data_count_for_blank_case(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/fetch_from_google', query_string=dict(query='   ')) 
        str_response = result.data.decode('utf-8')
        obj = json.loads(str_response)
        response_count = len(obj)
        # assert the response data
        self.assertEqual(response_count, 1)

    def test_home_data_class(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/fetch_from_google', query_string=dict(query='   ')) 
        str_response = result.data.decode('utf-8')
        obj = json.loads(str_response)
        response_class = type(obj)
        # assert the response data
        self.assertEqual(response_class.__name__, "list")

    def test_home_data_for_unicode(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/fetch_from_google', query_string=dict(query='global blue')) 
        str_response = result.data.decode('utf-8')
        obj = json.loads(str_response)
        response_class = type(obj)
        # assert the response data
        self.assertEqual(response_class.__name__, "list")