# -*- coding: utf-8 -*-
import os
import time
from slacker import Slacker

api_token = os.environ.get('SLACK_API_TOKEN', '')
age_threshold = 30  # days

slack = Slacker(api_token)

# Get channels list
response = slack.channels.list(exclude_archived=1)
channels = response.body['channels']

now = int(time.time())
age_threshold_secs = age_threshold * 86400

for channel in channels:
    response = slack.channels.info(channel['id'])
    last_message = response.body['channel'].get('latest')
    if last_message:
        latest_message_secs = int(float(response.body['channel']['latest']['ts']))
    else:
        latest_message_secs = channel['created']
    last_message_ago_secs = now - latest_message_secs
    too_old = last_message_ago_secs >= age_threshold_secs

    if too_old or channel['name'] == 'test-channel':
        choice = raw_input("Channel #{} hasn't had a message in {} days and has {} members. Archive it? ".format(
            channel['name'],
            last_message_ago_secs / 86400,
            channel['num_members'],
        ))

        if choice.lower().startswith('y'):
            slack.chat.post_message(
                channel=channel['id'],
                text="People of {} your attention please. This is Prostectic Vogon Jeltz of the Galactic "
                     "Hyperspace Slack Council. As you no doubt will be aware, the plans for the development "
                     "of the outlying regions of the western spiral arm of the community require the building "
                     "of a hyperspace express route through your Slack and, regrettably, your channel is "
                     "one of those scheduled for demolition. The process will take slightly less than two of "
                     "your Earth minutes thank you very much.\n\n"
                     "*(This channel has been too quiet for too long, so we're archiving it)*".format(channel['name']),
                username="Vogon Constructor Fleet",
                icon_emoji=":rocket:",
            )

            response = slack.channels.archive(channel['id'])
            if response.body['ok']:
                print "Archived channel #{}".format(channel['name'])
        else:
            print "Skipping channel #{}".format(channel['name'])
