import unittest
import EventHelper


# Add other imports here if needed

class TestFormatDate(unittest.TestCase):
    def test_format_date_invalid_date_format(self):
        """Tests for an invalid date which can also mean empty strings"""
        test_date = '21022023'
        self.assertRaises(Exception, lambda: EventHelper.format_date(test_date))

    def test_format_date_yyyy_mm_dd(self):
        """Tests for dates entered the yyyy-mm-dd format"""
        test_date = '2023-02-21'
        self.assertEqual(EventHelper.format_date(test_date), '2023-02-21')

    def test_format_date_dd_mm_yyyy(self):
        """Tests for dates entered the dd-mm-yyyy format"""
        test_date = '10-03-2023'
        self.assertEqual(EventHelper.format_date(test_date), '2023-03-10')

    def test_format_date_not_string(self):
        """Tests for dates entered as a type other than string"""
        test_date = 10032023
        self.assertRaises(TypeError, lambda: EventHelper.format_date(test_date))

class TestEmailChecker(unittest.TestCase):
    def test_valid_email1(self):
        """Test for a valid email address"""
        email_address = "shyam.borkar108@gmail.com"
        self.assertTrue(EventHelper.check_valid_email(email_address))

    def test_valid_email2(self):
        """Test for another valid email address"""
        email_address = "sbor0018@student.monash.edu"
        self.assertTrue(EventHelper.check_valid_email(email_address))

    def test_invalid_email_address(self):
        """Test for an invalid email address (without the @ symbol)
        """
        email_address = "shyam.borkar.hotmail.com"
        self.assertFalse(EventHelper.check_valid_email(email_address))

class TestConvertToID(unittest.TestCase):
    def test_convert_to_id_not_string(self):
        """Tests for event summaries entered as a type other than string"""
        test_summary = 69696
        self.assertRaises(TypeError, lambda: EventHelper.convert_to_id(test_summary))

    def test_convert_to_id_input_too_short(self):
        """
        Tests for inputs entered that are too short
        Not necessary, but summaries that are too short might cause the same summary to accidentally used again
        """
        test_summary = 'test'
        self.assertRaises(Exception, lambda: EventHelper.convert_to_id(test_summary))

    def test_convert_to_id_valid(self):
        """Tests for summaries with a valid type and length"""
        test_summary = 'lunch'
        self.assertEqual(EventHelper.convert_to_id(test_summary), '10811711099104')

class TestLocationAddressChecker(unittest.TestCase):
    def test_valid_address1(self):
        """Test for a valid address with a valid country name"""
        address = "Mrs Smith\n98 Shirley Street\nPIMPAMA QLD 420\nAUSTRALIA"
        self.assertTrue(EventHelper.location_address_checker(address))

    def test_valid_address2(self):
        """Test for another valid address with a valid country name"""
        address = "Mr Borkar\nSuasana Sentral Loft Jln. Stesen Sentral\nKL 50470 Brickfields\nMALAYSIA"
        self.assertTrue(EventHelper.location_address_checker(address))

    def test_invalid_address_less_lines(self):
        """Test for an invalid address with less than 4 lines (3 lines) and
        a valid country
        """
        address = "Mr Borkar\nSuasana Sentral Loft KL 50470 Brickfields\nMALAYSIA"
        self.assertFalse(EventHelper.location_address_checker(address))

    def test_invalid_address_more_lines(self):
        """Test for an invalid address with more than 4 lines (5 lines) and
        a valid country
        """
        address = "Mr Borkar\nSuasana Sentral Loft\nKL\n50470 Brickfields\nMALAYSIA"
        self.assertFalse(EventHelper.location_address_checker(address))

    def test_invalid_country_address(self):
        """Test for an valid address with less than 4 lines (3 lines) and
        an invalid country (KRYPTON)
        """
        address = "Mr Borkar\nSuasana Sentral Loft\nKL 50470 Brickfields\nKRYPTON"
        self.assertFalse(EventHelper.location_address_checker(address))

    def test_address_raises_type_error(self):
        """Test that method should not work with any type except for string and
        it should raise an error.
        """
        address = 55
        self.assertRaises(TypeError, lambda: EventHelper.location_address_checker(address))


def main():
    # Create the test suites from the cases above.
    date_format_suite = unittest.TestLoader().loadTestsFromTestCase(TestFormatDate)
    email_checker_suite = unittest.TestLoader().loadTestsFromTestCase(TestEmailChecker)
    convertID_suite = unittest.TestLoader().loadTestsFromTestCase(TestConvertToID)
    address_suite = unittest.TestLoader().loadTestsFromTestCase(TestLocationAddressChecker)
    # This will run the test suites.
    unittest.TextTestRunner(verbosity=2).run(date_format_suite)
    unittest.TextTestRunner(verbosity=2).run(email_checker_suite)
    unittest.TextTestRunner(verbosity=2).run(convertID_suite)
    unittest.TextTestRunner(verbosity=2).run(address_suite)


main()
