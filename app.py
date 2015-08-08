#! /usr/bin/env python
from datetime import datetime
import logging
import os
import requests

logger = logging.getLogger('CfAPI_Attendance_Sync')
logger.setLevel(logging.INFO)

group_urlname = os.environ['MEETUP_GROUP_URLNAME']
time_frame = os.environ.get('MEETUP_TIME_FRAME', '-1w,')
api_key = os.environ['MEETUP_API_KEY']


class MeetupClient(object):
    """Very basic client class for fetching event/attendee data.
    """

    def __init__(self, group_urlname, api_key):
        """
        :param group_urlname: Brigade identifier used in Meetup URLs, e.g.
            OpenTwinCities. Required if `url` is not provided.
        :param api_key: Key used to authenticate the request to Meetup's API.
            See https://secure.meetup.com/meetup_api/key/. Required if `url` is
            not provided.
        """

        if group_urlname is None or api_key is None:
            raise ValueError('group_urlname, and api_key must be set')
        self.group_urlname = group_urlname
        self.api_key = api_key

    def fetch_events(self, time_frame=None, url=None):
        """Fetch recent Brigade events from Meetup

        :param time_frame: Period of time to fetch events from. Matchs Meetup's
            time format: `<beginning>,<end>`, with either being absolute time
            in milliseconds since the Unix epoch, or relative dates e.g. `1m`
            or `-1w`. Required if `url` is not provided.
        :param url: If provided, the url that will be called to fetch events.
            If not provided, then the url will be constructed based on
            `time_frame`, `group_urlname`, and `api_key`.
        :return: List of events
        :rtype: List of dictionaries

        Usage::
            # Fetch events from the last week
            meetup_client = MeetupCient('OpenTwinCities', 'OurKey')
            events = meetup_client.fetch_events(-1w,')
            for event in events:
                print "Event ID:" + event['id']
                print "Event Name:" + event['name']
                print "Event DateTime" + datetime.fromtimestamp(
                    event['time']/1000.0).strftime('%Y-%m-%d %H:%M:%S')

        """

        if url is None:
            if time_frame is None:
                raise ValueError('time_frame must be provided if not '
                                 'providing url')
            # Using Meetup V2 Events API
            # http://www.meetup.com/meetup_api/docs/2/events/
            url = 'https://api.meetup.com/2/events'
            params = {
                'group_urlname': self.group_urlname,
                'time': time_frame,
                'status': 'past',
                'page': 20,
                'key': self.api_key
            }
        else:
            params = None

        # Note the differnce in how V2 and V3 handle next links.
        # In V2, 'next' is part of the body.
        r = requests.get(url, params=params).json()
        events = r['results']
        if r['meta']['next']:
            events += self.fetch_events(url=r['meta']['next'])
        return events

    def fetch_attendees(self, event_id=None, url=None):
        """Fetch the attendees of a specific event

        :param event_id: Meetup ID string for the event to fetch attendees of.
            Required if `url` is not provided.
        :param url: If provided, the url that will be called to fetch
            attendees. If not provided, then the url will be constructed based
            on `event_id`, `group_urlname`, and `api_key`.
        :return: List of attendees
        :rtype: List of dictionaries

        Usage::
            # Fetch attendees for event with ID '12345abcd'
            meetup_client = MeetupCient('OpenTwinCities', 'OurKey')
            attendees = meetup_client.fetch_events('12345abcd')
            for attendee in attendees:
                print "Attendee Name:" + attendee['member']['name']

        """

        if url is None:
            if event_id is None:
                raise ValueError('event_id must be provided if not providing '
                                 'url')
            # Using Meetup V3 Attendance API
            # http://www.meetup.com/meetup_api/docs/:urlname/events/:id/attendance/
            url = (
                'https://api.meetup.com/%(group_urlname)s'
                '/events/%(event_id)s/attendance' % {
                    'group_urlname': self.group_urlname,
                    'event_id': event_id
                }
            )
            params = {
                'sign': 'true',
                'filter': 'attended',
                'page': 50,
                'key': self.api_key
            }
        else:
            params = None

        # Note the differnce in how V2 and V3 handle next links.
        # In V3, 'next' is a link header.
        r = requests.get(url, params=params)
        attendees = r.json()
        if 'next' in r.links:
            attendees += self.fetch_attendees(url=r.links['next']['url'])
        return attendees


# Pseudocode:
#   for event in events:
#       attendees = fetch_attendees(event)
#       push_to_cfapi(event, attendees)


if __name__ == '__main__':

    meetup_client = MeetupClient(group_urlname, api_key)
    events = meetup_client.fetch_events(time_frame)
    logging.info('Fetched %d events from Meetup' % len(events))
    for event in events:
        logger.info("Event ID: " + event['id'])
        logger.info("Event Name: " + event['name'])
        logger.info("Event DateTime: " + datetime.fromtimestamp(
            event['time']/1000.0).strftime('%Y-%m-%d %H:%M:%S'))
        attendees = meetup_client.fetch_attendees(event['id'])
        logger.info("\tFetched %d attendees" % len(attendees))
        for attendee in attendees:
            logger.info("\tAttendee Name: " + attendee['member']['name'])
