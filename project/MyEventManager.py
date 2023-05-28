# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on 'Enable the Google Calendar API'
# Configure your OAuth client - select 'Desktop app', then proceed
# Click on 'Download Client Configuration' to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the 'View your calendars' permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path
import re
from typing import Type
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from EventCreator import *
from EventHelper import convert_to_id, check_valid_email

# If modifying these scopes, delete the file token.pickle.

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_api():  # pragma: no cover
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if number_of_events <= 0:
        raise ValueError('Number of events must be at least 1.')

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def add_attendees(api, event_id, starting_time, attendees_list):
    """ allows the user to add an attendee list to an existing event
    looking up the event id. If event does not exist than an Exception will be raised.
    """
    event_id = event_id

    events_result = api.events().list(calendarId='primary', timeMax=starting_time,
                                      singleEvents=True,
                                      orderBy='startTime').execute()
    event_list = events_result.get('items', [])
    contains_id = False
    for event in event_list:
        if event_id == event['id']:
            contains_id = True
    if contains_id:
        event = api.events().get(calendarId='primary', eventId=event_id).execute()
        event['attendees'] = attendees_list
        api.events().patch(calendarId='primary', eventId=event['id'], body=event).execute()
        print("success")
    else:
        raise Exception('Event does not exist!')


def create_attendee(email, attendee_name):
    """ Creates a dictionary of the attendee details that will be used for the attendee list 
    to add to the event in the api.
    """
    if type(email) != str and type(attendee_name) != str:
        raise TypeError("Email and attendee name must be of type string")
    attendee = {
        "id": convert_to_id(attendee_name),
        "email": email,
        "displayName": attendee_name,
    }

    return attendee

def get_attendees(number_of_attendees):
    """ Creates a list of attendees using user input and creates attendee dictionaries
    that are appended to the attendee list.
    Only a maximum of 20 attendees can be created for a particular event.
    """
    if type(number_of_attendees) != int:
        raise TypeError("Number of attendees must be a positive integer.")

    elif number_of_attendees <= 0:
        raise ValueError("Number of attendees must be greater than zero")

    if number_of_attendees > 20:
        raise ValueError("Only upto 20 attendees are supported by the application")

    attendee_list = []

    for i in range(number_of_attendees):
        print("Attendee " + str(i + 1))
        name = input("Enter the attendee's name: ")
        email = input("Enter the attendee's email address: ")
        while not check_valid_email(email):
            email = input("Please enter a valid email address: ")
        attendee_list.append(create_attendee(email, name))
    return attendee_list


def send_event(api, summary):
    event = create_event(summary, Meeting.ONLINE, '2022-09-20', 'Discord')
    api.events().insert(calendarId='primary', body=event).execute()
    return 'success'


def delete_event(api, current_time, event_summary):
    """ This method deletes a past event"""
    event_id = convert_to_id(event_summary)
    events_result = api.events().list(calendarId='primary', timeMax=current_time,
                                      singleEvents=True,
                                      orderBy='startTime').execute()
    event_list = events_result.get('items', [])
    contains_id = False
    for event in event_list:
        # print(event['id'] + '\n')
        if event_id == event['id']:
            contains_id = True
    if contains_id:
        api.events().delete(calendarId='primary', eventId=event_id).execute()
        return 'success'
    else:
        raise Exception('Event does not exist!')


def cancel_event(api, event_summary):
    """This method cancels an upcoming event"""
    event_id = convert_to_id(event_summary)
    events_result = api.events().list(calendarId='primary', singleEvents=True,
                                      orderBy='startTime').execute()
    event_list = events_result.get('items', [])
    contains_id = False
    for event in event_list:
        # print(event['status'] + '\n')
        if event_id == event['id']:
            contains_id = True
    if contains_id:
        # First retrieve the event from the API.
        event = api.events().get(calendarId='primary', eventId=event_id).execute()
        event['status'] = 'cancelled'
        api.events().patch(calendarId='primary', eventId=event['id'], body=event).execute()
        return 'success'
    else:
        raise Exception('Event does not exist!')


def set_reminder(api, event_summary, time_before_in_mins: int):
    """ This method sets the time before the event when which a reminder should be produced"""
    event_id = convert_to_id(event_summary)
    events_result = api.events().list(calendarId='primary', singleEvents=True,
                                      orderBy='startTime').execute()
    event_list = events_result.get('items', [])
    contains_id = False
    for event in event_list:
        # print(event['status'] + '\n')
        if event_id == event['id']:
            contains_id = True
    if contains_id:
        # First retrieve the event from the API.
        event = api.events().get(calendarId='primary', eventId=event_id).execute()
        event['reminders']['overrides'][0]['minutes'] = time_before_in_mins
        api.events().patch(calendarId='primary', eventId=event['id'], body=event).execute()
    else:
        raise Exception('Event does not exist!')


def search_event(api, event_summary):
    """Look up the event in the calendar api to check if the event exists or not"""
    event_id = convert_to_id(event_summary)
    events_result = api.events().list(calendarId='primary', singleEvents=True,
                                      orderBy='startTime').execute()
    event_list = events_result.get('items', [])
    contains_id = False
    for event in event_list:
        if event_id == event['id']:
            contains_id = True
    if contains_id:
        return True
    else:
        return False


def main():  # pragma: no cover
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events = get_upcoming_events(api, time_now, 10)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    print('\n')



if __name__ == '__main__':  # Prevents the main() function from being called by the test suite runner
    main()  # pragma: no cover
