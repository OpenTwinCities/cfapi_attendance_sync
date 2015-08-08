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

    CFAPI_ORG_ID=Open-Twin-Cities MEETUP_GROUP_URLNAME=OpenTwinCities MEETUP_API_KEY=OurKey ./app.py
