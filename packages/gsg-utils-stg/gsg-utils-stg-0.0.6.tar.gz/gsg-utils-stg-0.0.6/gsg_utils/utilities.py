from .configuration import *
import requests
import json
import boto3

import logging
log = logging.getLogger(__name__)


def notify_slack(subject, body, tags=None):
    """
    send a message to a slack based on an environment
    :param subject: meaningful title of the notification
    :param body: notification message
    :param tags: any extra information need to send to slack
    :return:
    """
    slack_url = Configuration.get_value_by_key("SLACK_URL")
    region = Configuration.get_value_by_key("REGION")
    env = Configuration.get_value_by_key("ENV")

    ssm = boto3.client('ssm', region_name=region)

    slack_url = ssm.get_parameter(Name=slack_url, WithDecryption=True).get('Parameter').get('Value')

    if tags is None:
        tags = [f"Running in {env}"]
    data = {"text": f"{env} \n {subject}\n {body}\n {tags}"}
    resp = requests.post(slack_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    return resp


def get_secret_key_details(secret_name, tags=None):
    """
    will try to get details of the secret key by using the client
    :param secret_name: name of the secret key
    :param tags: Any tags to add while notifying slack?
    :return: json response
    """
    try:
        region = Configuration.get_value_by_key("REGION")
        env = Configuration.get_value_by_key("ENV")

        log.info(f'Making a secret call to manager with key {secret_name} in region {region} having environment {env}')

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region,
        )
        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        response = secret_value_response['SecretString']
        return response
    except Exception as ex:
        log.exception(f"Exception occurred while fetching details for key {secret_name} : {ex}")
        notify_slack(subject=f"Exception occurred while fetching details for key {secret_name}", body=f"{ex}",
                     tags=tags)
        raise
