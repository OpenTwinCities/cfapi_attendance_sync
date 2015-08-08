#! /usr/bin/env python
from datetime import datetime
import logging
import os
import requests

logging.basicConfig(level=logging.DEBUG)

group_urlname = os.environ['MEETUP_GROUP_URLNAME']
time_frame = '-1w,',
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

    r = requests.get(url, params=params).json()
    events = r['results']
    if r['meta']['next']:
        events = events + fetch_meetup_events(url=r['meta']['next'])
    return events

events = fetch_meetup_events(group_urlname, time_frame, api_key)
logging.info('Fetched %d events from Meetup' % len(events))
for event in events:
    print "Event ID: " + event['id']
    print "Event Name: " + event['name']
    print "Event DateTime: " + datetime.fromtimestamp(
        event['time']/1000.0).strftime('%Y-%m-%d %H:%M:%S')


#def fetch_attendees(group_urlname, event_id, api_key):
#	event_url ='https://api.meetup.com/$group_urlname/events/$event_id/attendance?&sign=true&filter=attended&page=50&key=$api_key'
#	return fetch_attendees_from_url(event_url)


#def fetch_attendees_from_url(url)
#	Request url
#	Add all results to a hash with name
#	If a person has a guest, add a "Guest"
#	If response has a next_link, hash.merge(fetch_attendees(next_link))
#	return hash
#
#events = fetch_events($group_url, $time_frame, $api_key)
#
#for event in events.results
#	attendees = fetch_attendees($group_urlname, event.id, $api_key)
