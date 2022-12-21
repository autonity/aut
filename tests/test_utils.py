"""
Test util functions
"""

from autcli.utils import parse_wei_representation, parse_token_value_representation
from autcli.constants import AutonDenoms

from unittest import TestCase


class TestUtils(TestCase):
    """
    Test util functions
    """

    def test_wei_parser(self) -> None:
        """
        Test Wei parser
        """
        self.assertEqual(
            AutonDenoms.KWEI_VALUE_IN_WEI, parse_wei_representation("1kwei")
        )
        self.assertEqual(
            AutonDenoms.MWEI_VALUE_IN_WEI, parse_wei_representation("1mwei")
        )
        self.assertEqual(
            AutonDenoms.GWEI_VALUE_IN_WEI, parse_wei_representation("1gwei")
        )
        self.assertEqual(
            AutonDenoms.SZABO_VALUE_IN_WEI, parse_wei_representation("1szabo")
        )
        self.assertEqual(
            AutonDenoms.FINNEY_VALUE_IN_WEI, parse_wei_representation("1finney")
        )
        self.assertEqual(
            AutonDenoms.AUTON_VALUE_IN_WEI, parse_wei_representation("1auton")
        )
        self.assertEqual(
            AutonDenoms.AUTON_VALUE_IN_WEI, parse_wei_representation("1aut")
        )

        # Fractional parts
        self.assertEqual(200, parse_wei_representation("0.2kwei"))
        self.assertEqual(
            AutonDenoms.FINNEY_VALUE_IN_WEI * 500, parse_wei_representation("0.5auton")
        )
        self.assertEqual(
            AutonDenoms.FINNEY_VALUE_IN_WEI * 500, parse_wei_representation("0.5auton")
        )
        self.assertEqual(
            AutonDenoms.FINNEY_VALUE_IN_WEI * 200, parse_wei_representation("0.2")
        )

    def test_token_value_parser(self) -> None:
        """
        Test token value parser.
        """

        self.assertEqual(312345, parse_token_value_representation("3.12345", 5))
        self.assertEqual(31234, parse_token_value_representation("3.12345", 4))
        self.assertEqual(3123, parse_token_value_representation("3.12345", 3))
        self.assertEqual(312, parse_token_value_representation("3.12345", 2))
        self.assertEqual(31, parse_token_value_representation("3.12345", 1))
        self.assertEqual(3, parse_token_value_representation("3.12345", 0))
