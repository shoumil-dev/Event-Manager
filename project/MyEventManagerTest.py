import unittest
from unittest.mock import MagicMock, Mock, patch
import EventHelperTest
from EventHelper import convert_to_id
import MyEventManager


# Add other imports here if needed

class TestEvents(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    def test_send_event(self):
        """
        This test tests adding events to the calendar.
        """
        mock_api = Mock()
        MyEventManager.send_event(mock_api, 'test_summary')
        self.assertEqual(
            mock_api.events.return_value.insert.return_value.execute.call_count, 1)


class TestDeleteAndCancelEvents(unittest.TestCase):

    def test_delete_event_event_exists(self):
        """
        This test tests deleting events from the calendar.
        First tests that the specified event has been found.
        Then tests that the api has been called to delete the event successfully.
        """
        event_summary = 'Lunch at Testings house'
        event_id = convert_to_id(event_summary)
        eventlist = [{'id': event_id, 'status': 'confirmed'}, {'id': '12345', 'status': 'confirmed'}]
        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = eventlist
        MyEventManager.delete_event(mock_api, 'current_time', event_summary)
        self.assertEqual(
            mock_api.events.return_value.delete.return_value.execute.call_count, 1)

    def test_cancel_event_exists(self):
        """
        This test tests trying to cancel a valid event
        Tests that the event is found.
        Tests that the call to cancel the event has been successfully performed.

        """
        event_summary = 'Lunch at Testings house'
        event_id = convert_to_id(event_summary)
        eventlist = [{'id': event_id, 'status': 'confirmed'}, {'id': '12345', 'status': 'confirmed'}]
        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = eventlist
        mock_api.events.return_value.get.return_value.execute.return_value = {'id': event_id, 'status': 'confirmed'}
        MyEventManager.cancel_event(mock_api, event_summary)
        # Tests that the patch function is called once
        self.assertEqual(
            mock_api.events.return_value.patch.return_value.execute.call_count, 1)

    def test_cancel_event_does_not_exist(self):
        """
        This test tests trying to cancel an invalid event.
        Tests that the nonexistent event is not found and as a result the call to cancel an event is not performed.
        """
        nonexistent_event_summary = 'Fake'
        eventlist = [{'id': '56789', 'status': 'confirmed'}, {'id': '12345', 'status': 'confirmed'}]
        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = eventlist
        mock_api.events.return_value.get.return_value.execute.return_value = {'id': '56789', 'status': 'confirmed'}
        # Tests that an nonexistent event raises an exception
        self.assertRaises(Exception, lambda: MyEventManager.cancel_event(
            mock_api, nonexistent_event_summary))


class TestSetReminder(unittest.TestCase):
    def test_set_reminder_event_exists(self):
        """
        This test tests setting a reminder to be shown in the user's application.
        Tests that the specified event is found.
        Tests that the api has been called to cancel the event successfully.
        """
        event_summary = 'Lunch at Testings house'
        event_id = convert_to_id(event_summary)
        time_before_in_mins = 15
        eventlist = [{'id': event_id, 'status': 'confirmed'}, {'id': '12345', 'status': 'confirmed'}]
        fake_event = {
            'id': event_id, 'reminders': {'usedefault': False, 'overrides': [
                {'method': 'popup', 'minutes': time_before_in_mins}]}}
        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = eventlist
        mock_api.events.return_value.get.return_value.execute.return_value = fake_event
        MyEventManager.set_reminder(mock_api, event_summary, time_before_in_mins)
        # Tests that the patch function is called once
        self.assertEqual(
            mock_api.events.return_value.patch.return_value.execute.call_count, 1)


class TestAttendees(unittest.TestCase):

    def test_create_attendee(self):
        """Test if an attendee dictionary is created properly as required by the google
        calendar api.
        """
        email = "shyam.borkar108@gmail.com"
        attendee_name = "Shyam Kamalesh Borkar"
        created_attendee = MyEventManager.create_attendee(email, attendee_name)

        self.assertTrue(type(created_attendee) == dict)
        self.assertEqual(created_attendee["email"], email)
        self.assertEqual(created_attendee["displayName"], attendee_name)
        self.assertRaises(TypeError, lambda: MyEventManager.create_attendee(55, 33))

    def test_get_invalid_attendees_list(self):
        """ test if get_attendees raises type error when anything but an integer is fed into it and 
        raises a value error when an attendee number of greater than 20 is passed in
        """
        invalid_attendee_num_type = "19"
        invalid_num_attendees = 21
        # cannot pass in a string as an argument
        self.assertRaises(TypeError, lambda: MyEventManager.get_attendees(invalid_attendee_num_type))

        # Number of attendees cannot be greater than 20
        self.assertRaises(ValueError, lambda: MyEventManager.get_attendees(invalid_num_attendees))

    @patch('MyEventManager.get_attendees',
           return_value=[{"id": convert_to_id("Shyam"), "email": "sbor0018@student.monash.edu", "displayName": "Shyam"},
                         {"id": convert_to_id("Shoumil"), "email": "sguh0003@student.monash.edu",
                          "displayName": "Shoumil"}])
    def test_get_valid_attendees_list(self, get_attendees):
        """get_attendees creates a list of attendee dicts based on the number of
        attendees the user specifies (attendee limit is 20 any more will raise an error)
        """

        attendees_list = [
            {"id": convert_to_id("Shyam"), "email": "sbor0018@student.monash.edu", "displayName": "Shyam"},
            {"id": convert_to_id("Shoumil"), "email": "sguh0003@student.monash.edu", "displayName": "Shoumil"}]

        # adding 2 attendees
        self.assertEqual(get_attendees(2), attendees_list)

    def test_add_attendees(self):
        event_summary = 'Discuss FIT2107 Assignment 3'
        event_id = convert_to_id(event_summary)
        attendees_list = [
            {"id": convert_to_id("Shyam"), "email": "sbor0018@student.monash.edu", "displayName": "Shyam"},
            {"id": convert_to_id("Shoumil"), "email": "sguh0003@student.monash.edu", "displayName": "Shoumil"}]
        mock_api = Mock()
        eventlist = [{'id': event_id, 'status': 'confirmed'}, {'id': '12345', 'status': 'confirmed'}]
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = eventlist
        mock_api.events.return_value.get.return_value.execute.return_value = {'id': event_id, 'status': 'confirmed'}
        MyEventManager.add_attendees(mock_api, event_id, 'starting_time', attendees_list)

        self.assertEqual(mock_api.events.return_value.patch.return_value.execute.call_count, 1)

        # Tests that a nonexistent event raises an exception
        nonexistent_event_id = '234'
        with self.assertRaises(Exception):
            MyEventManager.add_attendees(mock_api, nonexistent_event_id, 'starting_time', attendees_list)


class TestSearchEvent(unittest.TestCase):
    def test_search_event_valid(self):
        """
        This test tests deleting events from the calendar.
        First tests that the specified event has been found
        Then tests that the api has been called to delete the event successfully
        """
        event_summary = 'Lunch at Testings house'
        event_id = convert_to_id(event_summary)
        eventlist = [{'id': event_id, 'status': 'confirmed'}, {'id': '12345', 'status': 'confirmed'}]
        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = eventlist
        self.assertTrue(MyEventManager.search_event(mock_api, event_summary))


def main():
    # Running tests for EventHelper first
    EventHelperTest.main()
    # Create the test suites from the cases above.
    events_suite = unittest.TestLoader().loadTestsFromTestCase(TestEvents)
    delete_and_cancel_suite = unittest.TestLoader().loadTestsFromTestCase(TestDeleteAndCancelEvents)
    reminder_suite = unittest.TestLoader().loadTestsFromTestCase(TestSetReminder)
    attendees_suite = unittest.TestLoader().loadTestsFromTestCase(TestAttendees)
    search_suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchEvent)
    # This will run the test suites.
    unittest.TextTestRunner(verbosity=2).run(events_suite)
    unittest.TextTestRunner(verbosity=2).run(delete_and_cancel_suite)
    unittest.TextTestRunner(verbosity=2).run(reminder_suite)
    unittest.TextTestRunner(verbosity=2).run(attendees_suite)
    unittest.TextTestRunner(verbosity=2).run(search_suite)


main()
