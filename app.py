import boto3
import logging
import os
import sys
import urlparse

from dotenv import load_dotenv, find_dotenv
from base64 import b64decode

from chalice import Chalice, ForbiddenError, BadRequestError
from chalicelib import commands

de = find_dotenv()
if de is not None:
    load_dotenv(de)

app = Chalice(app_name='gochefit-slackbot')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
app.debug = True

slack_token = os.environ.get('SLACK_TOKEN')


try:
    slack_token = boto3.client('kms').decrypt(
                        CiphertextBlob=b64decode(slack_token)
                    )['Plaintext']
except:
    logger.warning("Could not decrypt the slack token")

@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index():
    body = urlparse.parse_qs(app.current_request.raw_body)

    if 'token' not in body:
        raise BadRequestError

    token = body['token'][0]

    if token != slack_token:
        raise ForbiddenError("Invalid token")

    if 'text' not in body:
        raise BadRequestError

    command = body['text'][0]

    result = commands.process_command(command)

    if result is None:
        raise BadRequestError("No command found!")
    else:
        return result
