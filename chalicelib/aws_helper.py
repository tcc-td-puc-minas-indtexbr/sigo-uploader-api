import os

import boto3

from chalicelib.logging import get_logger

logger = get_logger()


def get_s3_client():
    s3 = None
    try:
        profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
        logger.info('profile: {}'.format(profile))
        if profile:
            session = boto3.session.Session(profile_name=profile)
            s3 = session.client(
                's3',
                region_name="sa-east-1"
            )
        else:
            s3 = boto3.client(
                's3',
                region_name="sa-east-1"
            )
    except Exception as err:
        logger.error(err)

    return s3
