from cgitb import text
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack.errors import SlackApiError

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


def getUserName(user_id):
    try:
        # Call the users.info method using the WebClient
        result = client.users_info(
            user=user_id
        )
        user = result.get("user", {})
        return user["real_name"]

    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
        return ""


def sendMessage(user_id):
    user_name = getUserName(user_id)
    message = f"""
        Hi {user_name} :wave:,
        \n\n Welcome to the Atri community! We are so excited to have you here 🥰
        \n\n Please check the frequently asked questions below:
        \n\n - <https://github.com/Atri-Labs/atrilabs-engine/discussions/categories/help-installation-start|Installation>
        \n - <https://github.com/Atri-Labs/atrilabs-engine/discussions|General Resources>
        \n\n Check out the channels below to connect with everyone here:
        \n\n - <https://atricommunity.slack.com/archives/C03TJHWSA2F|#introductions> - we’d love to get to know you better!
        \n - <https://atricommunity.slack.com/archives/C03TJPYR2E7|#queries> - ask questions about the Atri framework here
        \n - <https://atricommunity.slack.com/archives/C03TJT3NZU2|#resources> - find resources to make the best use of the Atri framework
        \n - <https://atricommunity.slack.com/archives/C03TXAAENGZ|#gallery> - share your apps here
        \n - <https://atricommunity.slack.com/archives/C03TJM05DB4|#random> - anything else
        \n\n If you have any questions or suggestions, feel free to DM the community organizers: <https://atricommunity.slack.com/team/U03U8C5M9UG|@Darshita> <https://atricommunity.slack.com/team/U03U8C7KDHN|@Shyam Swaroop>
    """
    client.chat_postMessage(channel=user_id, text=message)


@slack_event_adapter.on('member_joined_channel')
def message(payload):
    event = payload.get("event", {})
    user_id = event.get("user")

    sendMessage(user_id)


if __name__ == "__main__":
    app.run(debug=True)
