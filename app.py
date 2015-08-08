#! /usr/bin/env python
from datetime import datetime
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)

group_urlname = os.environ['MEETUP_GROUP_URLNAME']
time_frame = os.environ.get('MEETUP_TIME_FRAME', '-1w,')
api_key = os.environ['MEETUP_API_KEY']


def fetch_meetup_events(group_urlname=None, time_frame=None, api_key=None,
                        url=None):
    """Fetch recent Brigade events from Meetup

    :param group_urlname: Brigade identifier used in Meetup URLs, e.g.
        OpenTwinCities. Required if `url` is not provided.
    :param time_frame: Period of time to fetch events from. Matchs Meetup's
        time format: `<beginning>,<end>`, with either being absolute time in
        milliseconds since the Unix epoch, or relative dates e.g. `1m` or
        `-1w`. Required if `url` is not provided.
    :param api_key: Key used to authenticate the request to Meetup's API. See
        https://secure.meetup.com/meetup_api/key/. Required if `url` is not
        provided.
    :param url: If provided, the url that will be called to fetch events. If
        not provided, then the url will be constructed based on
        `group_urlname`, `time_frame`, and `api_key`.
    :return: List of events
    :rtype: List of dictionaries

    Usage::
        # Fetch events from the last week
        events = fetch_meetup_events('OpenTwinCities', '-1w,', 'OurKey')
        for event in events:
            print "Event ID:" + event['id']
            print "Event Name:" + event['name']
            print "Event DateTime" + datetime.fromtimestamp(
                event['time']/1000.0).strftime('%Y-%m-%d %H:%M:%S')

    """
    if url is None:
        if group_urlname is None or time_frame is None or api_key is None:
            raise ValueError('group_urlname, time_frame, and api_key must be'
                             'set')
        # Using Meetup V2 Events API
        # http://www.meetup.com/meetup_api/docs/2/events/
        url = 'https://api.meetup.com/2/events'
        params = {
            'group_urlname': group_urlname,
            'time': time_frame,
            'status': 'past',
            'page': 20,
            'key': api_key
        }
    else:
        params = None

    # Note the differnce in how V2 and V3 handle next links.
    # In V2, 'next' is part of the body.
    r = requests.get(url, params=params).json()
    events = r['results']
    if r['meta']['next']:
        events += fetch_meetup_events(url=r['meta']['next'])
    return events


def fetch_meetup_attendees(group_urlname=None, event_id=None, api_key=None,
                           url=None):
    """Fetch the attendees of a specific event

    :param group_urlname: Brigade identifier used in Meetup URLs, e.g.
        OpenTwinCities. Required if `url` is not provided.
    :param event_id: Meetup ID string for the event to fetch attendees of.
        Required if `url` is not provided.
    :param api_key: Key used to authenticate the request to Meetup's API. See
        https://secure.meetup.com/meetup_api/key/. Required if `url` is not
        provided.
    :param url: If provided, the url that will be called to fetch attendees. If
        not provided, then the url will be constructed based on
        `group_urlname`, `event_id`, and `api_key`.
    :return: List of attendees
    :rtype: List of dictionaries

    Usage::
        # Fetch attendees for event with ID '12345abcd'
        attendees = fetch_meetup_events('OpenTwinCities', '12345abcd',
                                        'OurKey')
        for attendee in attendees:
            print "Attendee Name:" + attendee['member']['name']

    """

    if url is None:
        if group_urlname is None or event_id is None or api_key is None:
            raise ValueError('group_urlname, event_id, and api_key must be'
                             'set')
        # Using Meetup V3 Attendance API
        # http://www.meetup.com/meetup_api/docs/:urlname/events/:id/attendance/
        url = (
            'https://api.meetup.com/%(group_urlname)s'
            '/events/%(event_id)s/attendance' % {
                'group_urlname': group_urlname,
                'event_id': event_id
            }
        )
        params = {
            'sign': 'true',
            'filter': 'attended',
            'page': 50,
            'key': api_key
        }
    else:
        params = None

    # Note the differnce in how V2 and V3 handle next links.
    # In V3, 'next' is a link header.
    r = requests.get(url, params=params)
    attendees = r.json()
    if 'next' in r.links:
        attendees += fetch_meetup_attendees(url=r.links['next']['url'])
    return attendees

# Pseudocode:
#   for event in events:
#       attendees = fetch_attendees(event)
#       push_to_cfapi(event, attendees)


if __name__ == '__main__':

    events = fetch_meetup_events(group_urlname, time_frame, api_key)
    logging.info('Fetched %d events from Meetup' % len(events))
    for event in events:
        logging.info("Event ID: " + event['id'])
        logging.info("Event Name: " + event['name'])
        logging.info("Event DateTime: " + datetime.fromtimestamp(
            event['time']/1000.0).strftime('%Y-%m-%d %H:%M:%S'))
        attendees = fetch_meetup_attendees(group_urlname, event['id'], api_key)
        logging.info("\tFetched %d attendees" % len(attendees))
        for attendee in attendees:
            logging.info("\tAttendee Name: " + attendee['member']['name'])
