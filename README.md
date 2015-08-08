CfAPI_Attendance_Sync
=====================

A real hacked together attempt to push Attendence data into the CfAPI. Our 
first goal is Meetup. Currently we are fetching attendee data from Meetup and
formatting it to push to the CfAPI.

## Requirements

- Python
- Virtualenv

## Install

    git clone
    cd cfapi_attendance_sync
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

## Run It

This will fetch attendees from all of your events from the past week and push
them to the CfAPI:

    CFAPI_ORG_ID=Open-Twin-Cities MEETUP_GROUP_URLNAME=OpenTwinCities MEETUP_API_KEY=OurKey ./app.py

Need to specify a different timeframe? Just define the `MEETUP_TIME_FRAME` 
environment variable, which uses Meetup's time frame syntax: 
`<beginning>,<end>`, where either time can be the number of milliseconds since 
the start of the Unix epoch, a string representing a relative time (e.g. `-1m`
for one month in the past, `1w` for one week in the future), or nothing to 
indicate the beginning/end of time.

Sync attendees from all of the events you've ever had:

    MEETUP_TIME_FRAME=, CFAPI_ORG_ID=Open-Twin-Cities MEETUP_GROUP_URLNAME=OpenTwinCities MEETUP_API_KEY=OurKey ./app.py

Sync attendees from all events in the last day:

    MEETUP_TIME_FRAME=-1d, CFAPI_ORG_ID=Open-Twin-Cities MEETUP_GROUP_URLNAME=OpenTwinCities MEETUP_API_KEY=OurKey ./app.py
