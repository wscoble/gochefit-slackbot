import boto3
import logging
import os
import sys
import urlparse

from dotenv import load_dotenv, find_dotenv
from base64 import b64decode

from chalice import Chalice, ForbiddenError, BadRequestError
from chalicelib import commands


app = Chalice(app_name='gochefit-slackbot')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
app.debug = True


de = find_dotenv()
if de is not None:
    load_dotenv(de)

slack_token = os.environ.get('SLACK_TOKEN')

if os.environ.get('PROD') is not None:
    slack_token = boto3.client('kms').decrypt(
                        CiphertextBlob=b64decode(slack_token)
                    )['Plaintext']


@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def handle_slack_command():
    body = urlparse.parse_qs(app.current_request.raw_body)

    if 'token' not in body or 'text' not in body:
        raise BadRequestError

    token = body['token'][0]

    if token != slack_token:
        raise ForbiddenError("Invalid token")

    command = body['text'][0]

    result = commands.process_command(command)

    if result is None:
        raise BadRequestError("No command found!")
    else:
        return result
