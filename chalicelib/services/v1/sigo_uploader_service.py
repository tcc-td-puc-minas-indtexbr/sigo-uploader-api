import cgi
import os
from io import BytesIO
from os import path

from chalicelib.aws_helper import get_s3_client
from chalicelib.config import get_config
from chalicelib.logging import get_logger


class MaxSizeException(Exception):
    def __init__(self, message, errors=None):
        self.message = message
        super(Exception, self).__init__(message, errors)


class SigoUploaderService:
    DEBUG = False
    # file name max size
    MAX_SIZE_FILE_NAME = 50
    # files types
    FILE_TYPES = ['standard']
    # 20 MB
    MAX_SIZE = 20480000

    # 200 KB
    # MAX_SIZE = 20480

    def __init__(self, logger=None, config=None, s3_client=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # database connection
        self.s3_client = s3_client if s3_client is not None else get_s3_client()
        # error message
        self.error_message = ''

    def execute(self, file_type, file_name, app):
        self.error_message = ''

        try:
            if file_type not in self.FILE_TYPES:
                file_type = self.FILE_TYPES[0]

            profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
            self.logger.info('profile: {}'.format(profile))

            bucket = os.environ['AWS_BUCKET_NAME'] if 'AWS_BUCKET_NAME' in os.environ else None

            content_type = app.current_request.headers.get('content-type')
            self.logger.info('Content-type: %s' % content_type)

            body = app.current_request.raw_body
            # print(app.current_request.raw_body)

            if 'multipart/form-data' in str(content_type):
                property_dict = cgi.parse_header(content_type)[1]
                # convert to bytes
                property_dict['boundary'] = property_dict['boundary'].encode()
                form_data = cgi.parse_multipart(BytesIO(body), property_dict)
                if 'file' in form_data and len(form_data['file']) > 0:
                    body = form_data['file'][0]
                else:
                    body = ''

            # validate file size
            if len(body) > self.MAX_SIZE:
                raise MaxSizeException('File size great than limit %s' % (self.MAX_SIZE,))

            temp_file = path.join('/tmp', file_name)
            with open(temp_file, 'wb') as f:
                f.write(body)

            if bucket == '':
                raise Exception('Bucket name empty')

            file_name = str(file_name).replace(' ', '_').replace('%20', '_')
            file_data = file_name.split('.')
            ext = file_data[len(file_data) - 1]
            if len(file_name) > self.MAX_SIZE_FILE_NAME:
                file_name = file_name[:self.MAX_SIZE_FILE_NAME] + '.' + ext
            bucket_file_name = path.join(file_type, file_name)

            self.logger.info('Uploading to S3 %s %s %s' % (temp_file, bucket, bucket_file_name))
            self.s3_client.upload_file(temp_file, bucket, bucket_file_name)

            result = True
        except Exception as err:
            self.logger.error(err)
            self.error_message = 'Upload error'
            if isinstance(err, MaxSizeException):
                self.error_message = err.message

            result = False

        return result
