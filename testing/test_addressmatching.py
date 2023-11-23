import unittest

from aussieaddress.compare import Address


class test_address(unittest.TestCase):
    def test_1(self):

        x = "98 Shirley Street PIMPAMA QLD 4209 AUSTRALIA"
        y = "1/98 Shirley St. PIMPAMA Queensland 4209"

        matcher = Address(x, y)
        matcher.address_match()

        self.assertEqual(matcher.match, True)

        self.assertTrue(matcher.postcode_result)
        self.assertTrue(matcher.state_result)

        contains = "street" in matcher.address2_result
        self.assertTrue(contains)


    def test_2(self):

        x = "98 Shirley Street PIMPAMA QLD 4209 AUSTRALIA"
        y = "1/98 Shirley Road PIMPAMA Queensland 4209"

        matcher = Address(x, y)
        matcher.address_match()

        self.assertEqual(matcher.match, False)
        self.assertTrue(matcher.postcode_result)
        self.assertTrue(matcher.state_result)

    def test_3(self):

        x = "98 Shirley Street PIMPAMA QLD 4209 AUSTRALIA"
        y = "1/98 Shirley St PIMPAMA Queensland 4208"

        matcher = Address(x, y)
        matcher.address_match()

        self.assertEqual(matcher.match, False)
        self.assertFalse(matcher.postcode_result)
        self.assertTrue(matcher.state_result)