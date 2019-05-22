from sargilo import __version__
from django.test import TestCase


def test_version():
    assert __version__ == '0.1.0'


class BasicTest(TestCase):
    def test_basic(self):
        self.assertTrue(False)
