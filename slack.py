import os
import json
import logging

import requests
from requests.exceptions import RequestException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")
SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
SLACK_POST_MESSAGE_API_URL = "https://slack.com/api/chat.postMessage"


def format_payload_into_slack_blocks(data: dict) -> dict:
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "COAR Notification",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{json.dumps(data, indent=4)}```",
                },
            },
            {
                "type": "divider",
            },
        ],
    }


def post_slack_message(payload: dict) -> None:
    try:
        response = requests.post(
            url=SLACK_POST_MESSAGE_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SLACK_API_TOKEN}",
            },
            json={
                "channel": SLACK_CHANNEL,
                **format_payload_into_slack_blocks(payload),
            }
        )
        response.raise_for_status()

        if response.status_code == 201:
            logger.info("Message posted successfully to Slack.")
        else:
            logger.warning(f"Failed to post message to Slack. Response: {response.json()}")

    except RequestException:
        logger.exception(f"An error occurred while trying to post the message to Slack.")