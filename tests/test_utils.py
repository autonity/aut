"""
Test util functions
"""

from autcli.utils import parse_wei_representation
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
        self.assertEqual(1, parse_wei_representation("1"))
        self.assertEqual(1, parse_wei_representation("1wei"))
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
