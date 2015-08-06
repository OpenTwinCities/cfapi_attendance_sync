import os

groupname_url = os.environ['meetup_group_urlname'] 
time_frame = '-1w',
api_key = os.environ['meetup_api_key']

def fetch_events(group_urlname, time_frame, api_key)
	URL =
    "https://api.meetup.com/2/events?&group_urlname=$group_urlname&time=$time_frame&status=past&page=20&key=$api_key"

function fetch_attendees ($group_urlname, $event_id, $api_key):
	$event_url = https://api.meetup.com/$group_urlname/events/$event_id/attendance?&sign=true&filter=attended&page=50&key=$api_key
	return fetch_attendees_from_url(event_url)


function fetch_attendees_from_url(url)
	Request url
	Add all results to a hash with name
	If a person has a guest, add a "Guest"
	If response has a next_link, hash.merge(fetch_attendees(next_link))
	return hash

events = fetch_events($group_url, $time_frame, $api_key)

for event in events.results
	attendees = fetch_attendees($group_urlname, event.id, $api_key)
