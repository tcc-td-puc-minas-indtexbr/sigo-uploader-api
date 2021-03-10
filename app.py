import base64
import os

import yaml

from chalicelib.boot import register_vendor
from chalicelib.services.v1.sigo_uploader_service import SigoUploaderService, MaxSizeException

register_vendor()

# execute before other codes of app
from chalicelib.helper import open_vendor_file
from chalicelib.http_helper import CUSTOM_DEFAULT_HEADERS
from chalicelib.logging import get_logger, get_log_level
from chalicelib.openapi import generate_openapi_yml, spec

from chalice import Chalice
from chalicelib import APP_NAME, helper, http_helper, APP_VERSION

# debug
debug = helper.debug_mode()
# logger
logger = get_logger()
# chalice app
app = Chalice(app_name=APP_NAME, debug=debug)
# override the log configs
if not debug:
    # override to the level desired
    logger.level = get_log_level()
# override the log instance
app.log = logger


@app.route('/', cors=True)
def index():
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/ping', cors=True)
def ping():
    """
    get:
        summary: Ping method
        responses:
            200:
                description: Success response
                content:
                    application/json:
                        schema: PingSchema
    """
    body = {"message": "PONG"}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/alive', cors=True)
def alive():
    """
        get:
            summary: Service Health Method
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: AliveSchema
        """
    body = {"app": "I'm alive!"}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/favicon-32x32.png', cors=True)
def favicon():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "image/png"
    data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAkFBMVEUAAAAQM0QWNUYWNkYXNkYALjoWNUYYOEUXN0YaPEUPMUAUM0QVNUYWNkYWNUYWNUUWNUYVNEYWNkYWNUYWM0eF6i0XNkchR0OB5SwzZj9wyTEvXkA3az5apTZ+4C5DgDt31C9frjU5bz5uxTI/eDxzzjAmT0IsWUEeQkVltzR62S6D6CxIhzpKijpJiDpOkDl4b43lAAAAFXRSTlMAFc304QeZ/vj+ECB3xKlGilPXvS2Ka/h0AAABfklEQVR42oVT2XaCMBAdJRAi7pYJa2QHxbb//3ctSSAUPfa+THLmzj4DBvZpvyauS9b7kw3PWDkWsrD6fFQhQ9dZLfVbC5M88CWCPERr+8fLZodJ5M8QJbjbGL1H2M1fIGfEm+wJN+bGCSc6EXtNS/8FSrq2VX6YDv++XLpJ8SgDWMnwqznGo6alcTbIxB2CHKn8VFikk2mMV2lEnV+CJd9+jJlxXmMr5dW14YCqwgbFpO8FNvJxwwM4TPWPo5QalEsRMAcusXpi58/QUEWPL0AK1ThM5oQCUyXPoPINkdd922VBw4XgTV9zDGWWFrgjIQs4vwvOg6xr+6gbCTqE+DYhlMGX0CF2OknK5gQ2JrkDh/W6TOEbYDeVecKbJtyNXiCfGmW7V93J2hDus1bDfhxWbIZVYDXITA7Lo6E0Ktgg9eB4KWuR44aj7ppBVPazhQH7/M/KgWe9X1qAg8XypT6nxIMJH+T94QCsLvj29IYwZxyO9/F8vCbO9tX5/wDGjEZ7vrgFZwAAAABJRU5ErkJggg==')
    return http_helper.create_response(body=data, status_code=200, headers=headers)


@app.route('/docs', cors=True)
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/html"
    html_file = open_vendor_file('./public/swagger/index.html', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


@app.route('/openapi.json', cors=True)
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/json"
    html_file = open_vendor_file('./public/swagger/openapi.json', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


@app.route('/openapi.yml', cors=True)
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/yaml"
    html_file = open_vendor_file('./public/swagger/openapi.yml', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


# 'application/octet-stream'
# 'text/plain',
@app.route('/v1/upload/{file_type}/{file_name}', methods=['POST'], content_types=[
    'application/pdf',
    'multipart/form-data'
], cors=True)
def upload_to_s3(file_type, file_name):
    """
        post:
            summary: Upload file to S3 Sigo Bucket
            parameters:
            - in: path
              name: file_type
              description: "File type (standard, consulting)"
              example: standard
              required: true
              schema:
                type: string
                enum: [standard, consulting]
            - in: path
              name: file_name
              description: "File name"
              example: "ISO_9001_2010.pdf"
              required: true
              schema:
                type: string
            requestBody:
              content:
                multipart/form-data:
                  schema:
                    type: object
                    properties:
                        # 'file' will be the field name in this multipart request
                        file:
                            type: string
                            format: binary
                application/pdf:
                  schema:
                    type: string
                    format: binary
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: UploadResponseSchema
                500:
                    description: Success response
                    content:
                        application/json:
                            schema: UploadErrorResponseSchema
    """
    # file name max size
    MAX_SIZE_FILE_NAME = 50
    # files types
    FILE_TYPES = ['standard']
    # 20 MB
    MAX_SIZE = 20480000
    # 200 KB
    # MAX_SIZE = 20480

    try:
        service = SigoUploaderService(logger=logger)
        result = service.execute(file_type, file_name, app)

        message = 'Upload successful'
        status_code = 200

        if not result:
            message = 'Upload failed'
            status_code = 500

    except Exception as err:
        logger.error(err)
        message = 'Upload failed'
        if isinstance(err, MaxSizeException):
            message = err.message

        status_code = 500

    return http_helper.create_response(body={"message": message}, status_code=status_code)


spec.path(view=ping, path="/alive", operations=yaml.safe_load(alive.__doc__))
spec.path(view=ping, path="/ping", operations=yaml.safe_load(ping.__doc__))
spec.path(view=upload_to_s3, path="/v1/upload/{file_type}/{file_name}", operations=yaml.safe_load(upload_to_s3.__doc__))

helper.print_routes(app, logger)
logger.info('Running at {}'.format(os.environ['APP_ENV']))

# generate de openapi.yml
generate_openapi_yml(spec, logger)

