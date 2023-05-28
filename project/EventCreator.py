from EventHelper import *


def create_event(summary: str, meeting_type: str, date: str, location: str):
    """
    Returns an event dict object with specified parameters.

    params:
        summary (str): name of the event
        meeting_type (str): description of the event - describes the event
        date (str): date of the event
        location (str): where the event takes place (online, physical, etc.)
    """
    event = {
        'id': convert_to_id(summary),
        'summary': summary,
        'location': location,
        'description': meeting_type,
        'start': {
            'date': format_date(date),
        },
        'end': {
            'date': format_date(date),
        },
        'status': 'confirmed',
        'reminders': {
            'useDefault': False,
            'overrides': [
                {
                    'method': 'popup',
                    'minutes': 69
                }
            ]
        },
    }
    return event


