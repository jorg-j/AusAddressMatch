# %%
import re
import string
from functools import lru_cache
from typing import Tuple

from fuzzywuzzy import fuzz



class Address:
    def __init__(self, address1, address2):
        self.address1 = address1
        self.address2 = address2

        self.threshold = 75
        self.postcode = True
        self.state = True

        self.postcode_result = None
        self.state_result = None
        self.threshold_result = None

        self.address1_result = ""
        self.address2_result = ""

        self.match = False
        self.score = 0

        self.set_defaults()
# %%
    def set_defaults(self):
        self.abbreviated_states = ["qld", "nsw", "act", "vic", "tas", "sa", "wa", "nt"]
        self.state_names = [
            "queensland",
            "new south wales",
            "australian capital territory",
            "victoria",
            "tasmania",
            "south australia",
            "western australia",
            "northern territory",
        ]

        self.replacements = [
            ["street", "st"],
            ["road", "rd"],
            ["close", "cls"],
            ["court", "crt"],
            ["avenue", "ave", "av"],
        ]

        self.removals = [
            "au",
            "australia",
            "apartment",
            "u",
            "tower",
            "unit"
        ]



    def _clean_str(in_string: str, remove: list) -> str:
        """
        The function `_clean_str` takes a string and a list of items to remove,
        and returns the string with
        those items removed and any leading or trailing whitespace stripped.

        >>> _clean_str("This is a test", ["is", "a"])
        'This test'
        """
        expr = r"\b(?:" + "|".join(re.escape(word.lower()) for word in remove) + r")\b"
        outstring = re.sub(expr, "", in_string)
        while "  " in outstring:
            outstring = outstring.replace("  ", " ")
        return outstring.strip()


    # %%
    @staticmethod
    def postcode_match(self, address1: str, address2: str) -> Tuple[str, str, bool]:
        """
        Takes two addresses as input and checks if the last postcode in the
        first address is present in the second address,
        returning the modified addresses and a boolean
        indicating if there was a match.

        :param address1: The `address1` parameter is a string representing the first address. It is the
        address where we want to find the postcode match
        :type address1: str
        :param address2: The `address2` parameter is a string representing the second address
        :type address2: str
        :return: The function `postcode_match` returns a tuple containing three elements: the modified
        `address1` string, the modified `address2` string, and a boolean value indicating whether a postcode
        match was found.

        >>> postcode_match("123 Test St 2000", "123 Test St 2000")
        ('123 Test St', '123 Test St', True)

        >>> postcode_match("1234 Test St 2000", "1234 Test St 2000")
        ('1234 Test St', '1234 Test St', True)

        >>> postcode_match("1234 Test St", "1234 Test St 2000")
        ('1234 Test St', '1234 Test St 2000', False)
        """
        postcode_pattern = r"(?<!\d)\b\d{4}\b"

        add1_matches = re.findall(postcode_pattern, address1)

        if not add1_matches:
            return address1, address2, False

        add2_matches = re.findall(postcode_pattern, address2)

        last_postcode1 = add1_matches[-1]
        last_postcode2 = add2_matches[-1]

        if last_postcode1 == last_postcode2:
            return (
                self._clean_str(address1, [last_postcode1]),
                self._clean_str(address2, [last_postcode1]),
                True,
            )
        return address1, address2, False


    # %%
    @lru_cache(maxsize=50)
    def locate_state(address: str, state: str) -> bool:
        phrase = r"\b" + state + r"\b"
        matches = re.findall(phrase, address)
        return len(matches) > 0


    # %%
    def state_match(self, address1: str, address2: str) -> Tuple[str, str, bool]:
        """
        The function `state_match` compares two addresses and determines
        if they contain matching state information.

        :param address1: String representing the first address
        :type address1: str
        :param address2: The second address that you want to compare with
        :type address2: str
        :return: The function `state_match` returns a tuple containing
        the cleaned versions of `address1` and `address2`, along with a boolean
        indicating whether a state match was found.

        >>> state_match("123 test qld", "123 test queensland")
        ('123 test', '123 test', True)

        >>> state_match("123 test qld", "123 test nsw")
        ('123 test qld', '123 test nsw', False)

        >>> state_match("123 test qld", "123 test")
        ('123 test qld', '123 test', False)

        """
        extended_states = self.abbreviated_states + self.state_names
        extended_abbreviations = self.state_names + self.abbreviated_states

        lookup_array = dict(zip(extended_states, extended_abbreviations))

        address_lower1 = address1.lower()
        address_lower2 = address2.lower()

        for state in extended_states:
            if Address.locate_state(address=address_lower1, state=state):
                alter = lookup_array.get(state, "FAULT")
                if state in address_lower2 or alter in address_lower2:
                    cleaned_address1 = Address._clean_str(address_lower1, [state, alter])
                    cleaned_address2 = Address._clean_str(address_lower2, [state, alter])
                    return cleaned_address1, cleaned_address2, True
        return address_lower1, address_lower2, False
    

    def replacements(self, address):
        """
        Replaces certain content within the address

        >>> Address.replacements("123 short rd")
        '123 short road'
        """
        for replacement in self.replacements:
            primary = replacement[0].lower()
            pattern = r"\b(?=" + "|".join(re.escape(word.lower()) for word in replacement) + r")\b"
            address = re.sub(pattern, primary, address)
        return address
    
    @lru_cache(maxsize=50)
    def address_normaliser(self, address: str)-> str:
        """
        Takes a string and removes banned words and special characters
        As well as lowercases the string

        >>> address_normaliser("Unit 8, Test St, Lipton")
        '8 test st lipton'
        """

        new_address = address.lower()

        for word in self.removals:
            phrase = r"\b" + word + r"\b"
            new_address = re.sub(phrase, "", new_address)
        
        for character in string.punctuation:
            new_address = new_address.replace(character, " ")
        new_address = new_address.replace("  ", " ")
        new_address = Address.replacements(new_address)
        return new_address.strip()

    @lru_cache(maxsize=500)
    def address_match(self):
        """
        Compares 2 addresses and returns True if certain requirements
        are met
        """
        address1 = self.address_normaliser(self.address1)
        address2 = self.address_normaliser(self.address2)

        if self.postcode:
            address1, address2, match = self.postcode_match(address1, address2)
            if not match:
                self.postcode_result = False
            else:
                self.postcode_result = True
        
        if self.state:
            address1, address2, match = self.state_match(address1, address2)
            if not match:
                self.state_result = False
            else:
                self.state_result = True
        
        self.score = fuzz.token_sort_ratio(address1, address2)
        self.threshold_result = True if self.score > self.threshold else False

        self.address1_result = address1
        self.address2_result = address2
