import json
import unittest

from tests import ROOT_DIR
from tests.unit.mocks.aws_lambda_mock import FakeLambdaContext
from tests.unit.testutils import BaseUnitTestCase, get_function_name
import app
from chalice import app as chalice_app


def create_event(content_type):
    body = ''
    event = {
        'multiValueQueryStringParameters': '',
        'headers': {'Content-Type': content_type},
        'pathParameters': {},
        'requestContext': {
            'httpMethod': 'GET',
            'resourcePath': '/',
        },
        'body': body,
        'stageVariables': {},
        'isBase64Encoded': False,
    }
    return event

def create_request_with_content_type(content_type):
    event = create_event(content_type)
    return chalice_app.Request(event, FakeLambdaContext())


class AppTestCase(BaseUnitTestCase):

    def test_ping(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        event = create_event('application/json')
        # override the mock
        event['requestContext'] = {
            'httpMethod': 'GET',
            'resourcePath':'/ping'
        }
        response = app.app(event, FakeLambdaContext)
        self.assertEqual(json.loads(response['body'])['message'], "PONG")

    def test_upload_to_s3(self):

        self.logger.info('Running test: %s', get_function_name(__name__))
        self.skipTest('Implementar mocks')

        event = create_event('application/pdf')
        file_path = ROOT_DIR + 'tests/datasource/upload/sample.pdf'
        event['body'] = open(file_path, 'rb').read()
        # override the mock
        event['requestContext'] = {
            'httpMethod': 'POST',
            'resourcePath':'/v1/upload/{file_type}/{file_name}',
        }
        event['pathParameters'] = {
            'file_type': 'standard',
            'file_name': 'teste.pdf'
        }
        response = app.app(event, FakeLambdaContext)

        self.assertEqual(json.loads(response['body'])['message'], "Upload successful")


if __name__ == '__main__':
    unittest.main()
